import DB_Connect as connect
import pandas as pd
from FP_Manager import no_unpaid_fine

connection = connect.db.connect()
db = connect.db

def is_borrowed(book_id):
    member_id = pd.read_sql_query(f"SELECT borrowMemberID\
                                    FROM Book WHERE bookID = {book_id}",db)
    if member_id.isnull().values.any():
        return False
    else:
        return True

def borrow_book(book_id, member_id):
    if is_borrowed(book_id):
        return "Cannot borrow"
        # if not is_reserved(book_id):
        #     response = input("The book is borrowed but is available for reserving. Would you like to reserve?\n")
        #     if response == "Yes":
        #         return reserve_book(book_id, member_id)
        #     else:
        #         return "Not reserving book"
        # else:
        #     return "Cannot borrow and no reservation available."
    elif not no_unpaid_fine(member_id):
        return "Pay your fines first!"
    else:
        count_df = pd.read_sql_query(f"SELECT COUNT(borrowMemberID) AS count \
                                        FROM Book WHERE borrowMemberID = \"{member_id}\"",db)
        count_value = count_df.values[0][0]

        if count_value == 4:
            return "The user has borrowed a maximum of 4 books"
        else:
            statement = f"UPDATE BOOK SET borrowMemberID = \"{member_id}\", dateDue = DATE_ADD(CURDATE(), INTERVAL 4 WEEK) \
                                WHERE bookID = {book_id}"
            connection.execute(statement)
            return "Borrowing succeeded"

def is_reserved(book_id):
    member_id = pd.read_sql_query(f"SELECT reserveMemberID FROM Book \
                                    WHERE bookID = {book_id}", db)
    if member_id.isnull().values.any():
        return False
    else:
        return True

def same_person_reserving(book_id, reserve_member_id):
    borrow_member_id_df = pd.read_sql_query(f"SELECT borrowMemberID FROM Book \
                                    WHERE bookID = {book_id}", db)
    borrow_member_id = borrow_member_id_df.values[0][0]
    if borrow_member_id == reserve_member_id:
        return True
    else:
        return False
    
def reserve_book(book_id, member_id):
    if is_reserved(book_id):
        return "Book unavailable"
    elif not is_borrowed(book_id):
        return "Book borrowing available"
    elif not no_unpaid_fine(member_id):
        return "Pay your fines first!"
    elif same_person_reserving(book_id, member_id):
        return "Cannot reserve if you borrowed"
    else:
        statement = "UPDATE book SET reserveMemberID = \"{}\" WHERE bookID = {}".format(member_id, book_id)
        connection.execute(statement)
        return "Book reserved"
    
def is_max_book(member_id):
    count_df = pd.read_sql_query(f"SELECT COUNT(borrowMemberID) AS count \
                                        FROM Book WHERE borrowMemberID = \"{member_id}\"",db)
    count_value = count_df.values[0][0]

    if count_value >= 4:
        return True
    
    else:
        return False
    


