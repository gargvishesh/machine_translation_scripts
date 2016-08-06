"""
Align 2 files sentence-wise using Moses translator.

Given 2 files in different languages, and Moses tool trained to do
a cursory translation between them, the module prepares those files
into a new pair of files that is sentence-aligned. These generated files
can be used as input to Moses for another round of training.
"""
import sys
import os
import getopt

import utilities
import constants
import split_file_into_sentences

__author__ = 'spec'

MOSES_PATH='/home/spec/machine_translation/mosesdecoder/bin/moses'
TRAINED_MODEL_PATH='/home/spec/machine_translation/trained_models/fr_en_whispers/train/model/moses.ini'


def auto_align(fin1, fin2, fout1, fout2, lang2):
    """
    Auto aligns a pair of files

    Uses the current translation system to translate a non-english file to english.
    Then does word to word comparison between selected lines of english file to
    find best-matching line for alignment and outputs the pair to a second set of
    files.

    :param fin1:
    :param fin2:
    :param fout1:
    :param fout2:
    :param lang2:
    :return:
    """
    for line in fin2:
        line.rstrip('\n')

        command1 ='echo "' + line + '"'
        exitcode, out, err = utilities.get_exitcode_stdout_stderr(command1)

        command2 = MOSES_PATH + ' -f ' + TRAINED_MODEL_PATH + out

        exitcode, out, err = utilities.get_exitcode_stdout_stderr(command2)
        #print "Running Command: ", command
        os.system(command1)

        print "Command Output: ", out


def prepare_files_and_auto_align(infile, lang1, lang2, batch_mode):
    """
    Prepare input and output files before initiating core function. Assumes
    lang1 is ALWAYS ENGLISH.

    :param infile: input file
    :param language: language of input file
    :param batch_mode: flag to indicate mode
    :return:NONE
    """

    for filename in utilities.get_input_files(infile, batch_mode):

        infile1 = filename + "." + lang1
        infile2 = filename + "." + lang2

        fin1 = utilities.open_file(infile1, 'r')
        fin2 = utilities.open_file(infile2, 'r')

        tempfile1 = infile1 + ".split"
        tempfile2 = infile2 + ".split"

        f_temp_out1 = utilities.open_file(tempfile1, 'w')
        f_temp_out2 = utilities.open_file(tempfile2, 'w')

        split_file_into_sentences.one_sentence_per_line(fin1, f_temp_out1, lang1)
        split_file_into_sentences.one_sentence_per_line(fin2, f_temp_out2, lang2)

        fin1.close()
        fin2.close()
        f_temp_out1.close()
        f_temp_out2.close()

        f_temp_in1 = utilities.open_file(tempfile1, 'r')
        f_temp_in2 = utilities.open_file(tempfile2, 'r')

        outfile1 = infile1 + ".aligned"
        outfile2 = infile2 + ".aligned"

        fout1 = utilities.open_file(outfile1, 'w')
        fout2 = utilities.open_file(outfile2, 'w')

        auto_align(f_temp_in1, f_temp_in2, fout1, fout2, lang2)
        #print("Aligned lines successfully written to " + outfile)

        f_temp_in1.close()
        f_temp_in2.close()
        fout1.close()
        fout2.close()


def print_usage(binary_name):
    print ('Usage: ', binary_name, "-b(batch-mode) --ifile=<inputfile> "
                                   "--l1=<lang1(fr/en/hi/ta)> --l2=lang2 ")
    sys.exit(2)


def main(binary_name, argv):
    infile = ''
    lang1 = ''
    lang2 = ''

    batch_mode = False
    if len(argv) == 0:
        print_usage(binary_name)

    try:
        # Used to get command line options for the script. ":" means arg also expected.
        opts, args = getopt.getopt(argv, "hbi:", ["help", "batch", "infile=", "l1=", "l2="])
    except getopt.GetoptError:
        print_usage(binary_name)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_usage(binary_name)
        elif opt in ("-i", "--infile"):
            infile = arg
        elif opt == "--l1":
            lang1 = arg
        elif opt == "--l2":
            lang2 = arg
        elif opt in ("-b", "--batch"):
            batch_mode = True

    if infile == '':
        print "Input file not specified"
        print_usage(binary_name)
    elif lang1 == '' or lang2 == '':
        print "Languages not specified"
        print_usage(binary_name)

    print 'Input file', infile
    print 'Language 1:', lang1
    print 'Language 2:', lang2

    if lang1.lower() != constants.LANG_ENGLISH:
        if lang2.lower() != "en":
            print "Atleast one input language must be English"
            sys.exit()
        else:
            (lang1, lang2) = utilities.swap(lang1, lang2)

    prepare_files_and_auto_align(infile, lang1, lang2, batch_mode)

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])