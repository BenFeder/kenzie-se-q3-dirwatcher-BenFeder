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
import datetime
import os

exit_flag = False  # Create exit flag for infinite loop to occur until True


"""Create logger"""
logger = logging.getLogger(__name__)

logging.basicConfig(
    format='%(asctime)s: %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('dirwatcher.log')
stream_handler = logging.StreamHandler()

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
    logger.warning('Received ' + signal.Signals(sig_num).name)
    exit_flag = True
    end_time = datetime.datetime.now()
    duration = start_time - end_time
    logger.info(f"Process took duration: {duration}")


def search_for_magic(filename, start_line, magic_string):
    """Search for the magic string in the file"""
    if not files_dict[filename]:
        start_line = 0
    else:
        start_line = files_dict[filename]
    with open(filename, "r") as f:
        for i, line in enumerate(f):
            if i >= start_line:
                read = line.read()
                start_line += 1
                if magic_string in read:
                    logger.info(
                        f"""{magic_string} was found in {filename} at line
                    {start_line}.""")
                files_dict[filename] = start_line


def watch_directory(path, magic_string, extension, interval):
    """Watch directory by looking at all files in directory for magic string"""
    for filename in os.listdir(path):
        if filename.endswith(extension):
            search_for_magic(filename, files_dict[filename], magic_string)
    time.sleep(interval)


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
    """Create arg parser"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', help="Monitors given directory named")
    parser.add_argument('--ext', help="Searches files with given extension")
    parser.add_argument('--int', help="Searches dir every given interval")
    parser.add_argument('magic', help="""Must input a string to search
    for in files under given directory""")

    args = parser.parse_args()

    return args


def main(args):

"""Create a namespace from create parser, then watch directory"""
    ns = create_parser()

    # Hook into these two signals from the OS
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGHUP, signal_handler)
    # Now my signal_handler will get called if OS sends
    # either of these to my process.
    while not exit_flag:
        start_time = datetime.datetime.now()
       try:
            if not ns.dir:
                logger.error("No directory given to watch.")
            else:
                watch_directory(f"{ns.dir}/", ns.magic, ns.ext, ns.int)
        except Exception as e:
            # This is an UNHANDLED exception
            # Log an ERROR level message here
            logger.error(e)

        # put a sleep inside my while loop so I don't peg the cpu usage at 100%
        time.sleep(ns.int)

    # final exit point happens here
    # Log a message that we are shutting down
    # Include the overall uptime since program start


if __name__ == '__main__':
    main(sys.argv[1:])
