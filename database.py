import pymysql.cursors
import ssl
import os

MYSQL_HOST = "anime-convention-tracker-animeconventiontracker2025.h.aivencloud.com" 
MYSQL_PORT = 26181
MYSQL_USER = "avnadmin"
MYSQL_PASSWORD = "AVNS_YbJP225UsFzOAys_79O"
DB_NAME = "defaultdb"


def connect_to_db():
    connection = pymysql.connect(
                host=MYSQL_HOST,
                port=MYSQL_PORT,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                db=DB_NAME,
                charset='utf8mb4',
                # Key for secure connection:
                ssl={"ssl_verify_cert": True, "ssl_ca": "aiven-ca.pem"},
                # Use DictCursor to return results as dictionaries (optional but useful)
                cursorclass=pymysql.cursors.DictCursor
            )
    return connection

def fetch_from_db(start_date, end_date):
    connection = connect_to_db()
    with connection.cursor() as cursor:
        retrieve_between_dates = """
        SELECT name,
            start_date,
            end_date,
            location AS venue,
            url
            FROM Conventions WHERE start_date >= %s AND end_date <= %s;
    """
        cursor.execute(retrieve_between_dates,(start_date, end_date))
    if 'connection' in locals() and connection.open:
        connection.close()
    
    return cursor.fetchall()
