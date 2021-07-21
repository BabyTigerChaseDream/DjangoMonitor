# coding:utf-8

import pymysql
from sshtunnel import SSHTunnelForwarder


class DBHelper:

    def __init__(self, host, user, password, port, db, ssh_server, ssh_port, ssh_username):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.db = db
        self.ssh_server = ssh_server
        self.ssh_port = ssh_port
        self.ssh_username = ssh_username
        self.conn = None
        self.cur = None
        self.svr = None

    def connect_db(self):
        try:
            self.conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                db=self.db,
                port=self.port)
            print("Connection Done: %s : %s" % (self.host, self.db))
            self.cur = self.conn.cursor()
            print("Cursor Initialization Done")
        except Exception as exp:
            print("Connection Error: ", exp)

    def connect_db_ssh(self):
        try:
            self.svr = SSHTunnelForwarder(
                ssh_address_or_host=(self.ssh_server, self.ssh_port),
                ssh_username=self.ssh_username,
                remote_bind_address=(self.host, self.port)
            )
            self.svr.start()

            self.conn = pymysql.connect(
                host="127.0.0.1",
                user=self.user,
                password=self.password,
                db=self.db,
                port=self.svr.local_bind_port
            )
            print("Connection Done: %s : %s" % (self.host, self.db))
            self.cur = self.conn.cursor()
            print("Cursor Initialization Done")
        except Exception as exp:
            print("Connection Error: ", exp)

    def close(self):
        if self.cur:
            print("Close Cursor")
            self.cur.close()
            self.cur = None
        if self.conn:
            print("Close Connection")
            self.conn.close()
            self.conn = None
        if self.svr:
            print("Close SSH Server")
            self.svr.close()
            self.svr = None

    def execute(self, sql_str, params=None):
        try:
            self.cur.execute(sql_str, params)
            self.conn.commit()
            print("Execution Done: ", sql_str)
        except Exception as exp:
            print("Execution Failed when running: ", sql_str, " Error: ", exp)

    def query(self, sql_str, params=None):
        try:
            self.cur.execute(sql_str, params)
            results = self.cur.fetchall()
            print("Query Done: ", sql_str)
            return results
        except Exception as exp:
            print("Query Failed when running: ", sql_str, " Error: ", exp)
