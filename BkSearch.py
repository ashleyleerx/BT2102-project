import DB_Connect as connect
import pandas as pd
import numpy as np
from sqlalchemy import exc
import datetime as dt

# Dataframe for Book mySQL Relation Info
book_df = pd.read_sql('book', connect.db)

# Reading MongoDB Database


def mongo_output(cursor):
    outputlst = []

    for b in cursor:
        outputlst.append(b)
    return outputlst

# Splits the search_words string into diff elements in list form


def formatter(search_words):
    punct = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    if type(search_words) == str:
        new_search_words = ""
        for c in search_words:
            if c not in punct:
                new_search_words += c

        new_search_words = new_search_words.split(" ")
    return new_search_words


# MongoDB Reader Function
def mongoreader(cursor, bk_id, sort_type):
    for book in cursor:
        if book["_id"] == bk_id:
            return book[sort_type]


# print(type(mongoreader(connect.collection.find({}), 777, "_id")))


# Book Similarity Sorting
def similarity_sort(book_dict, search_words, sort_type):
    keylst = []
    reorderlst = []
    for bkID, info in book_dict.items():
        entry = [bkID, 0]
        for word in formatter(search_words):
            for indiv_keyword in formatter(mongoreader(connect.collection.find({}), bkID, sort_type)):
                if indiv_keyword.lower() == word.lower():
                    entry[1] += 1
        keylst.append(entry)
    keylst.sort(key=lambda entry: entry[1], reverse=True)
    for i in keylst:
        reorderlst.append(i[0])
    df = pd.DataFrame.from_dict(book_dict, orient="index")
    df = df.reindex(reorderlst)
    return df


# Does a simple search
'''
Search_words can either take in a string or a list.
Will return a dictionary with bookID as the key and value containing the
rest of the relevant information in a list form

Note: Cannot use keyword "in" to check if certain word inside book title
e.g. "on" --> matches with "Action" ==> Not an ideal result
'''


def simple_search(search_words):
    match_dict = {}
    # splits search words into indiv elements in list for looping
    search_words = formatter(search_words)
    for word in search_words:
        # looping through pandas dataframe (of books)
        for index, row in book_df.iterrows():
            # looping through indiv word in booktitle
            for title_indiv_word in formatter(row["bookTitle"].lower()):
                if word.lower() == title_indiv_word:
                    if row["borrowMemberID"] == None:
                        if row["reserveMemberID"] == None:
                            # Book not borrowed and not reserved
                            match_dict[row["bookID"]] = [
                                row["bookTitle"], "Available", "Not Reserved", "NIL"]
                        else:
                            # Book not borrowed but is reserved
                            match_dict[row["bookID"]] = [
                                row["bookTitle"], "Available", "Reserved", "NIL"]
                    else:
                        if row["reserveMemberID"] == None:
                            # Book borrowed and not reserved
                            match_dict[row["bookID"]] = [
                                row["bookTitle"], "On Loan", "Not Reserved", row["dateDue"]]
                        else:
                            # Book borrowed but is reserved
                            match_dict[row["bookID"]] = [
                                row["bookTitle"], "On Loan", "Reserved", row["dateDue"]]
    return match_dict


'''
Helper function to check if the book is borrowed or reserved and to add it to the dictionary

Why we cannot use adv_helper for simple search despite the similarities in code:
    param "b" is a mongo_output, comparoison in simple search is done slightly differently in this respect
'''


def adv_helper(match_dict, b):
    for index, row in book_df.iterrows():
        if row["bookID"] == b["_id"]:
            if row["borrowMemberID"] == None:
                if row["reserveMemberID"] == None:
                    # Book not borrowed and not reserved
                    match_dict[row["bookID"]] = [
                        row["bookTitle"], "Available", "Not Reserved", "NIL"]
                else:
                    # Book not borrowed but is reserved
                    match_dict[row["bookID"]] = [
                        row["bookTitle"], "Available", "Reserved", "NIL"]
            else:
                if row["reserveMemberID"] == None:
                    # Book borrowed and not reserved
                    match_dict[row["bookID"]] = [
                        row["bookTitle"], "On Loan", "Not Reserved", row["dateDue"]]
                else:
                    # Book borrowed but is reserved
                    match_dict[row["bookID"]] = [
                        row["bookTitle"], "On Loan", "Reserved", row["dateDue"]]
    return match_dict


