import os
import json
from afinn import Afinn
import nltk
from collections import defaultdict
from nltk.corpus import stopwords

stopwords = set(stopwords.words('english'))


# Import the necessary packages and modules
# import matplotlib
# matplotlib.use('Agg')
# import matplotlib.pyplot as plt
# import numpy as np


# Class for keywords
class Keywords:

    # positive_count
    # negative_count

    # Constructor
    def __init__(self, n):
        self.name = n
        self.positive_count = 0
        self.negative_count = 0
        self.total_keys = set()
        self.total_dict = {}

    # Adds to positive tweets
    def add_total(self, sent_score, tw_name):
        if sent_score > 0:
            self.positive_count += 1
        else:
            self.negative_count += 1

        self.total_dict[tw_name] = int(sent_score)
        self.total_keys.add(tw_name)

    def get_total_keys(self):
        return self.total_keys

    def get_score(self, tw_name):
        return self.total_dict[tw_name]


# Cleans up OSE_REU directory
def cleaner():
    # Open a path dir
    OSU_dir = os.listdir("/home/hedmund/OSU_REU/")

    for dir in OSU_dir:
        os.remove("/home/hedmund/OSU_REU/" + str(dir))


# creates tdm
def TDM(total_words, s):
    rows = defaultdict()
    cols = []
    sorted_list = []
    counter = 0

    # print the cols
    for n in s:
        print('{0:^30}'.format(str(n)), end="")

    # list of words (rows)
    for key in total_words:
        rows[key] = list(range(len(s)))
        sorted_list.append(key)
        counter = 0

        for item in s:
            rows[key][counter] = total_words[key].count(item)
            # print(str(key) + ": " + str(rows[key][counter]) + "\t"+ "\t"),
            counter += 1

    # sorted list
    sorted_list.sort()

    # list of words (rows)
    for key in sorted_list:
        counter = 0
        print("\t"),
        for item in s:
            print('{0:^30}'.format(str(rows[key][counter])), end="")
            counter += 1
        print(("|" + str(key) + "|"))
        print("------------------------------------------------------------------------------"
              "---------------------------------", end="")

    size_of_cols = len(s)


# Strip tweet of special characters and words
def text_parser(un_stripped, tweet_indent, nike_object, Snapchat_object, p_list, n_list, senti_map):
    # Empty string
    string_temp = ""
    Tweet_line = ""
    stripped_line = ""
    matches = []
    at_symbol_found = False
    p_count = 0
    n_count = 0

    # Iterate over the list of words and strip unnecessary characters
    for word in un_stripped:
        Tweet_line = Tweet_line + str(word) + " "

    # loop over big string to parse words
    for letter in Tweet_line:

        # converts characters to letter and makes it uppercase
        letter = str(letter)
        letter = letter.upper()

        # if letter than add temp string
        if letter.isalpha() or letter == "@":
            if letter == "@":
                at_symbol_found = True

            string_temp += letter


        # A space occurred so put whatever is in string_temp into dictionary
        elif letter == " ":

            # Gets rid of handle names
            if at_symbol_found == True:

                at_symbol_found = False
                string_temp = ""

            # only counting words that are greater than length 2 and isnt a stopword
            elif len(string_temp) > 2 and string_temp.lower() not in stopwords:

                # removes links
                if string_temp.find("HTTPS") != -1:
                    string_temp = ""
                # is a word so needs to be map to respective website and occurence updated
                else:
                    stripped_line = stripped_line + string_temp.lower() + " "
                    # print(lemmatiser.lemmatize(string_temp, "v"))

                    if string_temp in p_list:
                        p_count += 1
                        # print("Pos: " + string_temp)

                    elif string_temp in n_list:
                        n_count += 1
                        # print("Neg: " + string_temp)

                    else:
                        pass
                        # print("UN: " + string_temp)

                    string_temp = ""


            else:
                # clears string
                string_temp = ""

        # not a character
        elif letter.isalpha() == False:
            pass

    print(tweet_indent + " " + senti_map[tweet_id])

    # Check if tweet is usuable
    list_of_keywords = ["NIKE", "ADIDAS", "SHOES", "SHOE"]

    # upper case stripped line
    stripped_line = stripped_line.upper()

    # Finds all keywords in tweet
    for x in list_of_keywords:
        if stripped_line.find(x) == -1:
            pass
        else:
            matches.append(x)

    if len(matches) == 0 or "SHOES" not in matches:
        return "False"
    else:
        return stripped_line


# Cleans OSU_REU directory
cleaner()

# External file for converted json file
# Converted_file = open("/home/hedmund/OSU_REU/converted_results.txt", "w", encoding="utf8")
# keep a list of files to be deleted
removal_list = []
number_of_files = 0
count = 0

# Open a path dir
total_dir = os.listdir("/home/hedmund/Shoes_Data/")
print(total_dir)

#################################### MAIN #########################################

# plt.plot([1,2,3,4])
# plt.ylabel('some numbers')
# plt.show()


sent_words = Afinn(emoticons=True)
# Declare Keywords objects
nike_object = Keywords("Nike")
adidas_object = Keywords("Adidas")
reebok_object = Keywords("Reebok")
Spam_list = [line.rstrip().upper() for line in open("/home/hedmund/Words/spam.txt", "r")]
total_tweets = {}
sent_mapper = {}
# Check if tweet is usuable
list_of_keywords = ["NIKE", "ADIDAS", "REEBOK", "SHOES", "SHOE"]

