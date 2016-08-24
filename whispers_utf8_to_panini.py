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


def get_month_hindi(line):
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

def get_year_month_day_tamil(line):
    year = '0000'
    month ='00'
    day = '00'

    months_list = {u"ஜனவரி":'01', u"பிப்ரவரி":'02', u"மார்ச்":'03', u"ஏப்ரல்":'04', u"மே":'05', u"ஜூன்":'06', u"ஜூலை":'07',
                   u"ஆகஸ்ட்":'08', u"செப்டம்பர்":'09', u"அக்டோபர்":'10', u"நவம்பர்":'11', u"டிசம்பர்":'12'}

    for month_tamil in months_list.keys():
        pos = line.find(month_tamil)
        if pos != -1:
            # Get the list of all words after the month string
            month = months_list[month_tamil]
            post_month_words = line[pos:].replace(',','').split(' ')
            print 'post_month_words ',post_month_words
            if len (post_month_words) > 1 and post_month_words[1].isdigit():
                day = post_month_words[1]
                # Handle single digit such as 9
                if len(day) == 1:
                    day = '0' + day
            if len (post_month_words) > 2 and post_month_words[2].isdigit():
                year = post_month_words[2]

    return year, month, day


def get_day_hindi(line):
    words = line.split()
    #print words
    if len(words) > 0:
        day = words[-1]
        #print "Len(day)", len(day)
        if len(day) > 0:
            if day[0] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                if len(day) < 2:
                    day = "0" + day
                return day
    return "00"


def get_year_hindi(line):
    words = line.split()
    if (len(words) > 1):
        year = words[1]
        return year
    return "0000"



def get_time_hindi(line):
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

    time_components = time.split(':')
    hours_int = int(time_components[0])
    minutes_str = '00'
    if len(time_components) > 1:
        minutes_str = time_components[1]
    if add_12:
        hours_int += 12
    hours_str = str(hours_int)
    if len(hours_str) == 1:
        hours_str = '0' + hours_str
    return hours_str + minutes_str

def get_time_tamil(line):
    # Conversion to 24-hours timezone
    hours_str = '00'
    minutes_str = '00'
    print 'Header', line
    add_12 = False
    pos = line.find(u'காலை')
    if pos == -1:
        add_12 = True
        pos = line.find(u'மாலை')
        if pos == -1:
            return "0000"
    # Time itself is generally mentioned after the am (காலை) and pm (மாலை) keywords
    words = line[pos:].split()
    time = words[1]

    if (time.find('.')):
        time_components = time.split('.')
    else:
        time_components = time.split(':')
    if time_components[0].isdigit():
        hours_int = int(time_components[0])
        minutes_str = '00'
        if len(time_components) > 1 and time_components[1].isdigit():
            minutes_str = time_components[1]
        if add_12:
            hours_int += 12
        hours_str = str(hours_int)
        if len(hours_str) == 1:
            hours_str = '0' + hours_str

    return hours_str + minutes_str



def get_author_hindi(line):
    author_list_hindi =[u'बाबूजी', u'लालाजी']
    author_list_english = ['Babuji', 'Lalaji']
    for i in range(0, len(author_list_hindi)):
        if line.find(author_list_hindi[i]) != -1:
            return author_list_english[i]
    return ""

def get_author_tamil(line):
    author_dict = {u'பாபூஜி':'Babuji', u'லாலாஜி':'Lalaji'}
    for author_tamil in author_dict.keys():
        if line.find(author_tamil) != -1:
            return author_dict[author_tamil]
    print 'author unidentified'
    return ""


