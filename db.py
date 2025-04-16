import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="shreya",
        database="agrovision",
        cursorclass=pymysql.cursors.DictCursor
    )