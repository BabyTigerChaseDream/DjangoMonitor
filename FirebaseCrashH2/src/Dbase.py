'''
##################################################

This file is an abstraction of crash database
 - based on sqlalchemy session(multi-thread access safe)

##################################################
'''

from sqlalchemy import create_engine, Table, Column, Integer, String, Date, Text, MetaData, ForeignKey, desc, DateTime, UniqueConstraint

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session
#from sqlalchemy.sql import insert, select, update, delete
#from sqlalchemy.sql import or_, and_, any_, not_
from sqlalchemy.types import JSON 

Base = declarative_base()

'''
class ReservedDB(Base):
    __tablename__ = 'ReservedDB'

    id = Column(Integer, primary_key=True)
    issue_id = Column(String(20))
    event_timestamp = Column(Date)

    triageData_list = relationship("FirebaseCrashes", backref="ReservedDB")

    def __str__(self):
        return ':'.join(str(self.id), str(self.version), str(self.date))

    def to_json(self):
        return {
            'id': self.id,
            'issue_id': self.issue_id,
            "event_timestamp": self.event_timestamp
        }
'''

class Dbase:
	# default connection string: connect to QA team crash database & reading existing data  
    conn_string = 'mysql+pymysql://root:123456@localhost:3306/FirebaseCrashes'
    connection = None
    engine = None
    database = "FirebaseCrashes"
    # TODO: create DB
    # conn_string = None
    metadata = Base.metadata

    # android crash : android daily crash data
    firebase_crashlytics_android = Table('firebase_crashlytics_android',
                       metadata,
                       Column('id', Integer(),
                              primary_key=True, autoincrement=True),
                       Column('issue_id', String(50), index=True,
                              nullable=False, unique=True),
                       Column('issue_title', String(500)),
                       Column('issue_subtitle', String(500)),
                       Column('total_user', Integer()),
                       Column('crash_count', Integer()),
					   # TODO: string to datetime
                       Column('event_timestamp', DateTime()),
                       Column('platform', String(50),default='android'),
                       Column('app_version', String(50)),
					   Column('crashframes',JSON),
                       UniqueConstraint('issue_id'),
					   keep_existing=True 
                       )
'''
    # ios crash : ios daily crash data
    firebase_crashlytics_ios = Table('firebase_crashlytics_ios',
                       metadata,
                       Column('id', Integer(),
                              primary_key=True, autoincrement=True),
                       Column('issue_id', String(50), index=True,
                              nullable=False, unique=True),
                       Column('issue_title', String(500)),
                       Column('issue_subtitle', String(500)),
                       Column('total_user', Integer()),
                       Column('crash_count', Integer()),
					   # TODO: string to datetime
                       Column('event_timestamp', DateTime()),
                       Column('platform', String(50),default='ios'),
                       Column('app_version', String(50)),
					   Column('crashframes',JSON),
                       UniqueConstraint('issue_id'),
				 	   keep_existing=True
                       )

    # all jira tickets has issue_id 
    firebase_crashlytics_jira = Table('firebase_crashlytics_jira',
                 metadata,
                 Column('id', Integer(), primary_key=True, autoincrement=True),
				 # issue_id in firebase_crashlytics_'platform'
                 Column('issue_id', String(50), index=True, nullable=False, unique=True),
                 Column('ticket_id', String(50), index=True, nullable=False, unique=True),
				 # TODO : check logic of jira filed date
                 #Column('file_timestamp', DateTime()),
                 UniqueConstraint('issue_id'),
				 keep_existing=True
                 )

'''
	def __init__(self):
		pass

    def connect(self, echo=False, conn_string=None, database=None):
        try:
            self.engine=create_engine(
                conn_string or self.conn_string, echo=echo, pool_pre_ping=True)
        except:
            self.db=database or self.database
            self.engine.execute("create database if not exists %s" % self.db)
            self.engine.execute("use %s" % self.db)

        self.session = scoped_session(sessionmaker(bind=self.engine))
        self.connection=self.engine.connect()

	def execute(self, cmd):
		return self.engine.execute(cmd)

    def close(self):
        self.connection.close()

    def create_datatables(self):
        self.metadata.create_all(self.engine)

	########################################################
	# Operation on each table 
	########################################################

	def bulk_save(self, objects):
        self.session.bulk_save_objects(objects)
		self.session.commit()
	