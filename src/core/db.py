import os
import glob
import psycopg2
from psycopg2 import pool
from urllib.parse import urlparse
from contextlib import contextmanager
from typing import Optional, Dict, List, Any
from src.config import config
from src.utils.logger import get_logger

logger = get_logger('database')


class Database:

    def __init__(self, db_uri: str, sql_dir: str, min_conn: int = 1, max_conn: int = 10) -> None:
        url = urlparse(db_uri)

        # Create connection pool instead of single connection
        self.connection_pool = pool.ThreadedConnectionPool(
            min_conn,
            max_conn,
            dbname=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )

        self.db_uri = db_uri
        self.sql_dir = sql_dir
        self.sqls = self.load_sqls(sql_dir)
        logger.info(f"Database connection pool initialized (min={min_conn}, max={max_conn})")

    def load_sqls(self, sql_dir: str) -> Dict[str, str]:
        files = {}
        for file_path in glob.glob('%s/*.sql' % sql_dir):
            # Use context manager to properly close file handles
            with open(file_path, 'r') as f:
                files[os.path.basename(file_path)] = f.read()
        logger.info(f"Loaded {len(files)} SQL files from {sql_dir}")
        return files

    @contextmanager
    def get_connection(self):
        """Context manager for getting a connection from the pool."""
        conn = None
        try:
            conn = self.connection_pool.getconn()
            yield conn
        except psycopg2.OperationalError as e:
            logger.error(f"Database connection error: {e}")
            # Try to reconnect
            self._reconnect()
            conn = self.connection_pool.getconn()
            yield conn
        finally:
            if conn:
                self.connection_pool.putconn(conn)

    def _reconnect(self) -> None:
        """Attempt to reconnect to the database."""
        logger.warning("Attempting to reconnect to database...")
        try:
            url = urlparse(self.db_uri)
            self.connection_pool = pool.ThreadedConnectionPool(
                1, 10,
                dbname=url.path[1:],
                user=url.username,
                password=url.password,
                host=url.hostname,
                port=url.port
            )
            logger.info("Database reconnection successful")
        except Exception as e:
            logger.error(f"Database reconnection failed: {e}")
            raise

    def query(self, name: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        if '.sql' not in name:
            name += '.sql'

        query = self.sqls[name]
        if 'get' in name:
            return self.fetch(query, params)
        return self.execute(query, params)

    def execute(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(query, params)
                    conn.commit()
                    results = cur.fetchall()
                    return self.result_to_dict(cur, results)
                except psycopg2.Error as e:
                    conn.rollback()
                    logger.error(f"Database execute error: {e}")
                    raise

    def fetch(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(query, params)
                    results = cur.fetchall()
                    return self.result_to_dict(cur, results)
                except psycopg2.Error as e:
                    logger.error(f"Database fetch error: {e}")
                    raise

    def result_to_dict(self, cursor, results) -> List[Dict[str, Any]]:
        if not cursor.description:
            return []

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

    def close(self) -> None:
        """Close all connections in the pool."""
        if self.connection_pool:
            self.connection_pool.closeall()
            logger.info("Database connection pool closed")

    def health_check(self) -> bool:
        """Check if database connection is healthy."""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")
                    return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False


DB = Database(config.database_url, config.sql_dir)
