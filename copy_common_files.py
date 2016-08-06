#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Copy files with same names (but different extensions) from 2 separate folders to a third folder.
Useful to filter out the files in one language which have a counterpart in another language - such
as in the context of Whispers messages, because not all French whispers might have an English translation
file and vice-versa. The program takes 2 directories as input and writes out the "common files" to a
specified output directory.
"""

import sys
import getopt
import os
from os import walk

__author__ = 'spec'


mypath = "."

def copy_common_files(indir1, indir2, outdir, lang1, lang2, action):

    if action == "copy":
        action_cmd = "cp"
    else:
        action_cmd = "mv"

    for (dirpath1, dirnames1, filenames1) in walk(indir1):
        print dirpath1

        for (dirpath2, dirnames2, filenames2) in walk(indir2):
            for filename_lang2 in filenames2:
                if filename_lang2.endswith(lang2):

                    filename_wo_extension = filename_lang2[:-(len(lang2))]
                    filename_lang1 = filename_wo_extension + lang1

                    if filename_lang1 in filenames1:
                        command = action_cmd + " " + dirpath1 + "/" + filename_lang1 + " " + outdir
                        print command
                        os.system(command)
                        #print "Common file", filename_wo_extension


def print_usage(binary_name):
    print 'Usage: ', binary_name, "-b(batch-mode) --indir1=<input dir 1> "
    "--indir2=<input dir 2> --outdir=<output dir> --l1=<language1> "
    "--l2=<language2> --action=<move/copy>"
    print 'Note that l1 and l2 are only used for the extensions of the output file'
    sys.exit(2)

def main(binary_name, argv):
    indir1 = ''
    indir2 = ''
    outdir = ''
    lang1 = ''
    lang2 = ''
    action = ''

    batch_mode = False
    if len(argv) == 0:
        print_usage(binary_name)

    try:
        # Used to get command line options for the script. ":" means arg also expected.
        opts, args = getopt.getopt(argv, "hb", ["help", "batch", "indir1=", "indir2=",
                                                "outdir=", "l1=", "l2=", "action="])
    except getopt.GetoptError:
        print "Cannot parse arguments. Re-check flags"
        print_usage(binary_name)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_usage(binary_name)
        elif opt in ("--indir1"):
            indir1 = arg
        elif opt in ("--indir2"):
            indir2 = arg
        elif opt in ("--outdir"):
            outdir = arg
        elif opt == "--l1":
            lang1 = arg
        elif opt == "--l2":
            lang2 = arg
        elif opt == "--action":
            action = arg

    if (indir1 == '' or indir2 ==''):
        print "Input directories not specified"
        print_usage(binary_name)
    if (outdir == ''):
        print "Output directory not specified"
        print_usage(binary_name)
    if lang1 == '' or lang2 == '':
        print "Languages not specified"
        print_usage(binary_name)
    if action != "move" and action != "copy":
        print "Invalid action specified"
        print_usage(binary_name)

    print 'Input Dir 1:', indir1
    print 'Input Dir 2:', indir2
    print 'Output Dir:', outdir
    print 'Language 1:', lang1
    print 'Language 2:', lang2
    print 'Action:', action

    copy_common_files(indir1, indir2, outdir, lang1, lang2, action)

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])