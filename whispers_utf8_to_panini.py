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
import csv
from os import path

from collections import OrderedDict

__author__ = 'spec'

hindi_months_dictionary = {u"जनवरी": '01', u"फरवरी": '02', u"मार्च": '03', u"अप्रैल": '04',
                           u'अप्रेल': '04', u"मई": '05', u"जून": '06', u"जुलाई": '07',
                           u"अगस्त": '08', u"सितम्बर": '09', u"अक्टूबर": '10', u"नवम्बर": '11',
                           u"दिसम्बर": '12'}

language = None

def get_year_month_day_hindi(line):

    # Example Header: सोमवार, 2 अगस्त 1999  प्रात: 1000 बजे

    year = '0000'
    month = '00'
    day = '00'

    line = line.rstrip('\n')
    line = line.rstrip('\r')

    for month_hindi in hindi_months_dictionary.keys():
        pos = line.find(month_hindi)
        if pos != -1:
            month = hindi_months_dictionary[month_hindi]
            post_month_words = line[pos:].replace(',', '').split(' ')
            if len(post_month_words) > 1 and post_month_words[1].isdigit():
                year = post_month_words[1]

            pre_month_words = line[:pos].split()
            if len(pre_month_words) > 0 and pre_month_words[-1].isdigit():
                day = pre_month_words[-1]
                # Handle single digit such as 9
                if len(day) == 1:
                    day = '0' + day

    return year, month, day


def get_year_month_day_tamil(line):
    year = '0000'
    month = '00'
    day = '00'

    months_list = {u"ஜனவரி": '01', u"பிப்ரவரி": '02', u"மார்ச்": '03', u"ஏப்ரல்": '04',
                   u"மே": '05', u"ஜூன்": '06', u"ஜூலை": '07',
                   u"ஆகஸ்ட்": '08', u'ஆகஸ்டு':'08', u"செப்டம்பர்": '09', u"அக்டோபர்": '10', u"அக்டோபர்": '10',
                   u"நவம்பர்": '11', u"டிசம்பர்": '12'}

    for month_tamil in months_list.keys():
        pos = line.find(month_tamil)
        if pos != -1:
            # Get the list of all words after the month string
            month = months_list[month_tamil]
            post_month_words = line[pos:].replace(',', '').split(' ')
            if len(post_month_words) > 1 and post_month_words[1].isdigit():
                day = post_month_words[1]
                # Handle single digit such as 9
                if len(day) == 1:
                    day = '0' + day
            if len(post_month_words) > 2 and post_month_words[2].isdigit():
                year = post_month_words[2]

    return year, month, day


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
    hours_str = "00"
    minutes_str = '00'

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


def get_time_tamil(line):
    # Conversion to 24-hours timezone
    hours_str = '00'
    minutes_str = '00'
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

    if time.find('.') != -1:
        time_components = time.split('.')
    else:
        time_components = time.split(':')
    time_components[0] = time_components[0].strip(' ')
    if time_components[0].isdigit():
        hours_int = int(time_components[0])
        minutes_str = '00'
        if len(time_components) > 1:
            time_components[1] = time_components[1].strip(' ')
            if time_components[1].isdigit():
                minutes_str = time_components[1]
        if add_12:
            hours_int += 12
        hours_str = str(hours_int)
        if len(hours_str) == 1:
            hours_str = '0' + hours_str

    return hours_str + minutes_str


def get_author_hindi(line):
    author_list_hindi = [u'बाबूजी', u'लालाजी']
    author_list_english = ['Babuji', 'Lalaji']
    for i in range(0, len(author_list_hindi)):
        if line.find(author_list_hindi[i]) != -1:
            return author_list_english[i]
    return ""


def get_author_tamil(line):
    author_dict = {u'பாபூஜி': 'Babuji', u'லாலாஜி': 'Lalaji', u'ஜானகி': 'Janaki'}
    for author_tamil in author_dict.keys():
        if line.find(author_tamil) != -1:
            return author_dict[author_tamil]
    print 'WARNING: author unidentified'
    return ""



