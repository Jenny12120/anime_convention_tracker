import pymysql.cursors
import redis

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
                database=DB_NAME,
                charset='utf8mb4',
                # Key for secure connection:
                ssl={"ssl_verify_cert": True, "ssl_ca": "aiven-ca.pem"},
                # Use DictCursor to return results as dictionaries (optional but useful)
                cursorclass=pymysql.cursors.DictCursor
            )
    return connection

def connect_to_redis():
    r = redis.Redis(
        host='redis-17948.crce174.ca-central-1-1.ec2.redns.redis-cloud.com',
        port=17948,
        password='WIgd8aLQhGYg35oJJhovyD0pK8Sf7kGK',
        decode_responses=True)
    return r

def initialize_convention_counter():
    r = connect_to_redis()    
    r.setnx('global:convention_id_counter', 0)
    
def get_next_convention_id(r: redis.Redis):
    new_id = r.incr('global:convention_id_counter')
    return new_id