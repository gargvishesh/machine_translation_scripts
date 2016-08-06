__author__ = 'spec'

import os, sys
import getopt
import utilities

def spew_function(fin, filename):

    para_index = 1
    for para in fin:
        '''
        A line in this case is essentially a paragraph. Now for each paragraph there can be multiple
        delimiters - ex !, . etc. Hence, we replace one \n that is already present at the end of the para
        and later replace each delimiter with delimiter + \n combination
        '''
        if  para == "\n":
                continue #Skip blank lines.
        outfile = filename + ".para." + str(para_index)
        para_index += 1
        fout = utilities.open_file(outfile, 'w')
        fout.write(para)
        fout.close()
        print("Para successfully written to " + outfile)


def spew_paras(infile, batch_mode):
    # In batch mode, the input file consists of a newline separated list of file names containing the source text
    if (batch_mode == True):
        print "******************"
        print "Batch Mode Enabled"
        print "******************"

    print 'Input file:', infile

    fin = utilities.open_file(infile, 'r')

    if(batch_mode == True):
        fin_batch = utilities.open_file(infile, 'r')
        for filename in fin_batch:
            '''
            When we read linewise from file, even \n
            comes as a part of the name of the file!
            '''
            filename = filename.rstrip('\n')
            fin = utilities.open_file(filename, 'r')
            outfile = filename + ".split"
            #fout = utilities.open_file(outfile, 'w')
            spew_function(fin, filename);
            fin.close()
            #fout.close()
        fin_batch.close()

    else:
        fin = utilities.open_file(infile, 'r')
        spew_function(fin, infile);
        fin.close()

def print_usage(binary_name):
   print 'Usage: ', binary_name, '-b(batch-mode) -i <inputfile> -l <hindi/tamil>'
   sys.exit(2)

def main(binary_name, argv):
   infile = ''
   batch_mode = 'false'
   if len(argv) == 0:
      print_usage(binary_name)

   try:
      # Used to get command line options for the script. ":" means arg also expected.
      opts, args = getopt.getopt(argv,"hbi:",["help", "batch", "ifile="])
   except getopt.GetoptError:
      print_usage(binary_name)

   for opt, arg in opts:
      if opt in ( "-h", "--help"):
         print_usage(binary_name)
      elif opt in ("-i", "--ifile"):
         infile = arg
      elif opt in ("-b", "--batch"):
          batch_mode = True;

   if (infile == ''):
      print "Input file not specified"
      print_usage(binary_name)
   spew_paras(infile, batch_mode)

if __name__ == "__main__":
   main(sys.argv[0], sys.argv[1:])
