-- Users table
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,               -- use TEXT for UUIDs
    username TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);