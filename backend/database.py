import sqlite3

def get_db_connection():
    conn = sqlite3.connect("tickets.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id TEXT PRIMARY KEY,
            issue TEXT,
            order_id TEXT,
            image_url TEXT,
            status TEXT,
            created_at TEXT,
            resolved_at TEXT,
            refund_type TEXT,
            refund_amount TEXT,
            resolution_note TEXT
        )
    """)

    conn.commit()
    conn.close()