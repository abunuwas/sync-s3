from difflib import SequenceMatcher
import Levenshtein
import os


def similar(one, two):
    #return SequenceMatcher(None, one, two).ratio()
    return Levenshtein.ratio(one, two)


def get_files(file):
    with open('new_files.txt') as f:
        files = f.read()
    return files.splitlines()


def get_similars(files):
    outcome = {}
    for f in files:
        similars = [(file, similar(f, file)) for file in files if .8 < similar(f, file) < .95]
        outcome[f] = similars
    return outcome


if __name__ == '__main__':
    files = get_files('new_files.txt')
    files = sorted(files, key=str.lower)
    written = []
    with open('new_files_clean.txt', 'w') as f:
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

    print('#'*30)
    for w in written:
        print(w)
    print(len(written))
