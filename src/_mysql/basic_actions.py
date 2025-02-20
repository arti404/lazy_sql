import mysql.connector
from mysql.connector import Error as sqlErr
import logging, traceback


class BasicWrapper:
    def __init__(self, host, user, password, database, scheme:dict=None):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.scheme = scheme