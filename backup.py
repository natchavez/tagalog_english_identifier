# author: Nathaniel B. Chavez

# dictionaries/ list of words was scraped using the file tagalog_english_scraper.py
# both dictionaries were cleaned using the clean_dictionaries.py

#importing necessary module 
import sys, getopt
import os
import re
from string import ascii_uppercase
from os import path

vowel_letters = "aeiou"

#get current file directory
cwd = os.getcwd()
#get the drive letter ex. C, D, F, E
drive_letter = cwd[0]
data = []

## FUNCTIONS BELOW

#function if the input file is not in the same directory as py script
# this will return the location of the file
def get_file_location(file_name):
    try:
        for root, dirs, files in os.walk(drive_letter + ':\\'):
            for name in files:
                if name.endswith(".txt"):
                    if name == file_name.strip():
                        return str(os.path.abspath(os.path.join(root, name)))
    except Exception as e:
        print("Error: " + e)
           

# get list of text from an input
def get_textList(data):
    #textList = word_tokenize(data.lower())
    textList = data.split()
    return textList


# count the lines of the file not including the nextline or \n
def get_line_count(file):
    with open(file) as fp:
        line = fp.readline()
        count = 0
        while line:
            line = fp.readline()
            if line != "\n":
                count +=1
    return count


# get number of consonants and vowels
def get_char_count(textList):
    vowels = 0
    consonants = 0
    long_word = "".join(textList)
    long_word = long_word.strip().lower()
    for letter in long_word:
        if letter in vowel_letters:
            vowels += 1
        else:
            consonants += 1
    dict = {"vowels": vowels, "consonants": consonants}
    return dict


# get Filipino words from the inputted file
# this returns the number of tagalog words in the file, just in case it needs to be mentioned
def get_filipino_words(textList, tagalog_word_list):
    #tagalog_word_list will be the list of tagalog dictionary
    tag_col= list(tagalog_word_list.split(","))
    tag_list = [w.strip().lower() for w in tag_col]
    tagalog_list = []
    tagalog_count = 0
    #textList_lower = [word.lower() for word in textList]
    for word in textList:
        if word.lower() in tag_list:
            tagalog_list.append(word)
            tagalog_count += 1

    return tagalog_count, tagalog_list


# get english words count from dictionary
# the english dictionary used is composed of 400k+ words from nltk.corpus
# the length is huge, because it is a combination of singalur and plural words
def get_english_words(textList, english_word_list):
    eng_col = list(english_word_list.split(","))
    eng_list = [w.strip().lower() for w in eng_col]
    english_list = []
    english_count = 0
    #textList_lower = [word.lower() for word in textList]
    for word in textList:
        if word.lower() in eng_list:
            english_list.append(word)
            english_count += 1

    return english_count, english_list


# function for getting output file. data[4] is just to check wether the format will be english or tagalog
#will not return anything. will just create a new file in the current directory where this script is
def get_output_file(file_name, data):
    file = open(file_name, "w")
    eng_vowels = data[2]["vowels"]
    eng_consontants = data[2]["consonants"]
    if data[4] == "tagalog":
        tagalog_print = "Filename:{file}\nBlg. ng hanay: {0}\nBlg. ng Salita: {1}\nBlg. ng Patinig: {2}\nBlg. ng Katinig: {3}\n\nGinamit na Salitang Pilipino: \n{4}".format(data[0], data[1], eng_vowels, eng_consontants, data[3], file = str(file_name))
        file.write(tagalog_print)
    elif data[4] == "english":
        eng_print = "Filename:{file}\nNo. of Lines: {0}\n\nNo. of English words: {1}\nNo. of English Vowels: {2}\nNo. of English Consonants: {3}\n\nEnglish words used: \n{4}".format(data[0], data[1], eng_vowels, eng_consontants, data[3], file = str(file_name))
        file.write(eng_print)
    file.close()


