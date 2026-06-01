import sqlite3
from pathlib import Path

DB_PATH = "data/history.db"


def get_connection():
    """
    Create SQLite connection.
    """
    Path("data").mkdir(exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    return conn


def initialize_database():
    """
    Create history table if not exists.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        video_url TEXT NOT NULL,
        video_title TEXT,
        summary_type TEXT,
        content TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def save_history(
    video_url,
    video_title,
    summary_type,
    content
):
    """
    Save generated content.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO history (
        video_url,
        video_title,
        summary_type,
        content
    )
    VALUES (?, ?, ?, ?)
    """, (
        video_url,
        video_title,
        summary_type,
        content
    ))

    conn.commit()
    conn.close()


def get_all_history():
    """
    Fetch latest history.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        id,
        video_title,
        summary_type,
        created_at
    FROM history
    ORDER BY created_at DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_history_by_id(record_id):
    """
    Get specific history record.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM history
    WHERE id=?
    """, (record_id,))

    row = cursor.fetchone()

    conn.close()

    return row


def delete_history(record_id):
    """
    Delete one history item.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM history
    WHERE id=?
    """, (record_id,))

    conn.commit()
    conn.close()


def clear_history():
    """
    Remove all history.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM history
    """)

    conn.commit()
    conn.close()