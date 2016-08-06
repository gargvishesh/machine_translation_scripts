#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'vishesh'

import os, sys
import getopt

def open_file(filename, args):
   try:
      f = open(filename, args)
   except:
      str= "Cannot open file: " + filename + "\n"
      sys.stderr.write(str)
      exit(1)
   return f


def clean_function(fin, fout, lines_beg, lines_end, remove_chars_list):
    lines = fin.readlines()
    num_lines = len(lines)
    first_index = lines_beg
    if(num_lines > lines_end):
        last_index_plus_one = num_lines - lines_end
    else:
        last_index_plus_one = first_index

    #lines[0,n] is equivalent to line[0] to line[n-1]. Also lines[0,-k] = lines[0, n-k]
    for surviving_line in lines[first_index:last_index_plus_one]:
        for removal_char in remove_chars_list:
            surviving_line = surviving_line.replace(removal_char,"")
        if surviving_line:
            fout.write (surviving_line)

def clean_file(infile, lines_beg, lines_end, remove_chars_list, batch_mode):
    # In batch mode, the input file consists of a newline separated list of file names containing the source text
    if (batch_mode == True):
        print "******************"
        print "Batch Mode Enabled"
        print "******************"

    print 'Input file:', infile
    print '#Lines to be stripped from beginning:', lines_beg
    print '#Lines to be stripped from end:', lines_end
    print 'List of chars to be removed:', remove_chars_list

    if(batch_mode == True):
        fin_batch = open_file(infile, 'r')
        for filename in fin_batch:
            filename = filename.rstrip('\n')
            fin = open_file(filename, 'r')
            outfile = filename + ".clean"
            fout = open_file(outfile, 'w')
            clean_function(fin, fout, lines_beg, lines_end, remove_chars_list)
            print("Cleaned lines successfully written to " + outfile)
            fin.close()
            fout.close()
        fin_batch.close()

    else:
        fin = open_file(infile, 'r')
        outfile = infile + ".clean"
        fout = open_file(outfile, 'w')
        clean_function(fin, fout, lines_beg, lines_end, remove_chars_list)
        print("Cleaned lines successfully written to " + outfile)
        fout.close()
        fin.close()


def print_usage(binary_name):
    print 'Usage: ', binary_name, '\n-b (batch-mode) \n' \
                                  '-i <inputfile> (In batch-mode, input file should contain a newline separated list of file names)\n' \
                                  '--linescountbeg <#lines to be stripped from beg> \n' \
                                  '--linescountend <#lines to be stripped from end> \n' \
                                  '--chars <Space separated list of chars inside [], eg. --chars ^,@>'
    sys.exit(2)

def main(binary_name, argv):
    infile = ''
    batch_mode = 'false'
    remove_chars_list = []
    lines_beg = 0
    lines_end = 0

    if len(argv) == 0:
        print_usage(binary_name)

    try:
        # Used to get command line options for the script. ":" and "=" mean arg is also expected.
        opts, args = getopt.getopt(argv,"hbi:",["help", "batch", "ifile=", "linescountbeg=", "linescountend=", "chars="])
    except getopt.GetoptError:
        print ("Unrecognized command line option entered")
        print_usage(binary_name)

    for opt, arg in opts:
        if opt in ( "-h", "--help"):
            print_usage(binary_name)
        elif opt in ("-i", "--ifile"):
            infile = arg
        elif opt == "--linescountbeg":
            lines_beg = int(arg)
        elif opt == "--linescountend":
            lines_end = int(arg)
        elif opt in ("-b", "--batch"):
            batch_mode = True;
        elif opt == "--chars":
            remove_chars_list = arg.split(",")


    if (infile == ''):
        print "Input file not specified"
        print_usage(binary_name)

    clean_file(infile, lines_beg, lines_end, remove_chars_list, batch_mode)

if __name__ == "__main__":
   main(sys.argv[0], sys.argv[1:])
