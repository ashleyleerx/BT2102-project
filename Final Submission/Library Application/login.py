import DB_Connect as connect
import pandas as pd
import numpy as np
from sqlalchemy import exc

""" 
Function to create an account. Will ask user for 2 inputs 
(functionality can be modified later depending on how the front end is like ), 
and will push the new Username and Password into the memberUser table assuming the username 
has not already been taken
"""
def create_account(newMemberID,newMemberPass):
    # newMemberID = input("Key in your memberID: \n")
    # newMemberPass = input("Key in your password: \n")
    P = pd.DataFrame(np.array([[newMemberID, newMemberPass]]), columns=[
                     "memberID", "memberPassword"])
    try:
        P.to_sql('memberuser', connect.db, if_exists='append', index=False)
        return ("Success. New User Created!")
    except exc.IntegrityError:
        return ("Failure. Username already exists")

""" 
Function to check credentials. Takes in user ID and password and will return result of login 
(successful/unsuccessful)
Cases:
1. ID and Password Match -> Login Sucessful
2. ID match, wrong password -> "Login Unsuccessful -- Incorrect Password"
* if ID doesn't not match, don't bother checking password
3. No ID found -> Invalid UserID (Prompt to Create Acount?)

"""
def check_credential(ID, Password):
    # Dataframe for MemberUser mySQL Relation Info
    user_df = pd.read_sql('memberuser', connect.db) 
    for index, row in user_df.iterrows():
        if row["memberID"] == ID:
            if row["memberPassword"] == Password:
                return 1 #"Login Successful"
            return 2 #"Login Unsuccessful -- Incorrect Password"
    return 3 #Invalid UserID (Prompt to Create Acount?)