'''
List of options for Filter:
    - "Title" -- should take in a string
    - "ISBN"  -- should take in a string, and only can be 1 ISBN (i.e. cannot do something like "193518217X, 1933988509")
    - "PageCount" -- should take in an integer or string of NUMBERS
    - "PublishedDate" -- should take in datetime object
    - "Categories" -- should take in a string of 1 + category/categories
    - "Authors" -- should take in a string of 1 + author/authors

Extra param only applies for Pagecount, PublishedDate,
'''


def advance_search(search_words, filt, *extra_param):
    match_dict = {}

    # advanced searching by title will be same as a simple search
    if filt == "title":
        return simple_search(search_words)

    # advanced searching by isbn: only 1 entry, can be partial isbn
    elif filt == "isbn":
        for b in mongo_output(connect.collection.find(
                {"isbn": {"$regex": search_words}})):
            adv_helper(match_dict, b)
        return match_dict

    # advanced searching by pageCount: can either choose books with lesser page_count or greater page_count or equal page_count
    elif filt == "pagecount":
        nrpages = int(search_words)

        # Returns books with pages equal to or lesser than specified amount
        if extra_param[0] == "lesser":
            ep = "$lte"

        # Returns books with pages equal to or greater than specified amount
        elif extra_param[0] == "greater":
            ep = "$gte"

        # Returns books with pages equal to specified amount
        elif extra_param[0] == "equal":
            ep = "$eq"

        else:
            return "Give either lesser, greater or equal in the extra_param section"

        for b in mongo_output(connect.collection.find({"pageCount": {"{}".format(ep): nrpages}})):
            adv_helper(match_dict, b)
        return match_dict

    # advanced searching by publication date
    elif filt == "publisheddate":

        # Returns entries with publication date before or on specified date
        if extra_param[0] == "before":
            ep = "$lte"

        # Returns entries with publication date after or on specified date
        elif extra_param[0] == "after":
            ep = "$gte"

        # Returns entries with publication date exactly on specified date
        # Note for datetime equals that timezone matters (e.g. dt.datetime(2010,11,15) != dt.datetime(2010,11,15,8))
        elif extra_param[0] == "equal":
            ep = "$eq"

        else:
            return "Give either lesser, greater or equal in the extra_param section"

        for b in mongo_output(connect.collection.find({"publishedDate": {"{}".format(ep): search_words}})):
            adv_helper(match_dict, b)
        return match_dict

    # advanced search for categories
    elif filt == "categories":
        for b in mongo_output(connect.collection.find({"categories": {"$elemMatch": {"$regex": search_words, "$options": 'i'}}})):
            adv_helper(match_dict, b)
        return match_dict

    # advanced search for authors
    elif filt == "authors":
        for b in mongo_output(connect.collection.find({"authors": {"$elemMatch": {"$regex": search_words, "$options": 'i'}}})):
            adv_helper(match_dict, b)
        return match_dict

    else:
        return "Input an appropriate filter query"


# print(simple_search("flex on java"))
# print(book_df.loc[book_df["bookID"] == 777])
# print(advance_search(dt.datetime(2010, 11, 15, 8), "publisheddate", "equal"))
#print(similarity_sort(advance_search("Steve L", "authors"), "Steve L", "authors"))
# congo = connect.collection.find({})
# for b in congo:
#     print(b.keys())

# print(mongo_output(connect.collection.find(
# {"isbn": {"$regex": '16'}})))
# for b in mongo_output(connect.collection.find(
#         {"isbn": {"$regex": "19323945"}})):
#     bookinfo = book_df.loc[book_df["bookID"] == b["_id"]]
#     print(bookinfo)
# print(type(bookinfo["borrowMemberID"]))
# if bookinfo["bookID"] == 77:
#     print(bookinfo)

print(similarity_sort(simple_search("Android"), "Android", "title"))
