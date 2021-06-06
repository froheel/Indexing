# Importing libaries and modules
import os
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from collections import defaultdict, OrderedDict
import warnings
import codecs
import math
warnings.filterwarnings("ignore")

# Global variables
Dir1 = "C:\\Users\\KASHIF YOUSAF\\PycharmProjects\\IR-Assignment3\\corpus1\\1"
Dir2 = "C:\\Users\\KASHIF YOUSAF\\PycharmProjects\\IR-Assignment3\\corpus1\\2";
Dir3 = "C:\\Users\\KASHIF YOUSAF\\PycharmProjects\\IR-Assignment3\\corpus1\\3";
docId_mapping = None
if not os.path.isfile('docInfo.txt'):
    docId_mapping = codecs.open('docInfo.txt', 'w', "utf-8-sig")
curr_docId = 1
#limit_files_eachdir = 30

# Prints the total number of files in corpus
def verify_total_files():
    dirListing = os.listdir(Dir1)
    dirListing2 = os.listdir(Dir2)
    dirListing3 = os.listdir(Dir3)
    print(len(dirListing) + len(dirListing2) + len(dirListing3))


def process_file(file_path , docId , term_docId, dirname, filename):
    html = open(file_path, "rb").read()
    soup = BeautifulSoup(html, "html.parser")
    soup = soup.find('html')

    if soup == None:
        # No tokens; return empty position list
        return defaultdict(list)

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    # print(text)
    # print(word_tokenize(text))

    sw = nltk.corpus.stopwords.words('english')
    words_ns = []

    ps = PorterStemmer()

    # Add to words_ns all words that are in words but not in sw
    for word in word_tokenize(text):
        if word not in sw and word.isalpha():
            words_ns.append(ps.stem(word.lower()))

    # print(words_ns)

    pos = 1
    term_positions = defaultdict(list)

    length_of_doc = 0
    for word in words_ns:
        term_positions[word].append(pos)
        term_docId[word].add(docId)
        pos = pos + 1
        length_of_doc = length_of_doc + 1

    # Keeping additional information
    keeping_additional_information_file(docId, dirname, filename, length_of_doc, term_positions)
    return term_positions

    # print(sorted(term_docId.items()))


# Accept a directory name as a input, and process all files found in that directory
def process_directory(directory_path,dirname):
    global curr_docId
    doc_term_positions_list = {}
    term_docId = defaultdict(set)

    counter = 0

    for file in os.listdir(directory_path):
        print("Processed: " + file)
        term_positions = process_file(directory_path + "\\"+ file , curr_docId, term_docId, dirname, file)
        doc_term_positions_list[curr_docId] = OrderedDict(sorted(term_positions.items()))
        curr_docId = curr_docId + 1

        counter +=1
        #if counter == limit_files_eachdir:
            #break

    term_docId = OrderedDict(sorted(term_docId.items()))
    # term_docId = sorted(term_docId.items())
    doc_term_positions_list = OrderedDict(sorted(doc_term_positions_list.items()))


    writetofiles(term_docId, doc_term_positions_list,dirname)


def writetofiles(term_docId, doc_term_postions_list, dirname):

    # opening file to write posting list
    postinglist_file = codecs.open('index_'+ dirname +'_postings.txt', 'w', "utf-8-sig")
    inverted_index = codecs.open('index_' + dirname + '_terms.txt', 'w', "utf-8-sig")

    start = 0

    # for (key, value) in d.items():
    for term, set in term_docId.items():

        # write term
        inverted_index.write(term + " " + str(start) + "\n")

        # write doc frequency
        postinglist_file.write(str(len(set)) + ",")
        start += len(str(len(set))) + len(",")

        #print(f"{term} - {set}")

        # prev doc_id
        prev_doc_id = 0
        for doc_id in set:
            #print(doc_id)

            # write doc_id
            postinglist_file.write(str(doc_id-prev_doc_id) + ",")
            start += len(str(doc_id-prev_doc_id)) + len(",")
            prev_doc_id = doc_id

            # write freq of pos in doc_id
            postinglist_file.write(str(len(doc_term_postions_list.get(doc_id).get(term))) + ",")
            start += len(str(len(doc_term_postions_list.get(doc_id).get(term)))) + len(",")

            prev_pos = 0
            # for that document find the positions
            for pos in doc_term_postions_list.get(doc_id).get(term):
                #print(pos)

                # write pos
                postinglist_file.write(str(pos - prev_pos) + ",")
                start += len(str(pos - prev_pos)) + len(",")
                prev_pos = pos



        postinglist_file.write("\n")
        start += len("\r\n")
        #print("-----------------")

    postinglist_file.close()
    inverted_index.close()


