import DB_Connect as connect  
import pandas as pd

def admin_view_bksborrowed():
    query_stmt = "SELECT bookID, bookTitle, borrowMemberID, dateDue FROM book "
    query_stmt += "WHERE borrowMemberID IS NOT NULL ORDER BY dateDue, bookID"
    return pd.read_sql_query(query_stmt, connect.db)

def admin_view_bksreserved():
    query_stmt = "SELECT bookID, bookTitle, reserveMemberID FROM book "
    query_stmt += "WHERE reserveMemberID IS NOT NULL ORDER by bookID"
    return pd.read_sql_query(query_stmt, connect.db)

def admin_view_unpaidfines():
    query_stmt = "SELECT memberID, fineAmount, fineDate FROM fine "
    query_stmt += "WHERE paymentDate IS NULL ORDER BY fineDate, memberID"
    return pd.read_sql_query(query_stmt, connect.db)

def admin_view_totalfineamount():
    query_stmt = "SELECT memberID, SUM(fineAmount) AS totalFineAmount FROM fine "
    query_stmt += "WHERE paymentDate IS NULL GROUP BY memberID"
    return pd.read_sql_query(query_stmt, connect.db)

def member_view_bksborrowed(memberID):
    query_stmt = "SELECT bookID, bookTitle, dateDue FROM book "
    query_stmt += "WHERE borrowMemberID = \"{}\" ORDER BY dateDue, bookID".format(memberID)
    return pd.read_sql_query(query_stmt, connect.db)

def member_view_bksreserved(memberID):
    query_stmt = "SELECT bookID, bookTitle FROM book "
    query_stmt += "WHERE reserveMemberID = \"{}\" ORDER BY bookID".format(memberID)
    return pd.read_sql_query(query_stmt, connect.db)

def member_view_unpaidfines(memberID):
    query_stmt = "SELECT fineDate, fineAmount FROM fine "
    query_stmt += "WHERE memberID = \"{}\" AND paymentDate IS NULL ORDER BY fineDate".format(memberID)
    return pd.read_sql_query(query_stmt, connect.db)

# Returns a string representation of the total fine amount owed by the member. 
def member_view_totalfineamount(memberID):
    query_stmt = "SELECT SUM(fineAmount) AS totalFineAmountOwed FROM fine "
    query_stmt += "WHERE memberID = \"{}\" AND paymentDate IS NULL GROUP BY memberID".format(memberID)
    amount = pd.read_sql_query(query_stmt, connect.db)
    if amount.empty:
        return "You do not have any outstanding fines."
    else:
        return str(amount["totalFineAmountOwed"][0])

