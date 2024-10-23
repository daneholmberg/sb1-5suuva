import Database from 'better-sqlite3';

const db = new Database('messages.db');

db.exec(`
  CREATE TABLE IF NOT EXISTS messages (
    id TEXT PRIMARY KEY,
    content TEXT,
    author TEXT,
    timestamp DATETIME,
    channel_id TEXT
  )
`);

export function saveMessage(message) {
  const stmt = db.prepare(`
    INSERT OR IGNORE INTO messages (id, content, author, timestamp, channel_id)
    VALUES (?, ?, ?, ?, ?)
  `);

  stmt.run(
    message.id,
    message.content,
    message.author.username,
    message.createdAt.toISOString(),
    message.channelId
  );
}

export function getLastMessageId(channelId) {
  const stmt = db.prepare('SELECT id FROM messages WHERE channel_id = ? ORDER BY timestamp DESC LIMIT 1');
  const result = stmt.get(channelId);
  return result?.id;
}