def get_param_value(line):
    words = line.split(':')
    value = words[1]
    return value.rstrip('\n').rstrip('\r')


def separate_consolidated_whispers_master_file_into_individual_files(f_in, outdir, csv_writer):
    line_no = 0
    whisper_begin = False

    for line in f_in:
        line_no += 1
        if line.find("=======") == 0:
            continue
        elif line.find('#SOURCE') == 0:
            continue
        elif line.find('#YEAR') == 0:
           year = get_param_value(line)
           if len(year) != 4 or year == '0000':
               print "ERROR. Line No: ", line_no, "Invalid year"
        elif line.find('#MONTH') == 0:
            month = get_param_value(line)
            if len(month) != 2:
                print "ERROR. Line No: ", line_no, " Invalid Month"
        elif line.find('#DAY') == 0:
            day = get_param_value(line)
            if len(day) != 2:
                print "ERROR. Line No: ", line_no, " Invalid Day"
        elif line.find('#TIME') == 0:
            time = get_param_value(line)
        elif line.find('#AUTHOR') == 0:
            author = get_param_value(line)
        elif line.find('#WHISPER_BEGIN') == 0:
            if whisper_begin:
                print "ERROR. Line No: ", line_no, " 2 consecutive WHISPER_BEGIN without intermediate WHISPER_END. Exiting!"
                exit(1)
            whisper_begin = True
            timestamp = year + month + day + time
            if language == 'hindi':
                filename = timestamp + '-hi.txt'
            else:
                filename = timestamp + '-ta.txt'
            out_file_path = outdir + '/' + filename
            if path.isfile(out_file_path):
                print "WARNING: Line No: ", line_no, " Repeated file. Appending Data ", filename
            f_out = io.open(out_file_path, 'a', encoding='utf8')
        elif line.find('#WHISPER_END') == 0:
            if not whisper_begin:
                print "ERROR. Line No: ", line_no, " WHISPER_END without WHISPER_BEGIN. Exiting!"
                exit(1)
            whisper_begin = False
            if language == 'hindi':
                csv_writer.writerow([line_no, unicode(timestamp), u'hi', unicode(author), u'1'])
            else:
                csv_writer.writerow([line_no, unicode(timestamp), u'ta', unicode(author), u'1'])

        # We are reading a non-metadata line. Hence, if we have already encountered WHISPER_BEGIN,
        # simply output the line to the currently opened file. Else Exit!
        else:
            if not whisper_begin:
                print "ERROR. Line No: ", line_no, " Unidentified Portion of File. Exiting!"
                exit(1)
            f_out.write(line)


def write_out_whisper_hindi(lines, year, month, day, time,
                            infile, fout, whisper_start_line,
                            whisper_end_line):

    author = get_author_hindi(lines[whisper_end_line])
    timestamp = year + month + day + time
    fout.write(u'========================\n')
    fout.write(u"#SOURCE:" + infile + ', ' + str(whisper_start_line) + '\n')
    fout.write(u"#YEAR:" + year + '\n')
    fout.write(u"#MONTH:" + month + '\n')
    fout.write(u"#DAY:" + day + '\n')
    fout.write(u"#TIME:" + time + '\n')
    fout.write(u"#AUTHOR:" + author + '\n')
    fout.write(u'#WHISPER_BEGIN\n')

    for whisper_line_no in range(whisper_start_line, whisper_end_line):
        whisper_line = lines[whisper_line_no]

        whisper_line = whisper_line.rstrip('\n')
        whisper_line = whisper_line.rstrip('\r')

        if not utilities.is_blank_line(whisper_line):
            fout.write(whisper_line + u'\r\n')
            fout.write(u'\r\n')

    # There should be no blank line after author, hence putting it separately
    fout.write(lines[whisper_end_line])

    fout.write(u'#WHISPER_END\n')


