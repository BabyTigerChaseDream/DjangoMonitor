#!/usr/local/bin/python3
from collections import namedtuple
from db_helper import DBHelper

#######################################
# database for daily crash 
#######################################

mydb = DBHelper()
mydb.connect_db()
# check current database info / table 
mydb.query("show tables;")

# connect to db
mydb.connect_db()

# id, crash_date, platform, is_new, is_blacklist, is_oom, has_jira, JIRA, content, team, owner, ignore  
# start create table 
sql_create_table = '''
    create table if not exists DailyCrashes(
        id varchar(50), 
        crash_date varchar(50),
        platform varchar(50),
        is_new varchar(50),
        is_blacklist int,
        is_oom int,
        has_jira int,
        JIRA varchar(250) default null,
        content varchar(300),
        team varchar(50) default null,
        owner varchar(50) default null,
        ignore boolean default false,
        primary key(id)
    )
'''
mydb.query(sql_create_table)

mydb.query("show tables;")
L=mydb.cur.fetchall()
print(L)

#######################################
# get detail info of single crash 
#######################################
# get detailed info of each commit
# TODO : for dup ID items : ignore or replace ? 
sql_insert_to_table = '''
    insert ignore into DailyCrashes \
    (id, crash_date, platform, is_new, is_blacklist, is_oom, has_jira, JIRA, content, team, owner, ignore) \
    values({id},{crash_date},{platform},{is_new},{is_blacklist},{is_oom},{has_jira},{JIRA},{content},{team},{owner},{ignore});
'''
# Collect ALL data and put in DB 
try:
    # define namedtuple crash_id_list 
     crash_item  = namedtuple('crash_item',['id','crash_date','platform','is_new','is_blacklist','is_oom','has_jira','JIRA','content','team','owner','ignore'])  
     for crash_id in crash_id_list:
        get_single_commit_requests = get_single_commit_url.format(branch_id=branch_id,private_token=private_token,commit_id=commit_id)
        # get single commit 
        single_commit_detail_info = requests.get(get_single_commit_requests).json() 
        # assign json data to namedtuple 
        single_commit_info = crash_item(id=json.dumps(single_commit_detail_info['id']),
                                                   author_name=json.dumps(single_commit_detail_info['author_name']),
                                                   author_email=json.dumps(single_commit_detail_info['author_email']),
                                                   committed_date=json.dumps(single_commit_detail_info['committed_date']),
                                                   additionlines=json.dumps(single_commit_detail_info['stats']['additions']),
                                                   deletionlines=json.dumps(single_commit_detail_info['stats']['deletions']),
                                                   changedfiles=json.dumps(single_commit_detail_info['stats']['total']),
                                                   web_url=json.dumps(single_commit_detail_info['web_url']),
                                                   project_id=json.dumps(single_commit_detail_info['project_id']),
                                                )
        # single_commit_info._asdict()
        print(">>>>> single info : ",single_commit_info)
        #### get detail info of single commit 

        mydb.execute(sql_insert_to_table.format (**(single_commit_info._asdict()) ) )
        #print("[dbg sql cmd] ", sql_insert_to_table.format (**(single_commit_info._asdict()) ) )

except Exception as exp:
    print("Failed to get single commits info : ", exp)