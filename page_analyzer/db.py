"""Работа с базой данных."""

import sqlite3
from datetime import datetime

DATABASE = 'page_analyzer.db'

def get_db_connection():
    """Возвращает соединение с БД."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Инициализирует таблицы."""
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS url_checks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url_id INTEGER REFERENCES urls(id),
                status_code INTEGER,
                h1 TEXT,
                title TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

def add_url(name):
    """Добавляет новый URL в БД. Возвращает id."""
    with get_db_connection() as conn:
        cursor = conn.execute('INSERT INTO urls (name) VALUES (?)', (name,))
        return cursor.lastrowid

def get_url_by_name(name):
    """Ищет URL по имени. Возвращает строку или None."""
    with get_db_connection() as conn:
        return conn.execute('SELECT * FROM urls WHERE name = ?', (name,)).fetchone()

def get_all_urls():
    """Возвращает все URL с последней проверкой."""
    with get_db_connection() as conn:
        return conn.execute('''
            SELECT u.id, u.name, u.created_at,
                   uc.status_code, uc.h1, uc.title, uc.description, uc.created_at as last_check
            FROM urls u
            LEFT JOIN url_checks uc ON u.id = uc.url_id
            WHERE uc.created_at = (
                SELECT MAX(created_at) FROM url_checks WHERE url_id = u.id
            ) OR uc.id IS NULL
            ORDER BY u.created_at DESC
        ''').fetchall()

def get_url_by_id(url_id):
    """Возвращает URL по id."""
    with get_db_connection() as conn:
        return conn.execute('SELECT * FROM urls WHERE id = ?', (url_id,)).fetchone()

def get_checks_for_url(url_id):
    """Возвращает все проверки для URL."""
    with get_db_connection() as conn:
        return conn.execute('''
            SELECT * FROM url_checks WHERE url_id = ? ORDER BY created_at DESC
        ''', (url_id,)).fetchall()

def add_check(url_id, status_code, title, description, h1=None):
    """Добавляет новую проверку."""
    with get_db_connection() as conn:
        conn.execute('''
            INSERT INTO url_checks (url_id, status_code, h1, title, description, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (url_id, status_code, h1, title, description, datetime.utcnow()))
