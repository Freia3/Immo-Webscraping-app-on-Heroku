from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from connect_to_postgres import connectToPostGresDB


def insert_into_psql(list_article_ids):
    con = connectToPostGresDB()  # connect to PostGres DB and return connector
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    for item in list_article_ids:

        cur.execute(f"""
            INSERT INTO public."Articles"(article_id) VALUES ('{item}'); """)
    cur.close()
    con.close()