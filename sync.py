import os
import subprocess
import sys
from xml.etree import ElementTree as ET
import zipfile
from zipfile import ZipFile

import boto3

s3 = boto3.client('s3')


def trim_tpl(tpl):
    try:
        key, value = tpl
        return key.lstrip(), value.lstrip()
    except (IndexError, ValueError):
        return (None, None)


def to_dict(metadata_list):
    tuples = tuple(line.split(':', 1) for line in metadata_list)
    clean = tuple(map(trim_tpl, tuples))
    return dict(clean)


def pdf_metadata(file):
    metadata = subprocess.check_output(['pdfinfo', '-meta', file]).decode('utf-8')
    if 'Metadata' in metadata:
        metadata = metadata[:metadata.find('Metadata')]
    metadata_list = metadata.splitlines()
    metadata_dict = to_dict(metadata_list)
    return {
        'Author': metadata_dict.get('Author'),
        'Title': metadata_dict.get('Title'),
        'Publisher': metadata_dict.get('Pulbisher'),
        'Date': metadata_dict.get('ModDate')
    }


def get_text_from_xml(xml, search_for):
    for el in xml:
        if search_for in el.tag:
            return el.text
    return None


def extract_metadata(metadata_xml):
    metadata = [section for section in metadata_xml.getchildren() if 'meta' in section.tag][0].getchildren()
    return {
        'Author': get_text_from_xml(metadata, 'creator'),
        'Title': get_text_from_xml(metadata, 'title'),
        'Publisher': get_text_from_xml(metadata, 'publisher'),
        'Date': get_text_from_xml(metadata, 'date')
    }


def epub_metadata(file):
    with ZipFile(file, 'r') as zip:
        metadata_file = [f for f in zip.namelist() if f.endswith('opf')][0]
        with zip.open(metadata_file) as f:
            file_metadata = f.read().decode('utf-8')
    metadata_xml = ET.fromstring(file_metadata)
    return extract_metadata(metadata_xml)


def get_files(dir):
    for dirpath, dirs, files in os.walk(dir):
        if all(map(lambda unwanted: unwanted not in dirpath, ['venv', '.git', '.idea'])):
            for file in files:
                yield os.path.join(dirpath, file)


def yield_data(dir):
    for file in get_files(dir):
        try:
            print('Parsing file {}...'.format(file))
            if file.endswith('.pdf'):
                yield pdf_metadata(file)
            elif file.endswith('.epub'):
                yield epub_metadata(file)
            else:
                yield {}
        except zipfile.BadZipFile:
            yield {}


if __name__ == '__main__':
    dir = sys.argv[1]
    print('Parsing directory {}...'.format(dir))
    with open('existing_files.txt', 'w') as f:
        for file in get_files(dir):
            f.write(os.path.basename(file) + '\n')
