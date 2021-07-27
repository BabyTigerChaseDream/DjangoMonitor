from common_lib.db_helper import DBHelper

ssh_server = 'jiaguo-cron.dev.booking.com'
ssh_port = 22
ssh_username = 'jiaguo'
host_dqs = "dev-androidmdb-vip.lhr4.dqs.booking.com"
user_db = "devcronapp_cron_android65"
password_db = "bNWGiboBmRzQj9o2"
# port TBD 
port_dqs = 3306
db = "android"

dqs = DBHelper(host_dqs, user_db, password_db, port_dqs, db, ssh_server, ssh_port, ssh_username)
dqs.connect_db_ssh()

'''
[Trial local]
>>> ssh_server = 'jiaguo-cron.dev.booking.com'
>>> ssh_port = 22
>>> ssh_username = 'jiaguo'
>>> host_dqs = "dev-androidmdb-vip.lhr4.dqs.booking.com"
>>> user_db = "devcronapp_cron_android65"
>>> password_db = "bNWGiboBmRzQj9o2"
>>> port_dqs = 3306
>>> db = "android"
>>> 
>>> dqs=db_helper.DBHelper(host_dqs, user_db, password_db, port_dqs, db, ssh_server, ssh_port, ssh_username)
>>> dqs.connect_db_ssh()
Connection Error:  No password or public key available!
'''