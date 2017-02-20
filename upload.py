import os
import sys

from sync import get_files, s3


def file_to_lines(path):
    with open(path) as f:
        data = f.read()
    return data.splitlines()


def find_diff(existing, to_be_checked):
    total = []
    for file in to_be_checked:
        file_name = os.path.basename(file)
        if file_name not in existing:
            total.append(file_name)
    return total


def to_file(iterator, file):
    with open(file, 'w') as f:
        for i in iterator:
            f.write(i)
            print(i)


if __name__ == '__main__':
    dir = sys.argv[1]
    #existing_file = sys.argv[2]
    new_titles_file = sys.argv[2]

    new_titles = file_to_lines(new_titles_file)

    #existing = file_to_lines(existing_file)
    to_be_checked = get_files(dir)
    #diff = find_diff(existing, to_be_checked)
    #to_file(diff, 'new_files.txt')

    for file in to_be_checked:
        file_name = os.path.basename(file)
        if file_name in new_titles_file:
            print(file_name)
            #s3.upload_file(file, 'programming-books', file_name)
