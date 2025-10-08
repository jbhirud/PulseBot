import sqlite3
from contextlib import contextmanager
import bcrypt


class LocalAuth:
    def __init__(self, db_path='pulsebot.db'):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize SQLite database for local auth"""
        with self.get_db_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    session_token TEXT UNIQUE,
                    expires_at TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            ''')

    def register_user(self, username, password):
        """Register new local user using bcrypt"""
        password_hash = self.hash_password(password)
        with self.get_db_connection() as conn:
            conn.execute(
                'INSERT INTO users (username, password_hash) VALUES (?, ?)',
                (username, password_hash.decode('utf-8'))
            )


    def authenticate(self, username, password):
        """Authenticate user using bcrypt"""
        with self.get_db_connection() as conn:
            row = conn.execute(
                'SELECT id, password_hash FROM users WHERE username = ?',
                (username,)
            ).fetchone()

        if not row:
            return False

        stored = row[1].encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), stored)

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    @contextmanager
    def get_db_connection(self):
        """Database connection context manager"""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()