####################################################################################


################## STEP 1: Convert Flume Data into JSON format ######################

# Writes to results files
Tweet_file = open("/home/hedmund/OSU_REU/results.json", "a")

# Reads in Flume Data and put the Data into .json format
for FlumeData_files in total_dir:
    in_dir = os.listdir("/home/hedmund/Shoes_Data/" + str(FlumeData_files) + "/")
    for flume in in_dir:
        FlumeData_info_input = open("/home/hedmund/Shoes_Data/" + str(FlumeData_files), "r")
        FlumeData_info = FlumeData_info_input.read()
        Tweet_file.write(FlumeData_info)

Tweet_file.close()

####################################################################################

################## STEP 2: Iterate over .JSON file and Gather the text ######################

# List for stripped tweets
tweet = []
split_words = []
strip_tweet = ""

# IF contains multiple key words then do a function

json_file = open("/home/hedmund/OSU_REU/results.json")
lines = json_file.readlines()

for i in lines:

    try:
        # loads in json formatted line
        converted_line = json.loads(i)

        if "full_text" in converted_line:
            # Gathers english tweets and parses tweet
            tweet_text = converted_line["full_text"].upper()

        elif "retweeted_status" in converted_line:
            # Gathers english tweets and parses tweet
            tweet_text = converted_line["retweeted_status"]["text"].upper()
        else:
            tweet_text = converted_line["text"].upper()

        if converted_line["lang"] == "en" and (list_of_keywords[0] in tweet_text or list_of_keywords[1] in tweet_text
                                               or list_of_keywords[2] in tweet_text or list_of_keywords[
                                                   3] in tweet_text or list_of_keywords[4] in tweet_text):

            if any(ext in tweet_text for ext in Spam_list) == False:

                if sent_words.score(tweet_text) != 0:
                    try:
                        total_tweets[tweet_text]
                    except KeyError:
                        total_tweets.setdefault(tweet_text, 0)

                        if total_tweets.get(tweet_text, "None") == "None":
                            total_tweets.setdefault(tweet_text, 0)

                        total_tweets[tweet_text] = int(total_tweets[tweet_text]) + 1

                    hold = int(total_tweets[tweet_text])
                    hold += 1
                    total_tweets[tweet_text] = hold

                    # Nike, Reebok, Adidas seperator
                    if "NIKE" in tweet_text:
                        nike_object.add_total(sent_words.score(tweet_text), tweet_text)
                    elif "ADIDAS" in tweet_text:
                        adidas_object.add_total(sent_words.score(tweet_text), tweet_text)
                    elif "REEBOK" in tweet_text:
                        reebok_object.add_total(sent_words.score(tweet_text), tweet_text)
                    else:
                        pass

            # split_words = tweet_text.split()
            # strip_tweet = text_parser(split_words, tweet_id, nike_object, adidas_object, pos_list, neg_list,sent_mapper)

            # if strip_tweet == "False":
            # print("Not Valid: " + tweet_text)
            # pass
            # else:
            # tweet.append(strip_tweet)
            # print("Valid: " + strip_tweet + ":  " + tweet_id)

    except KeyError:
        print("Invalid")

for x in ["NIKE", "ADIDAS", "REEBOK"]:
    if x == "NIKE":
        for i in nike_object.get_total_keys():
            print("-----------------------------------///// " + str(x) + "/////-----------------------------------")
            if nike_object.get_score(i) > 0:
                print("Positive: ", str(i), ": ", sent_words.score(i) * total_tweets[str(i)], ": ",
                      total_tweets[str(i)])
                print("-----------------------------------------------------")
            else:
                print("Negative: ", str(i), ": ", sent_words.score(i) * total_tweets[str(i)], ": ",
                      total_tweets[str(i)])
                print("-----------------------------------------------------")
    elif x == "ADIDAS":
        for i in adidas_object.get_total_keys():
            print("-----------------------------------///// " + str(x) + "/////-----------------------------------")
            if adidas_object.get_score(i) > 0:
                print("Positive: ", str(i), ": ", sent_words.score(i) * total_tweets[str(i)], ": ",
                      total_tweets[str(i)])
                print("-----------------------------------------------------")
            else:
                print("Negative: ", str(i), ": ", sent_words.score(i) * total_tweets[str(i)], ": ",
                      total_tweets[str(i)])
                print("-----------------------------------------------------")
    else:
        for i in reebok_object.get_total_keys():
            print("-----------------------------------///// " + str(x) + "/////-----------------------------------")
            if reebok_object.get_score(i) > 0:
                print("Positive: ", str(i), ": ", sent_words.score(i) * total_tweets[str(i)], ": ",
                      total_tweets[str(i)])
                print("-----------------------------------------------------")
            else:
                print("Negative: ", str(i), ": ", sent_words.score(i) * total_tweets[str(i)], ": ",
                      total_tweets[str(i)])
                print("-----------------------------------------------------")
####################################################################################

################## STEP 3: WRITE STRIPPED TWEETS to .txt file ######################

count = 0
number_of_files = 0

# External file for converted json file
Converted_file = open("/home/hedmund/OSU_REU/converted_results.txt", "w", encoding="utf8")

# writes the tweets to external file
for x in tweet:
    Converted_file.write('{0}\n'.format(x))

Converted_file.close()
####################################################################################

