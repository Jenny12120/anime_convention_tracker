import pymysql.cursors

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
                database=DB_NAME,
                charset='utf8mb4',
                # Key for secure connection:
                ssl={"ssl_verify_cert": True, "ssl_ca": "aiven-ca.pem"},
                # Use DictCursor to return results as dictionaries (optional but useful)
                cursorclass=pymysql.cursors.DictCursor
            )
    return connection
