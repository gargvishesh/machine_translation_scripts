#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'vishesh'

import os, sys
import getopt
import utilities

def alignment_function(fin_left, fin_right, fout_left, fout_right):
    lines_left = fin_left.readlines()
    num_lines_left = len(lines_left)
    lines_right = fin_right.readlines()
    num_lines_right = len(lines_right)

    if num_lines_left != num_lines_right:
        return False

    for line in lines_left:
        fout_left.write(line)
    for line in lines_right:
        fout_right.write(line)

    return True

def process_alignment(infile, outfile_left, outfile_right, ext1, ext2, batch_mode):
    if (batch_mode == True):
        print "******************"
        print "Batch Mode Enabled"
        print "******************"

    print 'Input file:', infile
    print 'Output file left:', outfile_left
    print 'Output file right:', outfile_right

    fout_left = utilities.open_file(outfile_left, 'w')
    fout_right = utilities.open_file(outfile_right, 'w')

    if(batch_mode == True):
        fin_batch = utilities.open_file(infile, 'r')
        for filename in fin_batch:
            filename = filename.rstrip('\n')
            filename_left = filename + ext1
            filename_right = filename + ext2
            fin_left = utilities.open_file(filename_left, 'r')
            fin_right = utilities.open_file(filename_right, 'r')
            ret = alignment_function(fin_left, fin_right, fout_left, fout_right)
            if ret == False:
                print ("Skipping files: " + filename_left +", " + filename_right)
            fin_left.close()
            fin_right.close()
        fin_batch.close()

    else:
        filename_left = infile + ext1
        filename_right = infile + ext2
        fin_left = utilities.open_file(filename_left, 'r')
        fin_right = utilities.open_file(filename_right, 'r')
        ret = alignment_function(fin_left, fin_right, fout_left, fout_right)
        if ret == False:
            print ("Skipping files: " + filename_left +", " + filename_right)
        fin_left.close()
        fin_right.close()

    print("Aligned text written to files: " + outfile_left + ", " + outfile_right)

    fout_left.close()
    fout_right.close()


def print_usage(binary_name):
   print 'Usage: ', binary_name, '-b(batch-mode) -i <input file> --oleft <output file left> --oright <output file right>' \
                                 '--ext1 <extension of left file> --ext2 <extension of right file>'
   sys.exit(2)




def main(binary_name, argv):
    infile = ''
    outfile_left = ''
    outfile_right = ''
    language = ''
    ext1 = ''
    ext2 = ''
    batch_mode = 'false'
    if len(argv) == 0:
        print_usage(binary_name)

    try:
        # Used to get command line options for the script. ":" means arg also expected.
        opts, args = getopt.getopt(argv,"hbi:",["help", "batch", "ifile=", "ext1=", "ext2=", "oleft=", "oright="])
    except getopt.GetoptError:
        print_usage(binary_name)

    for opt, arg in opts:
        if opt in ( "-h", "--help"):
            print_usage(binary_name)
        elif opt in ("-i", "--ifile"):
            infile = arg
        elif opt == "--oleft":
            outfile_left = arg
        elif opt == "--oright":
            outfile_right = arg
        elif opt in ("-b", "--batch"):
            batch_mode = True;
        elif opt == "--ext1":
            ext1 = arg;
        elif opt == "--ext2":
            ext2 = arg;

    if (infile == ''):
        print "Input file not specified"
        print_usage(binary_name)
    elif (outfile_left == ''):
        print "Output file left not specified"
        print_usage(binary_name)
    elif (outfile_right == ''):
        print "Output file right not specified"
        print_usage(binary_name)
    elif (ext1 == ''):
        print "Extension 1 not specified"
        print_usage(binary_name)
    elif (ext2 == ''):
        print "Extension 2 not specified"
        print_usage(binary_name)

    process_alignment(infile, outfile_left, outfile_right, ext1, ext2, batch_mode)

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
