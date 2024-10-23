import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('messages.db')
        self.cursor = self.conn.cursor()
        self.setup_database()

    def setup_database(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id TEXT PRIMARY KEY,
                content TEXT,
                author TEXT,
                timestamp DATETIME,
                channel_id TEXT
            )
        ''')
        self.conn.commit()

    def save_message(self, message):
        sql = '''
            INSERT OR IGNORE INTO messages (id, content, author, timestamp, channel_id)
            VALUES (?, ?, ?, ?, ?)
        '''
        self.cursor.execute(sql, (
            str(message.id),
            message.content,
            message.author.name,
            message.created_at.isoformat(),
            str(message.channel.id)
        ))
        self.conn.commit()

    def get_last_message_id(self, channel_id):
        sql = 'SELECT id FROM messages WHERE channel_id = ? ORDER BY timestamp DESC LIMIT 1'
        self.cursor.execute(sql, (str(channel_id),))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def __del__(self):
        self.conn.close()