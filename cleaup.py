from difflib import SequenceMatcher
import Levenshtein
import os
import re


def similar(one, two):
    #return SequenceMatcher(None, one, two).ratio()
    return Levenshtein.ratio(one, two)


def sorting(value):
    return re.sub('_|\s|\d|\(|\)', 'z', value).lower()


def get_files(file):
    with open(file) as f:
        files = f.read()
    return sorted(set(files.splitlines()), key=sorting)


def get_similars(files):
    outcome = {}
    for f in files:
        similars = [(file, similar(f, file)) for file in files if .8 < similar(f, file) < .95]
        outcome[f] = similars
    return outcome


def remove_duplicates(files):
    written = []
    for file in files:
        if len(written) > 0:
            similars = [w for w in written if .8 < similar(file, w) < .99]
            if len(similars) > 0:
                decision = input('\n\nThe following file {} has the following'
                                 ' similar files already written to the file:\n'
                                 '{}.\nShould it be written? (y/n)'.format(
                    file, ','.join(similars))
                )
                if decision == 'y':
                    written.append(file)
            elif len([w for w in written if similar(file, w) == 1]) >= 1:
                pass
            else:
                written.append(file)
        else:
            written.append(file)
    return written


def to_file(files, file):
    print('#'*30)
    with open(file, 'w') as f:
        for w in files:
            f.write(w + '\n')
            print(w)
    print(len(files))


if __name__ == '__main__':
    files = get_files('new_files.txt')
    good_files = remove_duplicates(files)
    to_file(good_files, 'new_files_clean.txt')
