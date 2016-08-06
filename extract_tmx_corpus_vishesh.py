#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Extract a TMX corpus comprising of 2 languages to 2 separate sentence-aligned
files. This is geared towards preparing the corpus for Moses training input.
To conform to sentence alignment, it discards sentences in one language
when the counterpart in the other language is empty in the TMX file. Note
that it assumes a tag structure of a TMX file as <tuv><seg></seg></tuv>
"""

import sys
import getopt
import io
import utilities
import xml.dom.minidom

__author__ = 'spec'



def extract_corpus(infile, fout1, fout2):
    """
    Extract TMX corpus to 2 separate files - corresponding file ptrs given by fout1 and fout2.

    :param infile: input file
    :param fout1: first output file ptr
    :param fout2: second output file ptr
    :return:NONE
    """

    # Open XML document using minidom parser
    DOMTree = xml.dom.minidom.parse(infile)

    collection = DOMTree.documentElement

    # Vishesh: Leaving this part of code just for reference, to show that
    # we can use the attribute element to filter out stuff

    # if collection.hasAttribute("version"):
        #print "Root element : %s" % collection.getAttribute("version")

    # Get all the tuvs in the collection
    tuvs = collection.getElementsByTagName("tuv")

    tuv_index = 0
    tuv_lang1 = ""
    tuv_lang2 = ""

    for tuv in tuvs:
        segments = tuv.getElementsByTagName("seg")
        for seg in segments:
            if (seg.hasChildNodes()):
                if (tuv_index % 2) == 1:
                    tuv_lang1 = seg.childNodes[0].data
                else:
                    tuv_lang2 = seg.childNodes[0].data


        # After every odd-numbered element (starting from 0), we check if both lang sentences are non-empty.
        # If we do, we write them to corresponding files; else we discard them.

        if (tuv_index %2) == 1:
            if (tuv_lang1 != "" and tuv_lang2 != ""):
                #print "Writing" + tuv_lang2
                fout1.write(tuv_lang1+'\n')
                fout2.write(tuv_lang2+'\n')

            tuv_lang1 = ""
            tuv_lang2 = ""

        tuv_index = tuv_index + 1

def prepare_files_and_extract_corpus(infile, lang1, lang2, batch_mode):
    """
    Prepare input and output files before initiating core function.

    :param infile: input file
    :param lang1: first language
    :param lang2: second language
    :param batch_mode: flag to indicate mode
    :return:NONE
    """

    if (batch_mode == True):
        print "******************"
        print "Batch Mode Enabled"
        print "******************"

    for filename in utilities.get_input_files(infile, batch_mode):

        print "Processing file", filename
        outfile1 = filename + "." + lang1
        outfile2 = filename + "." + lang2

        print "Writing output to %s and %s" %(outfile1 , outfile2)

        #encoding='utf8' is necessary because file is opened in ascii by default, which throws error when trying to
        #write a non-ascii character

        fout1 = io.open(outfile1,'w',encoding='utf8')
        fout2 = io.open(outfile2,'w',encoding='utf8')

        extract_corpus(filename, fout1, fout2)

        fout1.close()
        fout2.close()

def print_usage(binary_name):
    print ('Usage: ', binary_name, "-b(batch-mode) --infile=<inputfile> "
                                   "--l1=<language1> --l2=<language2>")
    print('Note that l1 and l2 are only used for the extensions of the output file')
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
        print "Cannot parse arguments. Re-check flags"
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

    print 'Input file:', infile
    print 'Language 1:', lang1
    print 'Language 2:', lang2

    prepare_files_and_extract_corpus(infile, lang1, lang2, batch_mode)

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])