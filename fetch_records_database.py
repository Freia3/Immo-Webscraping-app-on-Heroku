import psycopg2
import urllib.parse as urlparse
import os
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from connect_to_postgres import connectToPostGresDB

def fetch_records_psql():
    con=connectToPostGresDB() #connect to PostGres DB
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS public."Articles"(user_id serial PRIMARY KEY, article_id VARCHAR (150) NOT NULL);
    select article_id from public."Articles";""")
    records = cur.fetchall()
    out = [item for t in records for item in t]
    cur.close()
    con.close()
    return out

