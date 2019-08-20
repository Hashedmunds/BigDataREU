


########## text parser ######
#total_words = dict(set)
total_words = defaultdict(list)
list_of_files_names = []

# Open a path dir
total_dirs = os.listdir("/home/hedmund/OSU_REU/")

for i in total_dirs:
    # Do nothing
    if i.find(".txt") == -1:
        continue
    else:
        list_of_files_names.append(i)
        text_parser(total_words,i) #passed in dictionary



#######Calls tdm function####
TDM(total_words, list_of_files_names)


#creates tdm
def TDM(total_words, s):

    rows = defaultdict()
    cols = []
    sorted_list = []
    counter = 0

    #print the cols
    for n in s:
        print('{0:^30}'.format(str(n)), end="")


    # list of words (rows)
    for key in total_words:
        rows[key] = list(range(len(s)))
        sorted_list.append(key)
        counter = 0

        for item in s:
            rows[key][counter] = total_words[key].count(item)
            #print(str(key) + ": " + str(rows[key][counter]) + "\t"+ "\t"),
            counter += 1

    #sorted list
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

