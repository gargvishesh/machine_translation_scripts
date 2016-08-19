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

__author__ = 'spec'


def convert_hindi_whispers_to_panini(fin, fout):
    combine_mode_quotes = False
    combine_mode_bracket = False

    for line in fin:

        # Should read http://nedbatchelder.com/text/unipain.html to understand this further.
        # Basically - Encode: Unicode -> Bytes, Decode: Bytes -> Unicode

        line = line.encode('utf-8')

        line = line.replace('ङ्क', 'म')
        line = line.replace('ङ्म', 'य')
        line = line.replace('μज', 'ज़')
        line = line.replace('ङ्ग', '“')
        line = line.replace('ङ्घ', '”')
        line = line.replace('ङ्ख', 'फ')
        line = line.replace('μफ', 'फ़')
        line = line.replace('०', '0')
        line = line.replace('१', '1')
        line = line.replace('२', '2')
        line = line.replace('३', '3')
        line = line.replace('४', '4')
        line = line.replace('५', '5')
        line = line.replace('६', '6')
        line = line.replace('७', '7')
        line = line.replace('८', '8')
        line = line.replace('९', '9')
        line = line.replace('μक', 'क़')

        # The whispers copied from PDF have newline after each line appearing in the PDF.
        # We therefore have to combine multiple lines in a single line by observing opening "
        # and sometimes using a bracket.
        print line[0], line[-2]

        if line[0] == '(':
            combine_mode_bracket = True
            print "Combine mode bracket start"
        if line.find('“') == 0:
            combine_mode_quotes = True
            print "Combine mode quotes start"

        # [-1] would be '\n'
        if line[-2] == ')':
            combine_mode_bracket = False
            print "Combine mode bracket end"

        # Used hit-and-trial (aka printfs) to determine where does a closed brace appear in unicode!
        # This is because in there, the characters are no longer 1-byte.In fact, I think we can safely
        # assume each char to be of 4 byte when working with pure Unicode

        if line.find('”') == len(line) -4:
            combine_mode_quotes = False
            print "Combine mode quotes end"

        if combine_mode_quotes == True or combine_mode_bracket == True:
            line = line.rstrip('\n')

        fout.write(line.decode("utf-8"))

        # line = line.replace( '६' , '6' )

#def convert_tamil_whispers_to_panini(fin, fout):


def process_conversion_to_panini(infile, language, batch_mode):
    # In batch mode, the input file consists of a newline separated list of file names containing the source text
    if (batch_mode == True):
        print "******************"
        print "Batch Mode Enabled"
        print "******************"

    print 'Input file:', infile
    print 'Language:', language

    if (language != "tamil" and language != "hindi"):
        sys.stderr.write("Language not supported\n")
        exit(1)

    for filename in utilities.get_input_files(infile, batch_mode):

        print "Processing file", filename
        outfile = filename + ".panini"

        print "Writing output to %s" % (outfile)

        # encoding='utf8' is necessary because file is opened in ascii by default, which throws error when trying to
        # write a non-ascii character

        fin = io.open(filename, 'r', encoding='utf8')
        fout = io.open(outfile, 'w', encoding='utf8')

        if(language == 'hindi'):
            convert_hindi_whispers_to_panini(fin, fout)
        #else:
            #convert_tamil_whispers_to_panini(fin, fout)

        fin.close()
        fout.close()


def print_usage(binary_name):
    print 'Usage:', binary_name, "-b(batch-mode) --infile=<inputfile> -l=<hindi/tamil>"
    sys.exit(2)


def main(binary_name, argv):
    infile = ''
    language = ''

    batch_mode = False
    if len(argv) == 0:
        print_usage(binary_name)

    try:
        # Used to get command line options for the script. ":" means arg also expected.
        opts, args = getopt.getopt(argv, "hbi:l:", ["help", "batch", "infile="])
    except getopt.GetoptError:
        print "Cannot parse arguments. Re-check flags"
        print_usage(binary_name)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_usage(binary_name)
        elif opt in ("-i", "--infile"):
            infile = arg
        elif opt == "-l":
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

    process_conversion_to_panini(infile, language, batch_mode)


if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
