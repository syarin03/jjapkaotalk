import socket
from _thread import *
import pymysql

client_sockets = list()

HOST = '10.10.21.116'
PORT = 9000
DB_HOST = '10.10.21.116'
DB_USER = 'talk_admin'
DB_PASSWORD = 'admin1234'


def conn_fetch():
    con = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db='talk', charset='utf8')
    cur = con.cursor()
    return cur


def conn_commit():
    con = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db='talk', charset='utf8')
    return con
