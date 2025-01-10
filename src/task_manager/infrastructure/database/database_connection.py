import psycopg2
import psycopg2.extras
from src.core.config import Settings


class DatabaseConnection:
    def __init__(self, settings: Settings):
        self.settings = settings

    def get_connection(self):
        try:
            conn = psycopg2.connect(
                dbname=self.settings.DB_NAME,
                user=self.settings.DB_USER,
                password=self.settings.DB_PASS,
                host=self.settings.DB_HOST,
                port=self.settings.DB_PORT
            )
            conn.cursor_factory = psycopg2.extras.DictCursor
            return conn
        except Exception as e:
            print(f"Error connecting to database: {e}")
            raise 