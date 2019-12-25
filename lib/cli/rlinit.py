#!/usr/bin/python3

"""
readline init script
"""

import atexit
import os
import readline
import sys

from lib.cli.cmd import COMMANDS

from . import colors


COMMAND_LIST = list(COMMANDS.keys())


def readline_init():
    """
    init readline settings
    """

    command_list = COMMAND_LIST
    command_list += ["webshell", "/tmp/", "inurl:"]

    hist_file = os.path.join(os.path.expanduser("~"), ".python_history")

    if not os.path.exists(hist_file):
        os.system('touch {}'.format(hist_file))
    with open(hist_file) as histf:
        for line in histf:
            for item in line.strip().split():
                command_list.append(item)

    # List ./data
    try:
        data_path = os.path.join(os.path.expanduser("~"), ".mec/data")

        for item in os.listdir(data_path):
            command_list.append(item)
    except FileNotFoundError:
        colors.colored_print("[-] Please run install.py first", colors.RED)
        sys.exit(1)

    readline.parse_and_bind("tab: complete")
    readline.set_completer(completer)

    try:
        readline.read_history_file(hist_file)
        # default history len is -1 (infinite), which may grow unruly
        readline.set_history_length(1000)
    except FileNotFoundError:
        pass

    atexit.register(readline.write_history_file, hist_file)


def completer(text, state):
    '''
    completer for readline, used in console
    '''
    options = [i for i in COMMAND_LIST if i.startswith(text)]

    if state < len(options):
        return options[state]

    return None