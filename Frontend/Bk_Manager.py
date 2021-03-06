import DB_Connect as connect 
import bookborrow as borrow

connection = connect.db.connect()

# Returns a value from the SQL database.
def result(stmt):
    return connection.execute(stmt).fetchall()[0][0]

# Extends borrowing by 4 weeks provided the book has not been reserved.
def extend_borrowing(bookID, memberID):
    borrowerID = result("SELECT borrowMemberID FROM book WHERE bookID = {}".format(bookID))
    reserverID = result("SELECT reserveMemberID FROM book WHERE bookID = {}".format(bookID))
    if borrowerID == memberID:
        if reserverID == None:
            update_stmt = "UPDATE book SET dateDue = DATE_ADD(dateDue, INTERVAL 4 WEEK) WHERE bookID = {}".format(bookID)
            connection.execute(update_stmt)
            newDueDate = result('SELECT dateDue FROM book WHERE bookID = {}'.format(bookID))
            return "Your due date has been extended by 4 weeks to {}.".format(newDueDate)
        return "This book is reserved. No extension of due date."
    else:
        return "You have not borrowed this book."

#Edited, cancel the confirmation input
def cancel_reservation(bookID, memberID):
    borrowerID = result("SELECT borrowMemberID FROM book WHERE bookID = {}".format(bookID))
    reserverID = result("SELECT reserveMemberID FROM book WHERE bookID = {}".format(bookID))
    if reserverID == memberID:
        update_stmt = "UPDATE book SET reserveMemberID = NULL WHERE bookID = {}".format(bookID)
        connection.execute(update_stmt)
        
# check status of the book (borrowed/ available)
def check_status(bookID):
    borrowerID = result("SELECT borrowMemberID FROM book WHERE bookID = {}".format(bookID))
    if borrowerID == None:
        return True
    else:
        return False
    
def return_book(bookID, memberID):
    borrowerID = result("SELECT borrowMemberID FROM book WHERE bookID = {}".format(bookID))
    if borrowerID == memberID:
        update_stmt = "UPDATE book SET borrowMemberID = NULL, dateDue = NULL WHERE bookID = {}".format(bookID)
        connection.execute(update_stmt)
        returnedBook = result("SELECT bookTitle FROM book WHERE bookID = {}".format(bookID))
        return "{} is returned.".format(returnedBook)
    else:
        return "You have not borrowed this book."