import os
import sys

from sync import get_files, s3


def get_existing_files(path):
    with open(path) as f:
        existing = f.readlines()
    return existing

if __name__ == '__main__':
    dir = sys.argv[1]
    existing_file = sys.argv[2]
    existing = get_existing_files(existing_file)
    with open('new_files.txt') as f:
        for file in get_files(dir):
            if os.path.basename(file) not in existing:
                print(file)
                f.write(file)