def readfile(query):
    # resultant documents in result
    terms_found = set()
    result = set()
    flag_first_time = 0
    f = open("inverted_index_postings.txt",'r',30,"utf-8-sig",'ignore')
    with open('inverted_index_terms.txt','r',30,"utf-8-sig",'ignore') as inverted_index:
        term = 1
        while term:
            term = inverted_index.readline().split()
            # print(term)
            if term != [] :
                term_doc_set = set()
                start = term[1]
                term = term[0]

                if start == "0":
                    f.seek(int(start))

                postinglist = f.readline()
                #print(postinglist)
                postinglist = postinglist.split(',')
                #print(postinglist)

                # if matches the term in query then add to temporary set
                ps = PorterStemmer()
                if ps.stem(term) in query:
                    terms_found.add(ps.stem(term))

                # Number of docs contaning that term
                prevdoc = 0
                listindex = 1
                for i in range(0, int(postinglist[0])):
                    # get doc id
                    curr_docId = int(postinglist[listindex]) + prevdoc
                    prevdoc = curr_docId

                    # if matches the term in query then add to temporary set

                    if ps.stem(term) in query:
                        term_doc_set.add(curr_docId)


                    listindex += 1
                    number_of_pos = int(postinglist[listindex])
                    listindex += 1

                    prevpos = 0
                    for i in range(0,number_of_pos):
                        # read positions
                        #curr_pos = int(postinglist[listindex])+prevpos
                        #print(str(curr_docId) + "----" + term + " ----" + str(curr_pos))
                        #prevpos = curr_pos
                        listindex += 1

                # if term found then intersection
                if flag_first_time == 0 and len(term_doc_set) > 0 and len(result) == 0:
                    result = term_doc_set
                    flag_first_time = 1
                elif len(term_doc_set)> 0:
                    result = result.intersection(term_doc_set)

                # If entire query processed then no need to read rest file
                if len(query - terms_found.intersection(query)) == 0:
                    return result

        # now check if all the terms are found
        if len(query - terms_found.intersection(query)) == 0:
            return result
        else:
            return set()

def merge(index_1_filename, posting_1_filename, index_2_filename, posting_2_filename, indexnew_filename):

    # Opening files for merge

    postinglist_1 = open(posting_1_filename, 'r', 30, "utf-8-sig", 'ignore')
    postinglist_2= open(posting_2_filename, 'r', 30, "utf-8-sig", 'ignore')
    index_1 = open(index_1_filename, 'r', 30, "utf-8-sig", 'ignore')
    index_2 = open(index_2_filename, 'r', 30, "utf-8-sig", 'ignore')
    postinglist_new = codecs.open(indexnew_filename + '_postings.txt', 'w', "utf-8-sig")
    inverted_new = codecs.open(indexnew_filename + '_terms.txt', 'w', "utf-8-sig")
    offset_new = 0

    # Read index and posting for each file
    term_1 = index_1.readline().split()
    term_2 = index_2.readline().split()

    while 1==1:

        #print(term_1[0] + "---" + term_2[0])

        if term_1 == []:
            # copy term2 & its postings
            postinglist_2_split = postinglist_2.readline()

            # write
            inverted_new.write(term_2[0] + " " + str(offset_new) + "\n")
            offset_new += len(postinglist_2_split)
            postinglist_new.write(postinglist_2_split)

            # update
            term_2 = index_2.readline().split()
            if not term_2:
                break

        elif term_2 == []:
            # copy term1 and its postings
            # copy term2 & its postings
            postinglist_1_split = postinglist_1.readline()

            # write
            inverted_new.write(term_1[0] + " " + str(offset_new) + "\n")
            offset_new += len(postinglist_1_split)
            postinglist_new.write(postinglist_1_split)

            # update
            term_1 = index_1.readline().split()
            if not term_1:
                break


        else:
            if term_1[0] == term_2[0]:

                postinglist_1_split = postinglist_1.readline()
                postinglist_1_split = postinglist_1_split.split(',')

                postinglist_2_split = postinglist_2.readline()
                postinglist_2_split = postinglist_2_split.split(',')

                number_of_docs_1 = postinglist_1_split[0]
                number_of_docs_2 = postinglist_2_split[0]
                doc_poslist = defaultdict(list)

                inverted_new.write(term_1[0] + " " + str(offset_new) + "\n")

                # Number of docs contaning that term in postinglist_1
                listindex = 1
                prevdoc = 0
                for i in range(0, int(number_of_docs_1)):
                    # get doc id
                    curr_docId = int(postinglist_1_split[listindex]) + prevdoc
                    prevdoc = curr_docId


                    listindex += 1
                    number_of_pos = int(postinglist_1_split[listindex])
                    listindex += 1


                    for i in range(0, number_of_pos):
                        # read positions
                        curr_pos = int(postinglist_1_split[listindex])
                        doc_poslist[curr_docId].append(curr_pos)
                        # print(str(curr_docId) + "----" + term + " ----" + str(curr_pos))
                        listindex += 1



                # Number of docs contaning that term in postinglist_2

                listindex = 1
                prevdoc = 0
                for i in range(0, int(number_of_docs_2)):
                    # get doc id
                    curr_docId = int(postinglist_2_split[listindex]) + prevdoc
                    prevdoc = curr_docId

                    listindex += 1
                    number_of_pos = int(postinglist_2_split[listindex])
                    listindex += 1


                    for i in range(0, number_of_pos):
                        # read positions
                        curr_pos = int(postinglist_2_split[listindex])
                        doc_poslist[curr_docId].append(curr_pos)
                        # print(str(curr_docId) + "----" + term + " ----" + str(curr_pos))
                        listindex += 1


                doc_poslist = OrderedDict(sorted(doc_poslist.items()))


                # write to file
                offset_new += len(str(len(doc_poslist.items()))) + len(",")
                postinglist_new.write(str(len(doc_poslist.items())) + ',')
                prevdoc = 0
                for set in doc_poslist.items():
                    offset_new += len(str(set[0]-prevdoc)) + len(",")
                    postinglist_new.write(str(set[0] - prevdoc) + ",")
                    prevdoc = set[0]

                    offset_new +=len(str(len(set[1]))) + len(",")
                    postinglist_new.write(str(len(set[1])) + ",")
                    for pos in set[1]:
                        offset_new +=len(str(pos)) + len(",")
                        postinglist_new.write(str(pos) + ",")


                postinglist_new.write("\n")
                offset_new += len("\r\n")

                # update both index
                term_1 = index_1.readline().split()
                term_2 = index_2.readline().split()


            elif term_1[0] < term_2[0]:

                # read
                postinglist_1_split = postinglist_1.readline()


                # write
                inverted_new.write(term_1[0] + " " + str(offset_new) + "\n")
                offset_new += len(postinglist_1_split)
                postinglist_new.write(postinglist_1_split)

                # update
                term_1 = index_1.readline().split()

            elif term_1[0] > term_2[0]:
                # read
                postinglist_2_split = postinglist_2.readline()

                # write
                inverted_new.write(term_2[0] + " " + str(offset_new) + "\n")
                offset_new += len(postinglist_2_split)
                postinglist_new.write(postinglist_2_split)

                # update
                term_2 = index_2.readline().split()