def write_consolidated_hindi_whispers_master_file(fin, fout, infile):
    line_no = 0
    message_beg_flag = False
    year = '0000'
    month = '00'
    day = '00'
    time = '0000'
    whisper_start_line = 0

    lines = fin.readlines()
    num_lines = len(lines)
    print "num_lines ", num_lines

    while line_no < num_lines:
        line = lines[line_no]
        # print "At line ", line_no
        if lines[line_no].find(u'प्रिय मालिक') != -1:
            message_beg_flag = True
            # Finish writing out the previous whisper to a file
            if line_no > 0:
                write_out_whisper_hindi(lines, year, month, day, time, infile, fout, whisper_start_line, line_no-1)

                # Reset variables to default values after use
                year = '0000'
                month = '00'
                day = '00'
                time = '0000'

            # Skip reading lines 'प्रिय मालिक' and '
            line_no += 2
            # Also close the prev whispers message here.
            continue

        if message_beg_flag:
            message_beg_flag = False
            whisper_start_line = line_no
            (year, month, day) = get_year_month_day_hindi(line)
            time = get_time_hindi(line)

            # print "Day:%s Month:%s Year:%s" %(day, month, year)

        line_no += 1

    # Handle the last whisper in the file. We always wrap up the prev whisper
    # after encountering a new one - which wouldn't be the case with the last one!

    if num_lines > 0:
        write_out_whisper_hindi(lines, year, month, day, time,
                                infile, fout,
                                whisper_start_line, line_no-1)

def write_out_whisper_tamil(lines, year, month, day, time,
                            infile, fout, whisper_start_line,
                            whisper_end_line):

    author = get_author_tamil(lines[whisper_end_line])
    timestamp = year + month + day + time
    fout.write(u'========================\n')
    fout.write(u"#SOURCE:"+infile + ', ' + str(whisper_start_line) + '\n')
    fout.write(u"#YEAR:"+year+'\n')
    fout.write(u"#MONTH:"+month+'\n')
    fout.write(u"#DAY:"+day+'\n')
    fout.write(u"#TIME:"+time+'\n')
    fout.write(u"#AUTHOR:"+author+'\n')
    fout.write(u'#WHISPER_BEGIN\n')

    for whisper_line_no in range(whisper_start_line, whisper_end_line):
        whisper_line = lines[whisper_line_no]

        whisper_line = whisper_line.rstrip('\n')
        whisper_line = whisper_line.rstrip('\r')

        if not utilities.is_blank_line(whisper_line):
            fout.write(whisper_line + u'\r\n')
            fout.write(u'\r\n')

    # There should be no blank line after author, hence putting it separately
    fout.write(lines[whisper_end_line])

    fout.write(u'#WHISPER_END\n')


def write_consolidated_tamil_whispers_master_file(fin, fout, infile):
    line_no = 0
    message_beg_flag = False
    year = '0000'
    month = '00'
    day = '00'
    time = '0000'
    whisper_start_line = 0
    last_non_empty_line_no = None

    # Just get non-blank lines from the file
    # Reference http://stackoverflow.com/questions/4842057/
    # /python-easiest-way-to-ignore-blank-lines-when-reading-a-file
    # lines = filter(None, (line.rstrip() for line in fin))

    lines = fin.readlines()
    num_lines = len(lines)

    while line_no < num_lines:
        line = lines[line_no].rstrip()

        if utilities.is_blank_line(line):
            line_no += 1
            continue
        # print "At line ", line_no

        if line.isdigit():

            # We retrieve the metadata of the whisper in the next iteration, when
            # we are at the beginning of the actual whisper itself
            message_beg_flag = True

            # Finish writing out the previous whisper to a file
            if line_no > 0:
                write_out_whisper_tamil(lines, year, month, day, time, infile,
                                        fout, whisper_start_line,
                                        last_non_empty_line_no)

                # Reset variables to default values after use
                year = '0000'
                month = '00'
                day = '00'
                time = '0000'
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
        write_out_whisper_tamil(lines, year, month, day, time, infile,
                                fout, whisper_start_line,
                                last_non_empty_line_no)