def separate_combined_hindi_whispers_to_separate_files(fin, outdir, csv_writer):
    line_no = 0
    message_beg_flag = False
    year = '0000'
    month = '00'
    day = '00'
    time = '0000'
    author = ''
    whisper_start_line = 0

    lines = fin.readlines()
    num_lines = len(lines)
    print "num_lines ", num_lines

    while line_no < num_lines:
        line = lines[line_no]
        print "At line ", line_no

        if lines[line_no].find(u'प्रिय मालिक') != -1:
            message_beg_flag = True
            # Finish writing out the previous whisper to a file
            if line_no > 0:
                author = get_author_hindi(lines[line_no-1])
                timestamp = year + month + day + time
                filename = timestamp + u'-hi.txt'
                filename_full_path = outdir + '/' + filename
                fout_whisper = io.open(filename_full_path, 'w', encoding='utf8')

                for whisper_line in range (whisper_start_line, line_no):
                    fout_whisper.write(lines[whisper_line] + '\r\n')

                fout_whisper.close()
                print "Naming file: ", filename
                csv_writer.writerow([whisper_start_line + 1, unicode(filename), unicode(timestamp), u'hi', unicode(author), u'1'])

                # Reset variables to default values after use
                year = '0000'
                month = '00'
                day = '00'
                time = '0000'
                author = ''
                #print author
            #Skip reading lines 'प्रिय मालिक' and '
            line_no += 2
            # Also close the prev whispers message here.
            continue

        if message_beg_flag:
            message_beg_flag = False
            whisper_start_line = line_no
            month, month_pos = get_month_hindi(line)
            if month_pos != -1:
                day = get_day_hindi(line[:month_pos])
                year = get_year_hindi(line[month_pos:])
                time = get_time_hindi(line)
            #print "Day:%s Month:%s Year:%s" %(day, month, year)

        line_no += 1

    # Handle the last whisper in the file. We always wrap up the prev whisper
    # after encountering a new one - which wouldn't be the case with the last one!

    if num_lines > 0:
        author = get_author_hindi(lines[line_no-1])
        timestamp = year + month + day + time
        filename = timestamp + u'-hi.txt'
        filename_full_path = outdir + '/' + filename
        fout_whisper = io.open(filename_full_path, 'w', encoding='utf8')

        for whisper_line in range (whisper_start_line, line_no):
            fout_whisper.write(lines[whisper_line] + '\n')

        fout_whisper.close()
        csv_writer.writerow([whisper_start_line + 1, unicode(filename), unicode(timestamp), u'hi', unicode(author), u'1'])

def separate_combined_tamil_whispers_to_separate_files(fin, infile, outdir, csv_writer):
    line_no = 0
    message_beg_flag = False
    year = '0000'
    month = '00'
    day = '00'
    time = '0000'
    author = ''
    whisper_start_line = 0

    # Just get non-blank lines from the file
    # Reference http://stackoverflow.com/questions/4842057/
    # /python-easiest-way-to-ignore-blank-lines-when-reading-a-file
    # lines = filter(None, (line.rstrip() for line in fin))

    lines = fin.readlines()
    num_lines = len(lines)
    print "num_lines ", num_lines

    while line_no < num_lines:
        line = lines[line_no].rstrip()
        # TODO-Vishesh: Check if blank's line length would be 0 or 1
        if utilities.is_blank_line(line):
            line_no += 1
            continue
        #print "At line ", line_no

        if line.isdigit():

            # We retrieve the metadata of the whisper in the next iteration, when
            # we are at the beginning of the actual whisper itself
            message_beg_flag = True


            # Finish writing out the previous whisper to a file
            if line_no > 0:
                print 'Author line', lines[last_non_empty_line_no]
                author = get_author_tamil(lines[last_non_empty_line_no])
                timestamp = year + month + day + time
                filename = timestamp + u'-ta.txt'
                filename_full_path = outdir + '/' + filename
                fout_whisper = io.open(filename_full_path, 'w', encoding='utf8')

                for whisper_line_no in range (whisper_start_line, line_no - 2 ):
                    whisper_line = lines[whisper_line_no]

                    whisper_line = whisper_line.rstrip('\n')
                    whisper_line = whisper_line.rstrip('\r')

                    if utilities.is_blank_line(whisper_line) == False:
                        fout_whisper.write(whisper_line+ u'\r\n')
                        fout_whisper.write(u'\r\n')

                fout_whisper.close()
                print "Naming file: ", filename
                csv_writer.writerow([whisper_start_line + 1, unicode(filename), unicode(timestamp), u'hi', unicode(author), u'1'])

                # Reset variables to default values after use
                year = '0000'
                month = '00'
                day = '00'
                time = '0000'
                author = ''
                #print author

            # 2 is because of word files format:
            # 032
            #
            # The message starts here
            #
            # 033

            line_no += 2
            continue

        if message_beg_flag:
            message_beg_flag = False
            whisper_start_line = line_no
            (year, month, day) = get_year_month_day_tamil(line)
            time = get_time_tamil(line)

        last_non_empty_line_no = line_no
        line_no += 1

    # Handle the last whisper in the file. We always wrap up the prev whisper
    # after encountering a new one - which wouldn't be the case with the last one!

    if num_lines > 0:
        author = get_author_tamil(lines[last_non_empty_line_no])
        timestamp = year + month + day + time
        filename = timestamp + u'-ta.txt'
        filename_full_path = outdir + '/' + filename
        fout_whisper = io.open(filename_full_path, 'w', encoding='utf8')

        for whisper_line_no in range (whisper_start_line, line_no - 2 ):
            whisper_line = lines[whisper_line_no]

            whisper_line = whisper_line.rstrip('\n')
            whisper_line = whisper_line.rstrip('\r')

            if utilities.is_blank_line(whisper_line) == False:
                fout_whisper.write(whisper_line+ u'\r\n')
                fout_whisper.write(u'\r\n')

        fout_whisper.close()
        csv_writer.writerow([whisper_start_line + 1, unicode(filename), unicode(timestamp), u'hi', unicode(author), u'1'])

