import pandas as pd
import sqlalchemy
import DB_Password as DB_Password


db = sqlalchemy.create_engine(
    'mysql+pymysql://root:{}@localhost:3306/library'.format(DB_Password.password))


# readsql in the form of pandas dataframe
#print(pd.read_sql('memberuser', db))
