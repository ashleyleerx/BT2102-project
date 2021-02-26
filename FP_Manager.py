import DB_Connect as connect  
import pandas as pd
from datetime import date

connection = connect.db.connect()

#Adds new fine entries to the fine table (due date yesterday) and cancels the book reservations of these fined users.
def new_fine():
    insert_stmt = "INSERT INTO fine "
    insert_stmt += "(SELECT borrowMemberID, COUNT(*) as fineAmount, NULL, CURRENT_DATE() as fineDate FROM book "
    insert_stmt += "WHERE dateDue = (SELECT DATE_ADD(CURRENT_DATE(), INTERVAL -1 DAY)) GROUP BY borrowMemberID)"
    connection.execute(insert_stmt)
    cancel_res_stmt = "UPDATE book SET reserveMemberID = NULL WHERE reserveMemberID IN "
    cancel_res_stmt += "(SELECT memberID FROM fine WHERE paymentDate IS NULL)"
    connection.execute(cancel_res_stmt)
    return "New fines added to system."

#Update fine before adding new fines. Use new_fine() only after update_fine().  
def update_fine():
    fines_df = pd.read_sql_query("SELECT * FROM fine", connect.db)

    query_stmt = "SELECT borrowMemberID, COUNT(*) as fineAmount, DATE_ADD(dateDue, INTERVAL 1 DAY) as fineDate "
    query_stmt += "FROM book WHERE dateDue IS NOT NULL AND dateDue NOT BETWEEN "
    #8 weeks taking into account 4 weeks borrow time + 4 weeks extension
    query_stmt += "DATE_ADD(CURRENT_DATE(), INTERVAL -1 DAY) AND DATE_ADD(CURRENT_DATE(), INTERVAL 8 WEEK) "
    query_stmt += "GROUP BY borrowMemberID, fineDate"
    overdueBooks_df = pd.read_sql_query(query_stmt, connect.db)

    overdueBooks_df_grouped = overdueBooks_df.groupby(["borrowMemberID", "fineDate"])

    for row in fines_df.itertuples():
        #Check if fine has been paid. Unpaid fines will have NaT under paymentDate. 
        if pd.isna(row.paymentDate):
            fine_memberID = row.memberID
            fine_fineDate = row.fineDate
            #Retrieve fine amount to add from the overdueBooks_df
            amount_to_add = int(overdueBooks_df_grouped["fineAmount"].get_group((fine_memberID, fine_fineDate)))
            #Modify dataframe value. fineAmount is at column index 1. 
            fines_df.iat[row.Index, 1] = row.fineAmount + amount_to_add

    #Update existing fine table by replacing it with the updated table. 
    fines_df.to_sql('fine', connect.db, if_exists='replace', index=False)
    return "Fines updated."

#Checks if memberUser has no outstanding fines. If user has unpaid fines, False is returned. 
#Use this to check before allowing user to borrow or reserve books. 
def no_unpaid_fine(memberID):
    query_stmt = "SELECT * FROM fine WHERE paymentDate IS NULL AND memberID = \"{}\"".format(memberID)
    unpaid_fine_df = pd.read_sql_query(query_stmt, connect.db)
    return unpaid_fine_df.empty

#Checks if user has any remaining overdue books not returned before payment can be made. 
# False if user still has overdue books not returned. 
def returned_overduebks(memberID):
    query_stmt = "SELECT * FROM book WHERE borrowMemberID = \"{}\" AND ".format(memberID)
    query_stmt += "dateDue IS NOT NULL AND dateDue NOT BETWEEN "
    query_stmt += "DATE_ADD(CURRENT_DATE(), INTERVAL -1 DAY) AND DATE_ADD(CURRENT_DATE(), INTERVAL 8 WEEK)"
    overduebks_df = pd.read_sql_query(query_stmt, connect.db)
    return overduebks_df.empty

def make_payment(memberID):
    #Checks if user needs to pay
    if no_unpaid_fine(memberID):
        return "You do not have any outstanding fines."
    #Checks if user has returned all overdue books.
    if not returned_overduebks(memberID):
        return "Please return all overdue books before making payment."

    #Checks the amount needed to pay and asks user to confirm payment. 
    query_stmt = "SELECT SUM(fineAmount) FROM fine WHERE paymentDate IS NULL AND memberID = \"{}\"".format(memberID)
    payment_amount = connection.execute(query_stmt).fetchall()[0][0]
    print("Your total amount payable is ${}.\n".format(payment_amount))
    response = input("Would you like to proceed with payment?\n")
    
    #Update tables if user confirms payment. Logs transaction into payment table and updates payment date for fine.
    if response == "Yes":
        today = str(date.today())
        insert_stmt = "INSERT INTO payment "
        insert_stmt += "VALUES(\"{}\", {}, DATE(\"{}\"))".format(memberID, int(payment_amount), today)
        connection.execute(insert_stmt)
        update_stmt = "UPDATE fine SET paymentDate = DATE(\"{}\") ".format(today)
        update_stmt += "WHERE memberID = \"{}\" AND paymentDate IS NULL".format(memberID)
        connection.execute(update_stmt)
        return "Payment has been made. You do not have any outstanding fines."

    return "Payment is unsuccessful."