import hashlib
import sqlite3
from contextlib import contextmanager


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
        """Register new local user"""
        password_hash = self.hash_password(password)
        with self.get_db_connection() as conn:
            conn.execute(
                'INSERT INTO users (username, password_hash) VALUES (?, ?)',
                (username, password_hash)
            )

    def authenticate(self, username, password):
        """Authenticate user"""
        password_hash = self.hash_password(password)
        with self.get_db_connection() as conn:
            user = conn.execute(
                'SELECT id FROM users WHERE username = ? AND password_hash = ?',
                (username, password_hash)
            ).fetchone()
        return user is not None

    def hash_password(self, password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    @contextmanager
    def get_db_connection(self):
        """Database connection context manager"""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()
