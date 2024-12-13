import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        self.host = 'localhost'
        self.database = 'electrack'
        self.user = 'root'
        self.password = ''

    def get_db_connection(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if connection.is_connected():
                print("Connection Successful")
                return connection
        except Error as e:
            print(f"Error: {e}")
            return None