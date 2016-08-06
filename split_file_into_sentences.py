#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Splits a file into multiple lines - each line containing 1 sentence

The module takes a file/set of files as input and outputs a file/set of files
containing one sentence in each line. The delimiter for identifying the ending
of a sentence is determined by the specified language.
"""

import sys
import getopt
import utilities
import constants

__author__ = 'vishesh'

DELIMITERS_HINDI = ['।', '?']
DELIMITERS_TAMIL = ['.', '?']
DELIMITERS_TELUGU = ['.', '?']
DELIMITERS_ENGLISH = ['.', '?']


def one_sentence_per_line(fin, fout, language):
    """
    Splits a paragraph into multiple lines - each line containing 1 sentence

    :param fin: Input file
    :param fout: Output file
    :param language: Language to know sentence delimiter
    :return: None
    """
    if language == constants.LANG_TAMIL:
        delimiters = DELIMITERS_TAMIL
    elif language == constants.LANG_HINDI:
        delimiters = DELIMITERS_HINDI
    else:
        delimiters = DELIMITERS_ENGLISH

    for para in fin:

        """
        For each paragraph
        there can be multiple delimiters - ex !, . etc. Hence, we remove one
        \n that is already present at the end of the para
        and later replace each delimiter with delimiter + \n combination
        """
        para.rstrip('\n')  # Because I'm explicitly adding it afterwards for each line
        for delimiter in delimiters:
            para = para.replace(delimiter, delimiter+'\n')

        """Doing this splitting in a round-about manner because dont know a
        direct way of simultaneously splitting
        with multiple delimiters. Secondly, as each sentence begins with a
        space after the previous delimiter, an lstrip()
        is necessary before writing it.
        """
        for sentence in para.split('\n'):
            sentence = sentence.lstrip()
            if sentence == "":
                continue  # Skip blank lines.
            fout.write(sentence + '\n')


def prepare_files_and_split(infile, language, batch_mode):
    """
    Prepare input and output files before initiating core function

    :param infile: input file
    :param language: language of input file
    :param batch_mode: flag to indicate mode
    :return:NONE
    """
    if batch_mode:
        print "**********"
        print "Batch Mode"
        print "**********"

    for filename in utilities.get_input_files(infile, batch_mode):
        fin = utilities.open_file(filename, 'r')
        outfile = filename + ".split"
        fout = utilities.open_file(outfile, 'w')
        one_sentence_per_line(fin, fout, language)
        print("Split lines successfully written to " + outfile)
        fin.close()
        fout.close()


def print_usage(binary_name):
    print 'Usage: ', binary_name, '-b(batch-mode) -i <inputfile> -l <hi/ta>'
    sys.exit(2)


def main(binary_name, argv):
    infile = ''
    language = ''
    batch_mode = 'false'
    if len(argv) == 0:
        print_usage(binary_name)

    try:
        # Used to get command line options for the script. ":" means arg also expected.
        opts, args = getopt.getopt(argv, "hbi:l:", ["help", "batch", "ifile=", "language"])
    except getopt.GetoptError:
        print_usage(binary_name)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_usage(binary_name)
        elif opt in ("-i", "--ifile"):
            infile = arg
        elif opt in ("-l", "--language"):
            language = arg
        elif opt in ("-b", "--batch"):
            batch_mode = True

    if infile == '':
        print "Input file not specified"
        print_usage(binary_name)
    elif language == '':
        print "Language not specified"
        print_usage(binary_name)

    print 'Input file:', infile
    print 'Language:', language

    if language == constants.LANG_TAMIL:
        print "Delimiter: ", DELIMITERS_TAMIL
    elif language == constants.LANG_HINDI:
        print "Delimiter: ", DELIMITERS_HINDI
    else:
        sys.stderr.write("Language not supported\n")
        exit(1)

    prepare_files_and_split(infile, language, batch_mode)

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
