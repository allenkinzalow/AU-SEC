import os

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

#mysql info
SQLALCHEMY_DATABASE_URI="mysql+pymysql://d2944o7xg2ywt9sq:w27ml3710spjztt6@tkck4yllxdrw0bhi.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/oajshe5hvvevfulh"
MYSQL_USER = "d2944o7xg2ywt9sq"
MYSQL_PASS = "w27ml3710spjztt6"
MYSQL_HOST = "tkck4yllxdrw0bhi.cbetxkdyhwsb.us-east-1.rds.amazonaws.com"
MYSQL_PORT = 3306
MYSQL_DB = "oajshe5hvvevfulh"

DEFAULT_DATA_TABLE = "patients"