# -*- coding:utf-8 -*-
from sqlalchemy import *
from sqlalchemy.orm import create_session
from sqlalchemy.ext.declarative import declarative_base
 
from configs import DB_URI
 
Base = declarative_base()
engine = create_engine(DB_URI)
metadata = MetaData(bind=engine)
 
class School(Base):
    '''Map an existing database, passing in three parameters: database name, metadata (binding interface), autoload=True'''
    __table__ = Table('school', metadata, autoload=True)
 
def show_query_result(rest):
    for student in rest:
        print (student.name)
 
 #Create a transaction
session = create_session(bind=engine)
 
 #test database query function
rest = session.query(School).all()
show_query_result(rest)
 
print ('-' * 15)
 
 #Test to increase the record function
session.begin()
session.add(School(name='Derek'))
session.commit()
 
 #Query increase results
rest = session.query(School).all()
show_query_result(rest)