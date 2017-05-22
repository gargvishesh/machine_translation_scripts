__author__ = 'spec'

import sys
import getopt
import utilities
import io
import textract
import os

dir_path_demarker = ""

def remove_page_number(infile, indir, outdir, language):
    if not indir == None:
        infile_path = indir + dir_path_demarker + infile
    else:
        infile_path = infile
    fin = io.open(infile_path, "r")
    outfile_path = outdir + dir_path_demarker + infile + '.out'
    fout = io.open(outfile_path, "w")
    for line in fin:
        pos = line.find("Babuji")
        if pos != -1:
            if (line.rstrip())[-1] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                fout.write(u"Babuji\n")
                continue
            else:
                print ("Rightmost char: " + (line.rstrip())[-1])
        fout.write(line)

def extract_from_pdf(infile, indir, outdir, language):
    if not indir == None:
        infile_path = indir + dir_path_demarker + infile
    else:
        infile_path = infile
    #fin = io.open(infile_path, "r")
    outfile = infile + '.raw.txt'

    if not outdir == None:
        outfile_path = outdir + dir_path_demarker + outfile
    elif not indir == None:
        outfile_path = indir + dir_path_demarker + outfile
    else:
        outfile_path = outfile

    fout = io.open(outfile_path, "wb")

    text = textract.process(infile_path)

    fout.write(text)


def combine_paragraph(infile, indir, outdir, language):

    print ("Input file:", infile)
    print ("Language:", language)

    if language != "tamil" and language != "hindi":
        sys.stderr.write("Language not supported\n")
        exit(1)

    if not indir == None:
        infile_path = indir + dir_path_demarker + infile
    else:
        infile_path = infile
    fin = io.open(infile_path, "r")
    outfile_path = outdir + dir_path_demarker + infile + '.out'
    fout = io.open(outfile_path, "w")
    accumulated = ""
    ignore_lines_count = 0
    for line in fin:
        if ignore_lines_count > 0:
            ignore_lines_count -= 1
            continue
        if line.find("IE-Section") != -1:
            #General pattern is
            # IE...
            #
            #11/21/2014   7:55:39 PM
            #
            ignore_lines_count = 3
            continue

        fout.write(line)
        '''if line.rstrip() == "":
            fout.write(accumulated + u'\n')
            fout.write(u'\n')
            accumulated = ""
        else:
            accumulated = accumulated + line.rstrip('\n')
            print "Accumulate Now: ", accumulated'''



def do_some_operation(infile, indir, outdir, language):

    # In batch mode, the input file consists of a newline separated list of file names containing the source text
    if indir:
        print ("**********************")
        print ("Directory Mode Enabled")
        print ("**********************")


    filenames = []
    output_filenames = []

    if indir:
        filenames = utilities.get_files_in_dir(indir)
    else:
        filenames.append(infile)

    for filename in filenames:
        #YOUR CUSTOM FUNCTION COMES HERE
        extract_from_pdf(filename, indir, outdir, language)

def print_usage(binary_name):
    print ("Usage:", binary_name, "--infile=<inputfile> --indir=<input dir> --outdir=<output dir> -l=<hindi/tamil>")
    print ("--infile: Take just a given file for processing")
    print ("--indir: Take all files in the dir for processing ")
    print ("--outdir: Puts all generated files in the output dir. Default is the same as the input path")
    sys.exit(2)


def main(binary_name, argv):
    infile = None
    indir = None
    outdir = None

    global language
    global dir_path_demarker

    if len(argv) == 0:
        print_usage(binary_name)

    try:
        # Used to get command line options for the script. ":" means arg also expected.
        opts, args = getopt.getopt(argv, "hl:", ["help", "infile=", "indir=",
                                                 "outdir="])
    except getopt.GetoptError:
        print ("Cannot parse arguments. Re-check flags")
        print_usage(binary_name)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_usage(binary_name)
        elif opt == "--infile":
            infile = arg
        elif opt == "-l":
            language = arg
        elif opt == "--indir":
            indir = arg
        elif opt == "--outdir":
            outdir = arg

    if infile is None and indir is None:
        print ("Input file / Dir not specified")
        print_usage(binary_name)
    elif language is None:
        print ("Language not specified")
        print_usage(binary_name)

    if os.name == 'nt':
        dir_path_demarker = '\\'
    else:
        dir_path_demarker='/'
    
    
    print ("Input file:", infile)
    print ("Input Dir:", indir)
    print ("Output Dir:", outdir)
    print ("Language:", language)

    do_some_operation(infile, indir, outdir, language)


if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