def main(argv):
    # code below's skeleton is from myscript.py in vle
    input_f = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"h:o:p:e:",["english=", "pilipino=", "output="])
    except getopt.GetoptError:
        print("-h: help\n-o + <output file>: output\n-p + <input file>: find tagalog words\n-e  + <input file>: find english words")
        sys.exit(2)
    for opt, arg in opts:
        # for help in commands
        if opt == '-h':
            print ("-h: help\n-o + <output file>: output\n-p + <input file>: find tagalog words\n-e  + <input file>: find english words")
            sys.exit()
        #for output
        elif opt in ("-o", "--output"):
            outputfile = arg
        # for filipino counter
            get_output_file(outputfile, data)
        elif opt in ("-p", "--pilipino"):
            # if user would like to look up all filipino words in the document
            input_f = arg.strip()
            #will look in current directory first
            try:
                inputfile = (str(cwd) + "\\" +input_f).strip()
                text = open(inputfile, "r")
            #will look up the pc
            except:
                try:
                    print("File not in current directory")
                    print("Continue looking? This may take a while...")
                    choice = input("Y/N: ").lower()
                    if choice =='y':
                        print("Now finding the file in your PC...\n")
                        print("This may take a while...")
                        inputfile = get_file_location(input_f)
                        text = open(inputfile, "r")
                    else:
                        break
                except:
                    print("File not found.")
                    break
            tagalog_poem = text.read()
            tagalog_poem_words = re.sub("\W+|\d+", " ", tagalog_poem)
            textList = get_textList(tagalog_poem_words)
            tag_dict = open('final_tagalog_dict.txt', "r")
            tagalog_words = tag_dict.read()
            tagalog_word_list = re.sub(" ", "\n", tagalog_words)
            tagalog_word_list = re.sub("\n", ",", tagalog_word_list)
            # converting the dictionary into list
            # getting all needed data
            line_count = get_line_count(inputfile)
            tagalog_count, tagalog_list = get_filipino_words(textList, tagalog_word_list)
            dict = get_char_count(tagalog_list)
            tagalog_words = "\n".join(tagalog_list)

            print("No. of Lines: {}".format(line_count))
            print("No. of Filipino words: {}".format(tagalog_count))
            print("No. of Fiipino Vowels (Patinig): {0}\nNo. of Fiipino Consonants (Katinig): {1}".format(dict["vowels"],dict["consonants"]))
            # for english counter
            data = [line_count, tagalog_count, dict, tagalog_words, "tagalog"]

        elif opt in ("-e", "--english"):
            # if user would like to look up all english words in the document
            input_f = arg.strip()

            try:
            # if user would like to look up all filipino words in the document
                inputfile = (str(cwd) + "\\" +input_f).strip()
                text = open(inputfile, "r")
            except:
            #will look up the pc
                try:
                    print("File not in current directory")
                    print("Continue looking? This may take a while...")
                    choice = input("Y/N: ").lower()
                    if choice =='y':
                        print("Now finding the file in your PC...\n")
                        print("This may take a while...")
                        inputfile = get_file_location(input_f)
                        text = open(inputfile, "r")
                    else:
                        break
                except:
                    print("File not found")
                    break
            english_poem = text.read()
            english_poem_words = re.sub("\W+|\d+", " ", english_poem)
            textList = get_textList(english_poem_words)

            eng_dict = open('final_english_dict.txt', "r")
            english_words = eng_dict.read()
            english_word_list = re.sub("\n", ",", english_words)

            line_count = get_line_count(inputfile)
            english_count, english_list = get_english_words(textList, english_word_list)
            dict = get_char_count(english_list)
            english_words = "\n".join(english_list)

            print("No. of Lines: {}".format(line_count))
            print("No. of English words: {}".format(english_count))
            print("No. of English Vowels: {0}\nNo. of English Consonants: {1}".format(dict["vowels"],dict["consonants"]))

            data = [line_count, english_count, dict, english_words, "english"]

if __name__ == "__main__":
    main(sys.argv[1:])
