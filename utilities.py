"""
Common utility functions used across files

The file contains functions for tasks such as file handling.
"""

import sys
import shlex
from subprocess import Popen, PIPE
from os import walk

__author__ = 'spec'


def open_file(filename, mode):
    """
    Open a file in a given mode
    """
    try:
        f = open(filename, mode)
    except:
        error_string = "Cannot open file: " + filename + "\n"
        sys.stderr.write(error_string)
        exit(1)
    return f


def get_input_files(infile, batch_mode):
    """
    Return a list of files to be opened for input

    The function takes a text file as input, and depending on whether batch_mode is true/false,
    returns a list of file names contained in that file, or the file itself

    :return LIST[filenames]
    """
    filenames = []

    if batch_mode:
        fin_batch = open_file(infile, 'r')
        for filename in fin_batch:
            """
            When we read line-wise from file, even \n
            comes as a part of the name of the file!
            """
            filename = filename.rstrip('\n')
            filenames.append(filename)
        fin_batch.close()

    else:
        filenames.append(infile)

    return filenames


def get_files_in_dir(indir):
    """
    Return a list of files to be opened for input

    The function takes a text file as input, and depending on whether batch_mode is true/false,
    returns a list of file names contained in that file, or the file itself

    :return LIST[filenames]
    """

    for (dirpath, dirnames, filenames) in walk(indir):
        return filenames

def swap(x, y):
    """
    Swaps values of x and y and returns the swapped pair

    :param x:
    :param y:
    :return: (y,x)
    """
    temp = x
    x = y
    y = temp
    return x, y


def get_exitcode_stdout_stderr(cmd):
    """
    Execute the external command and get its exitcode, stdout and stderr.
    """
    args = shlex.split(cmd)

    proc = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    exitcode = proc.returncode
    #
    return exitcode, out, err

def is_blank_line(line):
    if len(line.rstrip('\n').rstrip('\r')) == 0:
        return True
    return False