def restore_hindi_whispers_chars_and_formatting(fin, fout):
    combine_mode_quotes = False
    combine_mode_bracket = False

    # A weird way of keeping track of whether we've seen
    # a genuine message header. Increment it by 1 each time we
    # see priya malik, then babuji maharaj, and finally date.
    is_header_count_to_3 = 0
    prev_combined_lines = ''

    for line in fin:

        # Should read http://nedbatchelder.com/text/unipain.html to understand this further.
        # Basically - Encode: Unicode -> Bytes, Decode: Bytes -> Unicode

        line = line.encode('utf-8')

        # These characters have faulty conversion when converted using font-converter (font: shree-dev-0702)
        # OrderedDict keeps the order of insertion of keys. Necessary since we want to replace single chars
        # first, followed by whole words
        character_replacement_list = OrderedDict([('ङ्क', 'म'),
                                                  ('ङ्म', 'य'),
                                                  ('μज', 'ज़'),
                                                  ('ङ्ग', '“'),
                                                  ('ङ्घ', '”'),
                                                  ('ङ्ख', 'फ'),
                                                  ('μफ', 'फ़'),
                                                  ('μर्फ', 'र्फ़'),
                                                  ('०', '0'),
                                                  ('१', '1'),
                                                  ('२', '2'),
                                                  ('३', '3'),
                                                  ('४', '4'),
                                                  ('५', '5'),
                                                  ('६', '6'),
                                                  ('७', '7'),
                                                  ('८', '8'),
                                                  ('९', '9'),
                                                  ('μक', 'क़'),
                                                  ('μग', 'ग़'),
                                                  ('‘‘', '“'),
                                                  ('’’', '”'),
                                                  (' ्रया ', ' क्या '),
                                                  ('“्रया', '“क्या'),
                                                  ('्रयोंकि', 'क्योंकि'),
                                                  ('्रयों', 'क्यों'),
                                                  ('μख', 'ख़'),
                                                  ('अ्रटूबर','अक्टूबर'),
                                                  ('ैैं',  'ैं'),
                                                  ('आें', 'ओं'),
                                                  # ('़ुड',  'ुड़'),
                                                  ('़ुड',  'ुड़'),
                                                  # ('़ीड', 'ीड़'),
                                                  ('़ीड', 'ीड़'),
                                                  # ('़ाड', 'ाड़'),
                                                  ('़ाड', 'ाड़'),
                                                  ('कदमकदम', 'कदम-कदम'),
                                                  ('धीरेधीरे','धीरे-धीरे'),
                                                  ('ढूँ़ढ', 'ढूँढ'),
                                                  # ('़ृढ','ृढ़'),
                                                  ('़ृढ', 'ृढ़'),
                                                  # ('हँू', 'हूँ'),
                                                  ('हँू', 'हूँ'),

                                                  # ('ेें', 'ें'),
                                                  ('ेें', 'ें'),
                                                  ('ाें', 'ों'),
                                                  ('कभीकभी', 'कभी-कभी'),
                                                  ('छोटीछोटी', 'छोटी-छोटी'),
                                                  ('साथसाथ', 'साथ-साथ'),
                                                  ('काया]', 'कार्य'),
                                                  ('धमा]', 'धर्म'),
                                                  ('निष्कषा]', 'निष्कर्ष'),
                                                  ('μंजदगी', 'ज़िंदगी '),


                                                  # *********DON'T TOUCH*********
                                                  # ('़ड','ड़'),
                                                  ('़ड', 'ड़'),
                                                  # ('़ढ', 'ढ़'),
                                                  ('़ढ', 'ढ़'),
                                                  # ('़ोड', 'ोड़'),
                                                  ('़ोड', 'ोड़'),
                                                  # ('ंॅ', 'ँ'),
                                                  ('ंॅ', 'ँ'),
                                                  # ****************************

                                                  ('वμ्रत', 'वक्त')])

        for char in character_replacement_list.keys():
            line = line.replace(char, character_replacement_list[char])

        # The whispers copied from PDF have newline after each line appearing in the PDF.
        # We therefore have to combine multiple lines in a single line by observing opening "
        # or (.
        # print line[0], line[-2]

        # We have repeated header of 'प्रिय मालिक' in case of whispers spanning more
        # than a page. Hence weed out false positives
        if line.find('प्रिय मालिक') != -1:
            is_header_count_to_3 = 1
            prev_combined_lines = line
            continue

        elif is_header_count_to_3 == 1:
            if line.find('पूज्य बाबूजी महाराज') != -1:
                is_header_count_to_3 = 2
                prev_combined_lines = prev_combined_lines + line
            else:
                is_header_count_to_3 = 0
                prev_combined_lines = ''
            continue

        elif is_header_count_to_3 == 2:
            for month_hindi in hindi_months_dictionary.keys():
                if -1 != line.find(month_hindi.encode('utf8')):
                    # We got a genuine header. Add prev lines to current line for output
                    line = prev_combined_lines + line
                    combine_mode_bracket = False
                    combine_mode_quotes = False
                    break
            is_header_count_to_3 = 0
            prev_combined_lines = ''

        if line[0] == '(':
            combine_mode_bracket = True
        if line.find('“') == 0:
            combine_mode_quotes = True
        else:
            words = line.split()
            # Handle lines like माध्यम : “यह or माध्यम : “यह
            if len(words) >= 3 and (words[1].find('“') == 0 or words[2].find('“') == 0):
                combine_mode_quotes = True

        # [-1] would be '\n'
        if line[-2] == ')':
            combine_mode_bracket = False

        # Used hit-and-trial (aka printfs) to determine where does a closed brace appear in unicode!
        # This is because in there, the characters are no longer 1-byte. In fact, I think we can safely
        # assume each char to be of 4 byte when working with pure Unicode.

        if line.find('”') == len(line) - 4:
            combine_mode_quotes = False

        if combine_mode_quotes or combine_mode_bracket:
            # The \n acts as a space as well, so replace that with space
            line = line.replace('\n', ' ')

        fout.write(line.decode("utf-8"))
        # fout.write(line)

        # line = line.replace( '६' , '6' )


