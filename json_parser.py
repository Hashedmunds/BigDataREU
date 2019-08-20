#!/usr/bin/env python
#-*- coding: utf-8 -*-
import re
import time
from collections import Counter
import scipy.stats as stats
from hash_tools import hash_tools
from nltk.corpus import stopwords
stopwords = set(stopwords.words('english'))


class Node:
    def __init__(self, name,score, date, brand):
        self.tweet_name = name
        self.tweet_score = score
        self.tweet_date = date
        self.tweet_brand = brand
        self.tweet_count = 1

        #Checks to see if tweet is positive or negative
        if score > 0:
            self.tweet_view = "Positive"
        else:
            self.tweet_view = "Negative"

    def get_name(self):
        return self.tweet_name
    def get_score(self):
        return self.tweet_score
    def get_date(self):
        return self.tweet_date
    def get_view(self):
        return self.tweet_view
    def get_brand(self):
        return self.tweet_brand
    def get_count(self):
        return self.tweet_count
    def update_count(self):
        self.tweet_count = int(self.tweet_count) + 1

#Class for keywords
class Keywords:

    #Constructor
    def __init__(self, n):
        self.name = n
        self.tweet_days = set()
        self.total_keys = set()
        self.total_dict = {} #tw name and count

    def get_total_key(self):
        return self.total_keys

    def concord_file_write(self):
        output = open("/home/hedmund/OSU_REU/concardence.txt", "w+")
        output2 = open("/home/hedmund/Words/Stock_data.txt", "r")

        for day in sorted(self.total_dict.keys()):
            output.write("\t".join([day,str(sum(Counter(self.total_dict[day]).values()))]))
            output.write("\n")

        x1 = [float(sum(Counter(self.total_dict[day]).values())) for day in sorted(self.total_dict.keys()) if "Sat" not in day and "Sun" not in day and "04 Jul Wed" not in day]
        x2 = [float(line.strip("\n"))for line in output2]
        #day != "09 Jun Sat" and day != "10 Jun Sun" and day != "16 Jun Sat" and day != "17 Jun Sun"

        tau, p_value = stats.kendalltau(x1, x2)
        output.write(str(tau))
        output.write("\n")

        print("\n",str(tau),"\n")

        output.close()
        output2.close()

    def concord(self,tweet_name,day,brand):
        if self.total_dict.get(day, 0) == 0:
            self.total_dict[day] = list()

        self.total_dict[day].append(tweet_name)

    #Adds to positive tweets
    def add_total(self, sent_score, tw_name, day):
        found = False

        #Date doesnt exist yet
        if self.total_dict.get(day, 0) == 0:
            #self.total_dict[day] = set()
            self.total_dict[day] = list() # 0
            self.total_dict[day].append(set()) #total tweets
            self.total_dict[day].append(0) #positive tweets count #1
            self.total_dict[day].append(0) #negative tweets count #2
            self.total_dict[day].append(0.0)  # total positive score
            self.total_dict[day].append(0.0)  # total negative score
            self.total_dict[day].append(0) #total tweets

            self.total_dict[day][0].add(Node(tw_name, sent_score, day, self.name))

            self.total_keys.add(tw_name)
            self.tweet_days.add(day)
        #Date already exist
        else:
            for i in self.total_dict[day][0]:
                if tw_name == i.get_name() and i.get_date() == day:
                    i.update_count()
                    found = True
                    break

            if found == False:
                (self.total_dict[day])[0].add(Node(tw_name, sent_score, day, self.name))

        self.total_dict[day][5] += 1

        if sent_score > 0:
            self.total_dict[day][1] += 1
            self.total_dict[day][3] += float(sent_score)
        else:
            self.total_dict[day][2] += 1
            self.total_dict[day][4] += float(sent_score)

    def sent_avg(self):
        # External file for converted json file
        Converted_file = open("/home/hedmund/OSU_REU/sent_avg_results.txt", "a+", encoding="utf8")
        # writes the tweets to external file
        Converted_file.write("\t".join(["Brand", "Average Positive", "Average Negative", "Total Count"]))
        Converted_file.write('\n')
        for key in sorted(self.tweet_days):
            Converted_file.write(
                "\t".join([key + " " + self.name, str((self.total_dict[key][3])/self.total_dict[key][1]),
                           str((self.total_dict[key][2])/self.total_dict[key][1]),
                           str(self.total_dict[key][1]+self.total_dict[key][2])]))
            Converted_file.write("\n")

    def get_all_tweets(self):
        for day in sorted(self.tweet_days):
            for i in self.total_dict[day][0]:
                print("-----------------------------------///// " + str(self.name) + "/////-----------------------------------")
                print("Tweet: ", i.get_name())
                print("Sentiment View: ", str(i.get_view()))
                print("Sentiment Score: ", str(int(i.get_score())))
                print("Sentiment Value: ", str(i.get_score() * i.get_count()))
                print("Count: ", str(i.get_count()))
                print("Brand: ", i.get_brand())
                print("Date: ", i.get_date())
                print("-----------------------------------------------------")

    def write_to_file(self):
        # External file for converted json file
        Converted_file = open("/home/hedmund/OSU_REU/converted_results.txt", "a+", encoding="utf8")
        Converted_file2 = open("/home/hedmund/OSU_REU/converted_text.txt", "a+", encoding="utf8")
        # writes the tweets to external file
        for key in sorted(self.tweet_days):
            for x in self.total_dict[key][0]:
                Converted_file.write("\t".join(
                    [x.get_name(), str(x.get_score()), str(x.get_count()), x.get_date() + " " + x.get_brand(), ""]))
                Converted_file.write("\n")
                Converted_file2.write("\t".join(
                    [x.get_name(), x.get_brand(), x.get_date(), ""]))
                Converted_file2.write("\n")
        Converted_file.close()
        Converted_file2.close()

    def print_totals(self, s_flag):
        #stockdata
        if s_flag == 0:
            output2 = open("/home/hedmund/Words/nike_Stock_data.txt", "r")
        else:
            output2 = open("/home/hedmund/Words/adidas_stock_data.txt", "r")

        total_tweets = [float(self.total_dict[day][5]) for day in sorted(self.total_dict.keys()) if "Sat" not in day and "Sun" not in day and "04 Jul Wed" not in day]
        stock_data = [float(line.strip("\n")) for line in output2]
        output2.close()


        # External file for converted json file
        Converted_file = open("/home/hedmund/OSU_REU/sent_results.txt", "a+", encoding="utf8")
        # writes the tweets to external file
        Converted_file.write("\t".join(["Brand","Positive Count","Negative Count"]))
        Converted_file.write('\n')
        x1 = []
        x2 = []
        Pos_sent_total = []
        Neg_sent_total = []
        Converted_file.write(self.name)
        Converted_file.write("\n")
        for key in sorted(self.tweet_days):
            Converted_file.write("\t".join([key+" "+self.name,str(self.total_dict[key][1]),str(self.total_dict[key][2])]))
            x1.append(float(self.total_dict[key][1])) #positive count
            x2.append(float(self.total_dict[key][2]))   #negative count
            Pos_sent_total.append(float(self.total_dict[key][3])) #sent pos total count
            Neg_sent_total.append(float(self.total_dict[key][4]))  # sent pos total count
            Converted_file.write("\n")
            Converted_file.write("\n")

        #pos tweet count vs neg tweet count
        Converted_file.write("Pos Tweet Count vs Neg Tweet Count Tau: ")
        tau, p_value = stats.kendalltau(x1, x2)
        Converted_file.write(str(tau))
        Converted_file.write("\n")
        # Total Neg Sent Score vs Total Pos Sent Score
        Converted_file.write("Total Neg Sent Score vs Total Pos Sent Score Tau: ")
        tau, p_value = stats.kendalltau(Pos_sent_total, Neg_sent_total)
        Converted_file.write(str(tau))
        Converted_file.write("\n")
        # stock data vs total tweet count
        Converted_file.write("Total Tweets vs Stock Market Tau: ")
        tau, p_value = stats.kendalltau(stock_data, total_tweets)
        Converted_file.write(str(tau))
        Converted_file.write("\n")


    def get_total_keys(self):
        return self.total_keys

    def get_total_dict(self):
        return self.total_dict

