#!/usr/bin/python3

import os
import sys
from fnmatch import fnmatch


def find_match_in_file(filename, query):
    with open(filename, 'r') as f:
        for i, line in enumerate(f, 1):
            if query in line:
                yield i, line


def filter_files(root_dir, pattern):
    for current_dir, __, files in os.walk(root_dir):
        filtered_files = map(lambda fn: os.path.join(current_dir, fn),
                              filter(lambda fn: fnmatch(fn, pattern), files))
        for filtered_file in filtered_files:
            yield filtered_file


def grep(root_dir, pattern, query):
    for filtered_file in filter_files(root_dir, pattern):
        for i, line in find_match_in_file(filtered_file, query):
            print("{file}, #{i}: {line}".format(file=filtered_file, i=i, line=repr(line)))


if __name__ == '__main__':
    sys.exit(grep(os.getcwd(), sys.argv[1], sys.argv[2]))
