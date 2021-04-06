#!/usr/bin/env python3
"""
Dirwatcher - A long-running program
"""

__author__ = "Benjamin Feder"

import sys
import argparse
import logging
import signal
import time
import os

exit_flag = False

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

file_handler = logging.FileHandler('dirwatcher.log')
stream_handler = logging.StreamHandler()

file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


files_dict = {}


def signal_handler(sig_num, frame):
    """
    This is a handler for SIGTERM and SIGINT. Other signals can be mapped here
    as well (SIGHUP?)
    Basically, it just sets a global flag, and main() will exit its loop if the
    signal is trapped.
    :param sig_num: The integer signal number that was trapped from the OS.
    :param frame: Not used
    :return None
    """
    # log the associated signal name
    logger.warn('Received ' + signal.Signals(sig_num).name)


def search_for_magic(filename, start_line, magic_string):
    """Search for the magic string in the file"""
    up_to_line = 0
    if files_dict[filename] >= 1:
        up_to_line = files_dict[filename]
    with open(filename, "r") as f:
        for line in f:
            read = line.read()
            up_to_line += 1
            if magic_string in read:
                files_dict[filename] = up_to_line


def watch_directory(path, magic_string, extension, interval):
    for filename in os.listdir(path):
        if filename.endswith(extension):
            search_for_magic(filename, files_dict[filename], magic_string)


# def scan_single_file():
#     """
#     Use to check indivdual file if it has been added or new lines
#     have been added to the file
#     """
#     pass


# def detect_added_files():
#     """See if there are new files to scan"""
#     pass


# def detect_removed_files():
#     """See if any files have been deleted"""
#     pass


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dirwatch', help="Monitors given directory named")
    parser.add_argument('--ext', help="Searches files with given extension")
    parser.add_argument('--int', help="Searches dir every given interval")
    parser.add_argument('magic_string', help="""Must input a string to search
    for in files under given directory""")

    args = parser.parse_args()

    return args


def main(args):

    ns = create_parser()

    # Hook into these two signals from the OS
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGHUP, signal_handler)
    # Now my signal_handler will get called if OS sends
    # either of these to my process.

    while not exit_flag:
        try:
            if not ns.dirwatch:
                logger.error("No directory given to watch.")
            else:
                watch_directory(f"{ns.dirwatch}/",
                                ns.magic_string, ns.ext, ns.int)
        except Exception as e:
            # This is an UNHANDLED exception
            # Log an ERROR level message here
            logger.error(e)

        # put a sleep inside my while loop so I don't peg the cpu usage at 100%
        if ns.int:
            time.sleep(ns.int)

    # final exit point happens here
    # Log a message that we are shutting down
    # Include the overall uptime since program start


if __name__ == '__main__':
    main(sys.argv[1:])
