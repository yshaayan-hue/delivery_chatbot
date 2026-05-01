from backend.database import get_db

def create_ticket(order_id, issue, image):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tickets (order_id, issue, image, status)
        VALUES (?, ?, ?, ?)
    """, (order_id, issue, image, "Open"))

    conn.commit()

    ticket_id = cursor.lastrowid
    print("NEW TICKET ID:", ticket_id)

    conn.close()

    return ticket_id


def get_ticket(order_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tickets WHERE order_id = ?", (order_id,))
    row = cursor.fetchone()

    conn.close()

    if row:
        return {
            "id": row[0],
            "order_id": row[1],
            "issue": row[2],
            "image": row[3],
            "status": row[4]
        }

    return None