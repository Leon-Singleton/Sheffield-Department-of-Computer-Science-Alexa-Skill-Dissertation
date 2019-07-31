#import pymysql, the library used for SQL queries within python
import pymysql

#set the connection details to the MySQL webserver hosted by Amazon RDS
rds_host  = "dcs-skill-db.cqv2uqkxoxnp.eu-west-1.rds.amazonaws.com"
name = "Bazilpop"
password = "Bazilpoppassword"
db_name = "DCS_Skill_DB"

#connect to the database server
conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
