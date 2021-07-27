from sqlalchemy import create_engine, Table, Column, Integer, String, Date, Text, MetaData, ForeignKey, desc, DateTime, UniqueConstraint

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.sql import insert, select, update, delete
from sqlalchemy.sql import or_, and_, any_, not_


Base = declarative_base()

class Changlist(Base):
    __tablename__ = 'Changelist'

    id = Column(Integer, primary_key=True)
    CL = Column(String(20))
    version = Column(String(20))
    date = Column(Date)
    test_type = Column(String(10))
    status = Column(String(16))

    triageData_list = relationship("TriageData", backref="Changelist")

    def __str__(self):
        return str(self.id)

    def to_json(self):
        return {
            'id': self.id,
            'CL': self.CL,
            "version": self.version,
            "date": self.date,
            "type": self.test_type
        }

class Dbase:
    conn_string = 'mysql+pymysql://root:123456@10.19.193.83:3306/cudnn_auto_triage'
    connection = None
    engine = None
    database = "try"
    # TODO: create DB
    # conn_string = None
    metadata = Base.metadata

    # UUID table:store each UUID daily
    submission = Table('Submission',
                       metadata,
                       Column('subm_id', Integer(),
                              primary_key=True, autoincrement=True),
                       Column('uuid', String(50), index=True,
                              nullable=False, unique=True),
                       Column('date', DateTime()),
                       Column('changelist', Integer(), index=True),
                       Column('tag', String(300)),
                       UniqueConstraint('uuid')
                       )

    # test resus matrix
    test = Table('Test',
                 metadata,
                 Column('id', Integer(), primary_key=True, autoincrement=True),
                 Column('hw', String(30)),
                 UniqueConstraint('TBD')
                 )

 
    def connect(self, echo=False, conn_string=None, database=None):
        try:
            self.engine=create_engine(
                conn_string or self.conn_string, echo=echo, pool_pre_ping=True)
        except:
            self.db=database or self.database
            self.engine.execute("create database if not exists %s" % self.db)
            self.engine.execute("use %s" % self.db)

        self.metadata.create_all(self.engine)
        self.connection=self.engine.connect()

    def close(self):
        self.connection.close()