def restore_tamil_whispers_chars_and_formatting(fin, fout):
    for line in fin:

        # Should read http://nedbatchelder.com/text/unipain.html to understand this further.
        # Basically - Encode: Unicode -> Bytes, Decode: Bytes -> Unicode

        line = line.encode('utf-8')
        line = line.replace('Œாட்சியாக', 'சாட்சி யாக')
        fout.write(line.decode("utf-8"))


def process_conversion_to_panini(infile, indir, outdir, language, refine, panini_consolidated, panini):

    # In batch mode, the input file consists of a newline separated list of file names containing the source text
    if indir:
        print "**********************"
        print "Directory Mode Enabled"
        print "**********************"

    print 'Input file:', infile
    print 'Language:', language

    if language != "tamil" and language != "hindi":
        sys.stderr.write("Language not supported\n")
        exit(1)
    filenames = []
    output_filenames = []

    if indir:
        filenames = utilities.get_files_in_dir(indir)
    else:
        filenames.append(infile)

    if refine:

        for filename in filenames:

            if indir:
                read_filename = indir + '/' + filename
            else:
                read_filename = filename

            print "Processing file", filename

            fin = io.open(read_filename, 'r', encoding='utf8')

            outfile_conversion = filename + ".converted"
            outfile_conversion_full_path = outdir + '/' + outfile_conversion

            print "Writing refined output to %s" % outfile_conversion_full_path

            # encoding='utf8' is necessary because file is opened in ascii by default, which throws error when trying to
            # write a non-ascii character

            fout_conversion = io.open(outfile_conversion_full_path, 'w', encoding='utf8')

            if language == 'hindi':
                restore_hindi_whispers_chars_and_formatting(fin, fout_conversion)
            else:
                restore_tamil_whispers_chars_and_formatting(fin, fout_conversion)

            fin.close()
            fout_conversion.close()

            output_filenames.append(outfile_conversion)

        filenames = output_filenames
        output_filenames=[]

        #Now my input files for next round would be located in outdir
        indir = outdir

    if panini_consolidated:
        if language == 'hindi':
            outfile_panini_consolidated = 'hindi-whispers.txt'
        else:
            outfile_panini_consolidated = 'tamil-whispers.txt'
        fout = io.open(outdir + '/' + outfile_panini_consolidated, 'w', encoding='utf8')



        for filename in filenames:

            if indir:
                read_filename = indir + '/' + filename
            else:
                read_filename = filename

            print "Processing file", filename

            fin = io.open(read_filename, 'r', encoding='utf8')

            if language == 'hindi':
                write_consolidated_hindi_whispers_master_file(fin, fout, filename)
            else:
                write_consolidated_tamil_whispers_master_file(fin, fout, filename)

            fin.close()

        fout.close()
        output_filenames.append(outfile_panini_consolidated)
        filenames = output_filenames

        #Now my input files for next round would be located in outdir
        indir = outdir

    if panini:

        outfile_csv = outdir + '/' + 'whispers.' + language + '.csv'

        # Lifted from http://stackoverflow.com/questions/2084069/create-a-csv-file-with-values-from-a-python-list
        fout_csv = io.open(outfile_csv, 'wb')
        csv_writer = csv.writer(fout_csv, quoting=csv.QUOTE_ALL)

        for filename in filenames:

            if indir:
                read_filename = indir + '/' + filename
            else:
                read_filename = filename

            print "Separating whispers files", filename

            fin = io.open(read_filename, 'r', encoding='utf8')

            separate_consolidated_whispers_master_file_into_individual_files(fin, outdir, csv_writer)

            fin.close()

        fout_csv.close()




