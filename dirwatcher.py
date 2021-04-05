#!/usr/bin/env python3
"""
Dirwatcher - A long-running program
"""

__author__ = "Benjamin Feder"

import sys


def search_for_magic(filename, start_line, magic_string):
    # Your code here
    return


def watch_directory(path, magic_string, extension, interval):
    # Your code here
    return


def scan_single_file():
    """
    Use to check indivdual file if it has been added or new lines
    have been added to the file
    """
    pass


def detect_added_files():
    """See if there are new files to scan"""
    pass


def detect_removed_files():
    """See if any files have been deleted"""
    pass


def create_parser():
    # Your code here
    return


def signal_handler(sig_num, frame):
    # Your code here
    return


def main(args):
    # Your code here
    return


if __name__ == '__main__':
    main(sys.argv[1:])
