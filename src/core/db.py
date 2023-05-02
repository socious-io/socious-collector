import os
import glob
import psycopg2
from urllib.parse import urlparse
from src.config import config


class Database:

    def __init__(self, db_uri, sql_dir) -> None:
        url = urlparse(db_uri)

        # Connect to the database using the parsed connection string
        self.conn = psycopg2.connect(
            dbname=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )

        self.sqls = self.load_sqls(sql_dir)

    def load_sqls(self, sql_dir):
        files = {}
        for file in glob.glob('%s/*.sql' % sql_dir):
            files.update({os.path.basename(file): open(file, 'r').read()})
        return files

    def query(self, name, params=None):
        if '.sql' not in name:
            name += '.sql'

        query = self.sqls[name]
        if 'get' in name:
            return self.fetch(query, params)
        return self.execute(query, params)

    def execute(self, query, params=None):
        with self.conn.cursor() as cur:
            try:
                cur.execute(query, params)
                self.conn.commit()
                results = cur.fetchall()
                return self.result_to_dict(cur, results)
            except Exception as e:
                self.conn.rollback()
                raise e

    def fetch(self, query, params=None):
        with self.conn.cursor() as cur:
            cur.execute(query, params)
            results = cur.fetchall()
            return self.result_to_dict(cur, results)

    def result_to_dict(self, cursor, results):
        column_names = [desc[0] for desc in cursor.description]
        rows = []

        if not results:
            return rows

        for row in results:
            row_dict = {}
            for index, column_name in enumerate(column_names):
                row_dict[column_name] = row[index]
            rows.append(row_dict)
        return rows


DB = Database(config.database_url, config.sql_dir)