# def write_to_file(total_dict):
#     # External file for converted json file
#     Converted_file = open("/home/hedmund/OSU_REU/converted_results.txt", "a+", encoding="utf8")
#
#     # writes the tweets to external file
#     for key in total_dict.keys():
#         for x in total_dict[key][0]:
#             Converted_file.write("\t".join([x.get_name(), str(x.get_score()),str(x.get_count()),x.get_date() +" " +x.get_brand(),""]))
#             Converted_file.write("\n")
#     Converted_file.close()

#Strip tweet of special characters and words
#def text_parser(un_stripped, tweet_indent, nike_object, Snapchat_object, p_list, n_list, senti_map):
def text_parser(un_stripped, total_words, en_words):

    #Empty string
    stripped_line = ""
    at_symbol_found = False

    un_stripped = un_stripped.replace("\t", " ").replace("\n", " ")
    #Strip data
    un_stripped = re.sub(r"[^A-Za-z0-9]+"," ",re.sub(r"(HTTPS\S+)|(@\S+)|(#\S+)", " ", un_stripped))

    for word in un_stripped.split():
        word = word.lower()
        if len(word) > 2 and word not in stopwords and en_words.get(word, 0) >= 1:
            en_words[word] = en_words.get(word,0) + 1
            total_words.add(word)


start = time.time()

#Cleans up OSE_REU directory
hash_tools.cleaner()
####################################################################################
################## Reads in files ######################
hash_tools.reader()
####################################################################################
################## Sentiment Analysis ######################
hash_tools.sent_an(Keywords("Nike"), Keywords("Adidas"), Keywords("Reebok"))
#hash_tools.concordance(Keywords("Nike")).concord_file_write()
####################################################################################
# run your code
end = time.time()
elapsed = end - start
print(elapsed)
