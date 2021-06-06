# Indexing
Python along with it's imported libraries are used to implement Indexing and Boolean Retrieval from the Indexes.
PyChram is utilized as the IDE. Just press 1 to create the required index files and 2 for Boolean retrieval.

## Pre-Processing
1) Dir1, Dir2, Dir3 variables in Main.py need to point to the corpus1 Directories 1,2 and 3 respectively.
2) 3495 documents of type HTML are stored in corpus1 Folder.
3) Each document is processed by extracting only the text from it and then creating tokens.
4) Stop words are removed from the token list.

## Creating Inverted Index
1) Each directory will have it's own inverted index and posting list.
2) Delta encoding is used to store the posting list to reduce space.

## Merging Inverted Index
1) The 3 inverted indexes along with their posting lists are merged together in a single inverted index and posting list.
2) Buffered Readers and Writers are used to accomplish this task.
3) inverted_index_terms.txt and inverted_index_postings.txt will be created as the result.

## Keeping additional Information
1) Each document is assigned a unique docId in the corpus.
2) A single file known as docInfo.txt will be created that stores information about each file.
3) docID,sub_directory/documentName,documentLength,magnitudeofDocument is the format of storage for docInfo.txt

## Boolean Retrieval
1) Take Input from user as query.
2) Search that query in the final inverted_index_terms.
3) If it is found then display the documents that contain all the terms.
4) Output is the form of: Sub_directory/documentName or No Result.

## Running Code
![code](https://github.com/froheel/Indexing/blob/main/outputs_on_entire_corpora/files_created_on_entire_corpora_successfully.PNG)
