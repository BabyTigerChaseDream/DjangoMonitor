# -*- coding:utf-8 -*-
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
 
from configs import DB_URI
 
eng = create_engine(DB_URI) # equivalent to MySQLdb connection, database connection API
Base = declarative_base() # base class provided by sqlalchemy
 
class School(Base):
    __tablename__ = 'school'
    id = Column(Integer, Sequence('school_id_seq'), primary_key=True, autoincrement=True)
    name = Column(String(30))
 
 # Delete and create a new table in Base, where Base only has a school table
Base.metadata.drop_all(bind=eng)
Base.metadata.create_all(bind=eng)
 
 # Create session transaction
Session = sessionmaker(bind=eng)
session = Session()
 
 #) Add a record in the transaction and commit the commit
session.add(School(name='Adam'))
session.add_all([School(name=student_name) for student_name in ('James', 'Marrie', 'Charlie', 'David')])
session.commit()
 
 # Get the helper function of the query result
def show_query_result(rest):
    for student in rest:
        print (student.name)
 
 # Query all records and display
rest = session.query(School).all()
show_query_result(rest)