def restore_hindi_whispers_chars_and_formatting(fin, fout):
    combine_mode_quotes = False
    combine_mode_bracket = False

    for line in fin:

        # Should read http://nedbatchelder.com/text/unipain.html to understand this further.
        # Basically - Encode: Unicode -> Bytes, Decode: Bytes -> Unicode

        line = line.encode('utf-8')

        # These characters have faulty conversion when converted using font-converter (font: shree-dev-0702)

        character_replacement_list = {'ङ्क': 'म',
                                      'ङ्म': 'य',
                                      'μज': 'ज़',
                                      'ङ्ग': '“',
                                      'ङ्घ': '”',
                                      'ङ्ख': 'फ',
                                      'μफ': 'फ़',
                                      'μर्फ':'र्फ़',
                                      '०': '0',
                                      '१': '1',
                                      '२': '2',
                                      '३': '3',
                                      '४': '4',
                                      '५': '5',
                                      '६': '6',
                                      '७': '7',
                                      '८': '8',
                                      '९': '9',
                                      'μक': 'क़',
                                      'μग': 'ग़',
                                      '्रया': 'क्या',
                                      '्रयोंकि': 'क्योंकि',
                                      '्रयों': 'क्यों',
                                      'μख': 'ख़',
                                      'अ्रटूबर':'अक्टूबर',
                                      'ैैं': 'ैं',
                                      'आें':'ओं',
                                      '़ुड': 'ुड़',
                                      'ढूँ़ढ': 'ढूँढ',
                                      'कभीकभी':'कभी-कभी',
                                      'छोटीछोटी':'छोटी-छोटी',
                                      'काया]': 'कार्य',
                                      'ेें': 'ें',
                                      '‘‘': '“',
                                      '’’': '”',

                                      # *********DON'T TOUCH*********
                                      '़ड':'ड़',
                                      '़ढ': 'ढ़',
                                      '़ोड': 'ोड़',
                                      'ंॅ': 'ँ',
                                      # ****************************

                                      'वμ्रत': 'वक्त'}

        for char in character_replacement_list.keys():
            line = line.replace(char, character_replacement_list[char])

        # The whispers copied from PDF have newline after each line appearing in the PDF.
        # We therefore have to combine multiple lines in a single line by observing opening "
        # or (.
        #print line[0], line[-2]

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
        # This is because in there, the characters are no longer 1-byte. In fact, I think we can safely
        # assume each char to be of 4 byte when working with pure Unicode.

        if line.find('”') == len(line) -4:
            combine_mode_quotes = False
            print "Combine mode quotes end"

        if line.find('प्रिय मालिक') != -1:
            combine_mode_bracket = False
            combine_mode_quotes = False

        if combine_mode_quotes == True or combine_mode_bracket == True:
            #The \n acts as a space as well, so replace that with space
            line = line.replace('\n', ' ')

        fout.write(line.decode("utf-8"))
        #fout.write(line)

        # line = line.replace( '६' , '6' )

