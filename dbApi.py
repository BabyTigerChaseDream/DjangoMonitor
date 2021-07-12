#!/usr/local/bin/python3
from collections import namedtuple
from db_helper import DBHelper

#### 
from sqlalchemy import create_engine, Table, Column, Integer, String, Date, Text, MetaData, ForeignKey, desc
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session

#######################################
###     Database class  
#######################################

class MonitorDB:
    def __init__(self):
        self.mydb = DBHelper()
        self.mydb.connect_db()

        # check current database info / table 
        #self.mydb.query("show tables;")
        #L=mydb.cur.fetchall()
        #print(L)

        self.table = "DailyCrashes"

    def create_table(self, sql_create_cmd=None):
        # id, crash_date, platform, is_new, is_blacklist, is_oom, has_jira, JIRA, content, team, owner, ignore  
        # start create table 
        sql_create_cmd = sql_create_cmd or '''
            create table if not exists DailyCrashes(
                id int not null auto_increment, 
                platform varchar(50),
                timestamp date,
                version varchar(50),
                crash_id varchar(50), 
                devices int, 
                is_new boolean default false,
                is_oom boolean default false,
                is_blacklisted boolean default false,
                has_jira boolean default false,
                crash_count int,
                contents text,
                team varchar(50) default "",
                owner varchar(50) default "",
                mute boolean default false,
                jira varchar(250) default "",
                primary key(id)
            )
        '''
        try:
           self.mydb.execute(sql_create_cmd)

        except Exception as exp:
            print("Failed to exec {sql_create_cmd} with {exp}\n".format(sql_create_cmd=sql_create_cmd, exp=exp))

    def insert_crash_elements(self, crash_elements_detail_list):

        sql_insert_to_table = '''
            insert ignore into DailyCrashes \
            (platform, timestamp, version, crash_id, devices, is_new, is_oom, is_blacklisted, has_jira, crash_count, contents) \
            values( \'{platform}\',\'{timestamp}\',\'{version}\',\'{crash_id}\',\'{devices}\',\'{is_new}\',\'{is_oom}\',\'{is_blacklisted}\',\'{has_jira}\',\'{crash_count}\', {contents});
            '''

        if not len(crash_elements_detail_list):
            raise Exception("crash elements is empty \n")
        else:
            print("### Total element to insert {num} ###\n".format(num = len(crash_elements_detail_list) ))

        for ce in crash_elements_detail_list:
            #print(**(ce._asdict()) )
            try:
                sql_cmd = sql_insert_to_table.format (**(ce._asdict())) 
                print( "### SQL cmd :  ", sql_cmd )
                print("\n ----------- \n")
                self.mydb.execute(sql_cmd)
                #exit()
            except Exception as exp:
                #print("Failed on {sql_cmd} with err {exp}".format(sql_cmd=sql_cmd,exp=exp) )
                print("Failed on {sql_cmd} ".format(sql_cmd=sql_cmd) )
                exit()
                #print(" ------ > BYE ")

    def fetch_crash_record(self, sql_cmd):
        try:
            self.mydb.execute(sql_cmd)
            results = self.mydb.cur.fetchall()
        except Exception as exp:
            print("Failed to execute cmd :", sql_cmd)

        return results

    def select_crash_elements_from_db(self, sql_cmd):
        # TODO : table as parameter 
        #table = table or self.table

        sql_select_from_table = '''
            insert ignore into DailyCrashes \
            (platform, timestamp, version, crash_id, devices, is_new, is_oom, is_blacklisted, has_jira, crash_count, contents) \
            values( \'{platform}\',\'{timestamp}\',\'{version}\',\'{crash_id}\',\'{devices}\',\'{is_new}\',\'{is_oom}\',\'{is_blacklisted}\',\'{has_jira}\',\'{crash_count}\', {contents});
            '''

        if not len(crash_elements_detail_list):
            raise Exception("crash elements is empty \n")
        else:
            print("### Total element to insert {num} ###\n".format(num = len(crash_elements_detail_list) ))

        for ce in crash_elements_detail_list:
            #print(**(ce._asdict()) )
            try:
                sql_cmd = sql_insert_to_table.format (**(ce._asdict())) 
                print( "### SQL cmd :  ", sql_cmd )
                print("\n ----------- \n")
                self.mydb.execute(sql_cmd)
                #exit()
            except Exception as exp:
                #print("Failed on {sql_cmd} with err {exp}".format(sql_cmd=sql_cmd,exp=exp) )
                print("Failed on {sql_cmd} ".format(sql_cmd=sql_cmd) )
                exit()
                #print(" ------ > BYE ")

