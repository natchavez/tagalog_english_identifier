# Author: Nathaniel B. Chavez
# this was ran using Jupyter notebook, in order to clean the data of both filipino and english
# the nltk.corpus of english words are not yet in plural form, so added the list of orig corpus + the plural form
# I used inflect to get plural form of english words


import string
import re
from nltk.corpus import words
import os
import inflect


# os.chdir can be anything where you would like to pull a file. here I used my own dir
os.chdir("C:/Users/Nathan")
text = open('tagalog_dict.txt', "r")
# then read it and convert to STR
data = text.read()
# re.sub for substituting value
tagalog_word_list = re.sub(" ", "\n", data)
# I did not remove the - . as for filipino words, some words actually need -
tagalog_word_list = re.sub("\n", ",", tagalog_word_list)
tagalog_word_list = tagalog_word_list.split(",")

#lower case all the words, because it will be compared to lower case set of input words.
tagalog_lower = [w.strip().lower() for w in tagalog_word_list]
# below code removes the redundant word from dictionary
ftagalog_lower = list(dict.fromkeys(tagalog_lower))
# sorting from a to z
ftagalog_lower = sorted(ftagalog_lower)

# line by line printing before writing to new file
new_dict = '\n'.join(w for w in ftagalog_lower)
#print(new_dict)

#print(new_dict)
f = open('lower_tagalog_dict.txt', "w")
f.write(new_dict)
f.close()

#get all eng words but in singular form
english_word_list = words.words()

text = open('lower_tagalog_dict.txt', "r")
# then read it and convert to STR
data = text.read()
tagalog_word_list = re.sub("\n", ",", data)
ftagalog_lower = tagalog_word_list.split(",")

# just same process of reading and writing
text = open('remove.txt', "r")
data = text.read()
remove = re.sub("\n", ",", data)
remove = remove.split(",")
print(len(remove))

# manually removed some words that are english
# compared the english dictionary and tagalog dict
texto = open('lower_tagalog_dict.txt', "r")
datas = texto.read()
tagalog = re.sub(",", "\n", datas)
tag_list = re.sub("\n", ",", tagalog)
tag_list = tag_list.split(",")

for w in remove:
    tag_list.remove(w)


tag_list = sorted(tag_list)
tagalog_words = '\n'.join(tag_list)


f = open('lower_tagalog_dict.txt', "w")
f.write(tagalog_words)
f.close()

# got the difference or the words that are both present in eng and tagalog
difference = []
for word in ftagalog_lower:
    if word in english_word_list:
        difference.append(word)
        
diff = '\n'.join(difference)
f = open('difference.txt', "w")
f.write(diff)
f.close()


#get all plural words using codes below for english
#os.chdir("C:/Users/Nathan/TOPL finalpaper")

text = open('english_dict.txt', "r")
data = text.read()
#print(data)
english_w = re.sub("\n", ",", data)
#print(english_w)
#english_words = english_w.split(",")
print(len(english_words))
english_words = list(dict.fromkeys(english_words))


plural_words = []
# inflect.engine is for converting a word to its plural form
engine = inflect.engine()

for w in english_words:
    plural = engine.plural(w)
    plural_words.append(plural)

plural_words = [w.strip().lower() for w in plural_words]
plural_words = sorted(list(dict.fromkeys(plural_words)))
plural_str = ','.join(plural_words)
plural_str = re.sub(',', '\n', plural_str)
f = open('plural_words.txt', "w")
f.write(plural_str)
f.close()

# add the existing dict and the plural words 
all_english = english_words + plural_words
#remove redundant words, and sort from a to z as well
all_english = sorted(list(dict.fromkeys(all_english)))
all_english = ','.join(all_english)
all_english = re.sub(',', '\n', all_english)


# the final_english_dict.txt is now quite large, BUT it is more accurate.
# the main code repo does not use module like enchant anymore to check if word is english
f = open('final_english_dict.txt', "w")
f.write(all_english)
f.close()