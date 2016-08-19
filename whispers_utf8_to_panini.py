#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Extract a TMX corpus comprising of 2 languages to 2 separate sentence-aligned
files. This is geared towards preparing the corpus for Moses training input.
To conform to sentence alignment, it discards sentences in one language
when the counterpart in the other language is empty in the TMX file. Note
that it assumes a tag structure of a TMX file as <tuv><seg></seg></tuv>
"""
from numpy.ctypeslib import _num_fromflags

import sys
import getopt
import io
import utilities
import csv

__author__ = 'spec'


def get_month(line):
    months_list = {u"जनवरी":'01', u"फरवरी":'02', u"मार्च":'03', u"अप्रैल":'04', u'अप्रेल':'04', u"मई":'05', u"जून":'06', u"जुलाई":'07',
                   u"अगस्त":'08', u"सितम्बर":'09', u"अक्टूबर":'10', u"नवम्बर":'11', u"दिसम्बर":'12'}
    month_index = 0

    for month in months_list.keys():
        pos = line.find(month)
        if pos != -1:
            return months_list[month], pos
        month_index += 1

    # Indicate month not found by this pair.
    return "00", -1


def get_day(line):
    words = line.split()
    print words
    if len(words) > 0:
        day = words[-1]
        #print "Len(day)", len(day)
        if len(day) > 0:
            if day[0] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                if len(day) < 2:
                    day = "0" + day
                return day
    return "00"


def get_year(line):
    words = line.split()
    if (len(words) > 1):
        year = words[1]
        return year
    return "0000"



def get_time(line):
    time = "0000"
    # Conversion to 24-hours timezone
    add_12 = False
    pos = line.find(u'प्रात:')
    if pos == -1:
        add_12 = True
        pos = line.find(u'रात्रि')
        if pos == -1:
            return "0000"
    # Time itself is generally mentioned after the prataha and ratri keywords
    words = line[pos:].split()
    time = words[1]
    if add_12:
        # Handle 9 or 10
        if len(time) == 1 or len(time) == 2:
            hours = int(time)
            hours += 12
            time = str(hours) + "00"
        # Handle 9:30
        elif len(time) == 4:
            hours = int(time[0])
            hours += 12
            time = str(hours) + time[2:]
        # Handle 10:30
        elif len(time) == 5:
            hours = int(time[:2])
            hours += 12
            time = str(hours) + time[3:]
    else:
        time = time.replace(":","")

    print "Time: ", time
    return time


def get_author(line):
    author_list_hindi =[u'बाबूजी', u'लालाजी']
    author_list_english = ['Babuji', 'Lalaji']
    for i in range(0, len(author_list_hindi)):
        if line.find(author_list_hindi[i]) != -1:
            return author_list_english[i]
    return ""


def separate_combined_whispers_to_separate_files(fin, csv_writer):
    line_no = 0
    message_beg_flag = False
    year = "0000"
    month = "00"
    time = "0000"
    author = ""
    whisper_start_line = 0
    whisper_end_line = 0

    lines = fin.readlines()
    num_lines = len(lines)
    print "num_lines ", num_lines

    while line_no < num_lines:
        line = lines[line_no]
        print "At line ", line_no

        if lines[line_no].find(u'प्रिय मालिक') != -1:
            message_beg_flag = True
            if(line_no > 0):
                # Finish writing out the previous whisper to a file
                author = get_author(lines[line_no-1])
                timestamp = year + month + day + time
                filename = timestamp + u'-hi.txt'
                fout_whisper = io.open(filename, 'w', encoding='utf8')
                for whisper_line in range (whisper_start_line, line_no):
                    fout_whisper.write(lines[whisper_line] + '\n')
                fout_whisper.close()
                csv_writer.writerow([unicode(filename), unicode(timestamp), u'hi', unicode(author), u'1'])
                print author
            line_no += 2
            # Also close the prev whispers message here.
            continue

        if message_beg_flag:
            message_beg_flag = False
            whisper_start_line = line_no
            month, month_pos = get_month(lines[line_no])
            if month_pos != -1:
                day = get_day(lines[line_no][:month_pos])
                year = get_year(lines[line_no][month_pos:])
                time = get_time(lines[line_no])
            print "Day:%s Month:%s Year:%s" %(day, month, year)

        line_no += 1


def restore_hindi_whispers_chars_and_formatting(fin, fout):
    combine_mode_quotes = False
    combine_mode_bracket = False

    for line in fin:

        # Should read http://nedbatchelder.com/text/unipain.html to understand this further.
        # Basically - Encode: Unicode -> Bytes, Decode: Bytes -> Unicode

        line = line.encode('utf-8')

        # These characters have faulty conversion when converted using font-converter (font: shree-dev-0702)

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
        # or (.
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
        # assume each char to be of 4 byte when working with pure Unicode.

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

    if language != "tamil" and language != "hindi":
        sys.stderr.write("Language not supported\n")
        exit(1)

    for filename in utilities.get_input_files(infile, batch_mode):

        print "Processing file", filename
        outfile_conversion = filename + ".converted"

        print "Writing output to %s" % (outfile_conversion)

        # encoding='utf8' is necessary because file is opened in ascii by default, which throws error when trying to
        # write a non-ascii character

        fin = io.open(filename, 'r', encoding='utf8')
        fout_conversion = io.open(outfile_conversion, 'w', encoding='utf8')

        if language == 'hindi':
            restore_hindi_whispers_chars_and_formatting(fin, fout_conversion)
        #else:
            #convert_tamil_whispers_to_panini(fin, fout)

        fin.close()
        fout_conversion.close()
        outfile_csv = 'whispers.' + language + '.csv'

        fin = io.open(outfile_conversion, 'r', encoding='utf8')
        fout_csv = io.open(outfile_csv, 'ab')

        # Lifted from http://stackoverflow.com/questions/2084069/create-a-csv-file-with-values-from-a-python-list
        csv_writer = csv.writer(fout_csv, quoting=csv.QUOTE_ALL)
        separate_combined_whispers_to_separate_files(fin, csv_writer)

        fin.close()
        fout_csv.close()




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