# Process all 3 directories and handles the files of each directory seperately
def pre_processing():
    process_directory(Dir1,"1")
    process_directory(Dir2,"2")
    process_directory(Dir3,"3")


# merges the files using Buffers
def actual_merge(index_1, posting_1, index_2,posting_2, index_3, posting_3):
    merge(index_1, posting_1, index_2, posting_2, 'index_merge' )
    merge("index_merge_terms.txt", "index_merge_postings.txt", index_3, posting_3, 'inverted_index')

    # remove unnecessary files
    myfile = "index_merge_terms.txt"
    if os.path.isfile(myfile):
        os.remove(myfile)
    myfile = "index_merge_postings.txt"
    if os.path.isfile(myfile):
        os.remove(myfile)

# writing additional information of a file
def keeping_additional_information_file(docId, subdirectory, docName, length, term_position):
    # compute magnitude of document
    total = 0
    for term , positions in term_position.items():
        total += (len(positions) * len(positions))
    magnitude = math.sqrt(total)
    # Writing to file
    docId_mapping.write(str(docId)+ "," + subdirectory + "/" + docName + "," + str(length) + "," + str(magnitude) + "\n")


def boolean_retrieval(query):
    # tokenize the query
    sw = nltk.corpus.stopwords.words('english')
    words_ns = set()

    ps = PorterStemmer()

    # Add to words_ns all words that are in words but not in sw
    for word in word_tokenize(query):
        if word not in sw and word.isalpha():
            words_ns.add(ps.stem(word.lower()))

    # Now read the file and match
    docIds = readfile(words_ns)

    # Display output
    if len(docIds) == 0:
        print("No result found")
    else:
        # for each docId print the filename along with Dir in lexographical order
        #for docId in docIds:
         #   print(str(docId))
        if os.path.isfile('docInfo.txt'):
            docId_mapping = codecs.open('docInfo.txt', 'r', "utf-8-sig")
            while 1 == 1:
                docId_split = docId_mapping.readline()
                if not docId_split:
                    break
                docId_split = docId_split.split(',')

                # if matches the term in query then add to temporary set
                if int(docId_split[0]) in docIds:
                    print(docId_split[1])



def makefiles():
    # processing each directory seperately and creates files and also stores additional information for each file
    pre_processing()
    # merging all seperately made files for directories
    actual_merge("index_1_terms.txt", "index_1_postings.txt", "index_2_terms.txt", "index_2_postings.txt",
                 "index_3_terms.txt", "index_3_postings.txt")


def query():
    query = input("Enter query: \n")
    # Tokenize the query and print results
    boolean_retrieval(query)

def main():
    choice = input("Enter 1 to make files or 2 to query results: \n")
    if choice == '1':
        print("Delete the docInfo.txt first then call this function")
        makefiles()
    elif choice == '2':
        query()
    else:
        print("Error.Wrong Choice")

if __name__ == "__main__":
    main()

