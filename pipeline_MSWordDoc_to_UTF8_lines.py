#!/usr/bin/python
# -*- coding: utf-8 -*-

"""The pipeline combines 3 phases for a SINGLE whisper:

1) convert - convert from custom font encoding to UTF-8 for readability
2) clean - remove stray characters as well chop off unnecessary header and footer lines, all specified as commandline params
3) split - split paragraphs into newline separated sentences, the delimiter being specified in the command line

 Each of these phases is optional to be executed which can again be specified on the command line. """

import sys
import getopt
import cleanup_text
import split_file_into_sentences
import utf8_converter
import utilities

CONVERT = "convert"
CLEAN = "clean"
SPLIT = "split"

__author__ = 'vishesh'


def process_function(fin, fout, pipeline, language, lines_beg, lines_end, remove_chars_list):
    for task in pipeline:
        if task == CONVERT:
            f_utf8_write = utilities.open_file("/tmp/utf8_converted", 'w')
            utf8_converter.utf8_conversion_function(fin, f_utf8_write, language)
            f_utf8_write.close()
            fin.close()
            fin = utilities.open_file("/tmp/utf8_converted", 'r')

        elif task == CLEAN:
            f_cleaned_write = utilities.open_file("/tmp/cleaned", 'w')
            cleanup_text.clean_function(fin, f_cleaned_write, lines_beg, lines_end, remove_chars_list)
            f_cleaned_write.close()
            fin.close()
            fin = utilities.open_file("/tmp/cleaned", 'r')

        elif task == SPLIT:
            f_split = utilities.open_file("/tmp/split", 'w')
            split_file_into_sentences.one_sentence_per_line(fin, f_split, language)
            f_split.close()
            fin.close()
            fin = utilities.open_file("/tmp/split", 'r')

        else:
            print "FATAL ERROR: Invalid Task in Pipeline"
            exit(1)

    for line in fin.readlines():
        fout.write(line)


def prepare_io_files_and_process(infile, language, do_convert, do_clean, do_split, lines_beg, lines_end, remove_chars_list, batch_mode):
    if batch_mode:
        print "******************"
        print "Batch Mode Enabled"
        print "******************"

    print 'Input file:', infile

    if language not in ["tamil", "hindi", "english", "french"]:
        sys.stderr.write("ERROR Unsupported Language: " + language + "\n")
        exit(1)

    print 'Language:', language

    pipeline = []

    # **NOTE: These operations are ORDERED. Take care while inserting a new one.

    if do_convert:
        pipeline.append(CONVERT)

    if do_clean:
        pipeline.append(CLEAN)
        print '#Lines to be stripped from beginning:', lines_beg
        print '#Lines to be stripped from end:', lines_end
        print 'List of chars to be removed:', remove_chars_list

    if do_split:
        pipeline.append(SPLIT)

    print "Text going through following pipeline:", pipeline

    for filename in utilities.get_input_files(infile, batch_mode):
        fin = utilities.open_file(filename, 'r')
        print("Processing file: " + filename)
        outfile = filename + ".final"
        fout = utilities.open_file(outfile, 'w')
        process_function(fin, fout, pipeline, language, lines_beg, lines_end, remove_chars_list)
        print("Processed text successfully written to file: " + outfile)
        fin.close()
        fout.close()

def print_usage(binary_name):
    print("Usage: " + binary_name)
    

def main(binary_name, argv):


    try:
        # Used to get command line options for the script. ":" and "=" mean arg is also expected.
        opts, args = getopt.getopt(argv, "hbi:l:", ["convert", "clean", "split", "help", "batch", "ifile=", "beg=", "end=", "chars="])
    except getopt.GetoptError:
        print ("Unrecognized command line option entered")
        print_usage(binary_name)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_usage(binary_name)
        elif opt in ("-i", "--ifile"):
            infile = arg
        elif opt == "--beg":
            lines_beg = int(arg)
        elif opt == "--end":
            lines_end = int(arg)
        elif opt in ("-b", "--batch"):
            batch_mode = True
        elif opt == "--chars":
            remove_chars_list = arg.split(",")
        elif opt in ("-l", "--language"):
            language = arg.lower()
        elif opt == "--convert":
            do_convert = True
        elif opt == "--clean":
            do_clean = True
        elif opt == "--split":
            do_split = True

    if infile == '':
        print "Input file not specified"
        print_usage(binary_name)
    elif language == '':
        print "Language not specified"
        print_usage(binary_name)

    prepare_io_files_and_process(infile, language, do_convert, do_clean, do_split, lines_beg, lines_end, remove_chars_list, batch_mode)

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
