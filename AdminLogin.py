import DB_Connect as connect
import pandas as pd
import numpy as np
from sqlalchemy import exc

# Dataframe for MemberUser mySQL Relation Info
adminuser_df = pd.read_sql('adminuser', connect.db)

""" 

Function to create an Admin account. Will ask user for 2 inputs 
(functionality can be modified later depending on how the front end is like ), 
and will push the new Admin Username and Password into the AdminUser table assuming the username 
has not already been taken

"""


def create_account():
    newAdminID = input("Key in your memberID: \n")
    newAdminPass = input("Key in your password: \n")
    P = pd.DataFrame(np.array([[newAdminID, newAdminPass]]), columns=[
                     "adminID", "adminPassword"])
    try:
        P.to_sql('adminuser', connect.db, if_exists='append', index=False)
        return ("\nSuccess. New Admin User Created!")
    except exc.IntegrityError:
        return ("\nFailure. Admin Username already exists")


""" 

Function to check credentials. Takes in Admin User ID and password and will return result of login 
(successful/unsuccessful)

"""


def check_credential(ID, Password):
    for index, row in adminuser_df.iterrows():
        if row["adminID"] == ID:
            if row["adminPassword"] == Password:
                return "Login Successful"
            return "Login Unsuccessful -- Incorrect Password"
    response = input("No Admin User found. Create account?\n")
    if response == "Yes":
        return create_account()
    else:
        return "Try again with valid AdminUser ID and Password"


print(check_credential("Willy", 'Wonda'))
