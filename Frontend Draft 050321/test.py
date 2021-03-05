def create_account(newMemberID, newMemberPass):
    #newMemberID = input("Key in your memberID: \n")
    #newMemberPass = input("Key in your password: \n")
    P = pd.DataFrame(np.array([[newMemberID, newMemberPass]]), columns=[
                     "memberID", "memberPassword"])
    try:
        P.to_sql('memberuser', connect.db, if_exists='append', index=False)
        return ("\nSuccess. New User Created!")
    except exc.IntegrityError:
        return ("\nFailure. Username already exists")
    
x = input("Key in your memberID: \n")
y = input("Key in your password: \n")
create_account("willy wonka", "hello!")