def restore_tamil_whispers_chars_and_formatting(fin, fout):
    for line in fin:

        # Should read http://nedbatchelder.com/text/unipain.html to understand this further.
        # Basically - Encode: Unicode -> Bytes, Decode: Bytes -> Unicode

        line = line.encode('utf-8')
        line = line.replace('Œாட்சியாக', 'சாட்சி யாக')
        fout.write(line.decode("utf-8"))

def process_conversion_to_panini(infile, indir, outdir, language, refine, panini):

    # In batch mode, the input file consists of a newline separated list of file names containing the source text
    if (indir == True):
        print "**********************"
        print "Directory Mode Enabled"
        print "**********************"

    print 'Input file:', infile
    print 'Language:', language

    if language != "tamil" and language != "hindi":
        sys.stderr.write("Language not supported\n")
        exit(1)
    filenames = []
    if indir:
        filenames = utilities.get_files_in_dir(indir)
    else:
        filenames.append(infile)

    for filename in utilities.get_files_in_dir(indir):

        if indir:
            read_filename = indir + '/' + filename
        else:
            read_filename = filename

        print "Processing file", filename

        fin = io.open(read_filename, 'r', encoding='utf8')
        fin_filename = filename

        if refine:
            outfile_conversion = filename + ".converted"
            outfile_conversion_full_path = outdir + '/' + outfile_conversion

            print "Writing refined output to %s" %outfile_conversion_full_path

            # encoding='utf8' is necessary because file is opened in ascii by default, which throws error when trying to
            # write a non-ascii character

            fout_conversion = io.open(outfile_conversion_full_path, 'w', encoding='utf8')

            if language == 'hindi':
                restore_hindi_whispers_chars_and_formatting(fin, fout_conversion)
            else:
                restore_tamil_whispers_chars_and_formatting(fin, fout_conversion)

            fin.close()
            fout_conversion.close()


            fin = io.open(outfile_conversion_full_path, 'r', encoding='utf8')
            fin_filename = outfile_conversion

        if panini:
            outfile_csv = outdir + '/' + 'whispers.' + language + '.csv'

            fout_csv = io.open(outfile_csv, 'ab')


            # Lifted from http://stackoverflow.com/questions/2084069/create-a-csv-file-with-values-from-a-python-list
            csv_writer = csv.writer(fout_csv, quoting=csv.QUOTE_ALL)
            if language == 'hindi':
                separate_combined_hindi_whispers_to_separate_files(fin, outdir, csv_writer)
            else:
                separate_combined_tamil_whispers_to_separate_files(fin, fin_filename, outdir, csv_writer)
            fout_csv.close()

        fin.close()





def print_usage(binary_name):
    print 'Usage:', binary_name, "--infile=<inputfile> --indir=<input dir> -l=<hindi/tamil> --refine -- panini"
    print "--indir: Take all files in the dir for processing "
    print "--refine: Refine UTF-8 files further "
    print "--panini: Split into whispers with panini naming convention and populate a csv file"
    sys.exit(2)


def main(binary_name, argv):

    infile = None
    language = None
    indir = None
    outdir = '.'

    # Refine output from font-converter to correct some chars as well as combine split sentences
    refine = False

    # Create Whispers files for Panini
    panini = False


    batch_mode = False
    if len(argv) == 0:
        print_usage(binary_name)

    try:
        # Used to get command line options for the script. ":" means arg also expected.
        opts, args = getopt.getopt(argv, "hl:", ["help", "infile=", "indir=", "outdir=", "infile=",
                                                 "refine", "panini"])
    except getopt.GetoptError:
        print "Cannot parse arguments. Re-check flags"
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
        elif opt == "--refine":
            refine = True
        elif opt == "--panini":
            panini = True


    if infile == None and indir == None:
        print "Input file / Dir not specified"
        print_usage(binary_name)
    if refine == False and panini == False:
        print "No operations specified. Specify among --refine and/or --panini"
    elif language == None:
        print "Language not specified"
        print_usage(binary_name)

    print 'Input file:', infile
    print 'Input Dir:', indir
    print 'Language:', language

    process_conversion_to_panini(infile, indir, outdir, language, refine, panini)


if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
