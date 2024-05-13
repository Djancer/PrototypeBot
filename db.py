import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        chat_id INTEGER
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS work_sessions (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        start_time TEXT,
        end_time TEXT,
        paused INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')
    conn.commit()
    conn.close()

def add_user(username, chat_id):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, chat_id) VALUES (?, ?)', (username, chat_id))
    conn.commit()
    conn.close()

def get_users():
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return users

def start_work_session(user_id):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    start_time = datetime.now().isoformat()
    cursor.execute('INSERT INTO work_sessions (user_id, start_time, paused) VALUES (?, ?, ?)', (user_id, start_time, 0))
    conn.commit()
    conn.close()

def end_work_session(user_id):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    end_time = datetime.now().isoformat()
    cursor.execute('UPDATE work_sessions SET end_time = ? WHERE user_id = ? AND end_time IS NULL', (end_time, user_id))
    conn.commit()
    conn.close()

def pause_work_session(user_id):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE work_sessions SET paused = 1 WHERE user_id = ? AND end_time IS NULL', (user_id,))
    conn.commit()
    conn.close()

def resume_work_session(user_id):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE work_sessions SET paused = 0 WHERE user_id = ? AND end_time IS NULL', (user_id,))
    conn.commit()
    conn.close()

def calculate_worked_time(user_id):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT start_time, end_time FROM work_sessions WHERE user_id = ? AND end_time IS NOT NULL', (user_id,))
    sessions = cursor.fetchall()
    total_time = 0
    for session in sessions:
        start_time = datetime.fromisoformat(session[0])
        end_time = datetime.fromisoformat(session[1])
        total_time += (end_time - start_time).total_seconds()
    conn.close()
    return total_time
