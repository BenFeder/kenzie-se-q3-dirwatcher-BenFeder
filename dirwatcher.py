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

"""
Create empty files dictionary to create key/value pairs
of what line was left off at (value = start_line)
for each file (key)
"""
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
    global exit_flag
    # log the associated signal name
    logger.warning(
        f"{datetime.datetime.now()}: Received {signal.Signals(sig_num).name}")
    exit_flag = True


def search_for_magic(filename, start_line, magic_string):
    """Search for the magic string in the file"""
    with open(filename, "r") as f:
        for line in f.readlines()[start_line:]:
            start_line += 1
            if magic_string in line:
                logger.info(
                    f"""{datetime.datetime.now()}: {magic_string} was found in {filename} at line
                {start_line}.""")
            files_dict[filename.split("/")[-1]] = start_line


def watch_directory(path, magic_string, extension):
    """Watch directory by looking at all files in directory for magic string"""
    for filename in os.listdir(path):
        if filename.endswith(extension):
            if filename not in files_dict:
                files_dict[filename] = 0
                logger.info(f"File named {filename} was created.")
            search_for_magic(f"{path}{filename}",
                             files_dict[filename], magic_string)
    check_removed(path)


def check_removed(path):
    file_list = []

    for filename in files_dict:
        if filename not in os.listdir(path):
            file_list.append(filename)

    for filename in file_list:
        del files_dict[filename]
        logger.info(f"File {filename} was deleted.")


def create_parser():
    """Create arg parser"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--ext', default=".txt",
                        help="Searches files with given extension")
    parser.add_argument('--int', default=1,
                        help="Searches dir every given interval")
    parser.add_argument('dir', help="Monitors given directory named")
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
    start_time = datetime.datetime.now()
    logger.info(f"Current start time to process is: {start_time}")
    while not exit_flag:
        try:
            if not ns.dir:
                logger.error(
                    f"{datetime.datetime.now()}: No directory given to watch.")
            else:
                watch_directory(f"{ns.dir}/", ns.magic, ns.ext)
        except Exception as e:
            # This is an UNHANDLED exception
            # Log an ERROR level message here
            logger.error(f"{datetime.datetime.now()}: {e}")

        # put a sleep inside my while loop so I don't peg the cpu usage at 100%
        time.sleep(int(ns.int))

    end_time = datetime.datetime.now()
    duration = end_time - start_time
    logger.info(
        f"{datetime.datetime.now()}: Process took duration: {duration}")

    # final exit point happens here
    # Log a message that we are shutting down
    # Include the overall uptime since program start


if __name__ == '__main__':
    main(sys.argv[1:])