def print_usage(binary_name):
    print 'Usage:', binary_name, "--infile=<inputfile> --indir=<input dir> -l=<hindi/tamil> --refine --combine --panini "
    print "--infile: Take just a given file for processing"
    print "--indir: Take all files in the dir for processing "
    print "--refine: Refine UTF-8 files further "
    print "--combine: Combined set of whispers (for verification)"
    print "--panini: Split into whispers with panini naming convention and populate a csv file"
    sys.exit(2)


def main(binary_name, argv):
    infile = None
    indir = None
    outdir = '.'

    global language

    # Refine output from font-converter to correct some chars as well as combine split sentences
    refine = False
    panini = False
    panini_consolidated = False


    # Create Whispers files for Panini
    panini_consolidated = False

    if len(argv) == 0:
        print_usage(binary_name)

    try:
        # Used to get command line options for the script. ":" means arg also expected.
        opts, args = getopt.getopt(argv, "hl:", ["help", "infile=", "indir=",
                                                 "outdir=",
                                                 "refine", "combine", "panini"])
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
        elif opt == "--combine":
            panini_consolidated = True
        elif opt == "--panini":
            panini = True

    if infile is None and indir is None:
        print "Input file / Dir not specified"
        print_usage(binary_name)
    if not refine and not panini_consolidated and not panini:
        print "No operations specified. Specify among --refine and/or --combine and/or --panini"
        print_usage(binary_name)
    elif language is None:
        print "Language not specified"
        print_usage(binary_name)

    print 'Input file:', infile
    print 'Input Dir:', indir
    print 'Language:', language

    process_conversion_to_panini(infile, indir, outdir, language, refine, panini_consolidated, panini)


if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
