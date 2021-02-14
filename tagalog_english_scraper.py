# author: Nathaniel B. Chavez
# in this file, BeautifulSoup was used to scrape all the dictionary words from 'https://tagalog.pinoydictionary.com/'
# request module is for checking if page is valid

import string
import re
from nltk.corpus import words
from urllib import request
from bs4 import BeautifulSoup
import requests
import os

# get alphabet
alphabet = string.ascii_lowercase

# can be any dir depends on your environment 
os.chdir("C:/Users/Nathan/Desktop/TOPL finals/FINALS")
tagalog_list = []

# checking if a page is valid
def is_page_valid(page_number, letter_index, url):
    request = requests.get(url)
    is_valid_page = True
    if request.status_code == 200:
        is_valid_page = True
    else:
        if letter_index < len(alphabet)-1:
            letter_index += 1
            page_number = 0
            print(letter_index)
        else:
            is_valid_page = False
    return page_number, letter_index, is_valid_page


is_valid_page = True
page_number = 1
index = 0

# the URL is just the increment of page number and letter in alphabet
# it will auto scrape each page from the website

while is_valid_page:
    url = 'https://tagalog.pinoydictionary.com/list/' + str(alphabet[index]) + '/' + str(page_number) + '/'
    page_number, index, is_valid_page = is_page_valid(page_number, index, url)
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    #h2.word-entry stands for heading 2 class word-entry
    # using the inspect element and finding the element of the data needs to be gathered,
    # the page number and current letter will increment
    for i in range(0, len(soup.select('h2.word-entry'))):
        word = soup.select('h2.word-entry')[i].text.strip()
        tagalog_list.append(word)
    page_number += 1

# writing the scraped words in a txt file
tagalog_words = ','.join(tagalog_list)
tagalogString = re.sub(',', '\n', tagalog_words)
f = open('tagalog_dict.txt', "w")
f.write(tagalogString)
f.close()



# get english dictionary from nltk.corpus
word_list = words.words()
word_list = [w.lower() for w in word_list]
string_words = "\n".join(word_list)


f = open('english_dict.txt', "w")
f.write(string_words)
f.close()

# note: this is an unclean data (words), the cleaning happened on file named clean_dictionaries.py