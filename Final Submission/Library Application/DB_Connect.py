import pandas as pd
import sqlalchemy
import DB_Password as DB_Password
from pymongo import MongoClient

db = sqlalchemy.create_engine(
        'mysql+pymysql://root:{}@localhost:3306/library'.format(DB_Password.password))

mongodb = MongoClient('localhost', 27017)

# m_db = mongodb.mongodb_database_name
m_db = mongodb.library
#collection = m_db.collection_name
collection = m_db.books