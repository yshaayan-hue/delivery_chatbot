import os
import uuid
import random
from datetime import datetime
from flask import Blueprint, request, jsonify, session
from backend.database import get_db_connection

ticket_bp = Blueprint("ticket_bp", __name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "..", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------------- AUTH CHECK ---------------- #
def admin_required():
    return session.get("admin")


# ---------------- CREATE TICKET ---------------- #
@ticket_bp.route("/tickets", methods=["POST"])
def create_ticket():
    issue = request.form.get("issue")
    order_id = request.form.get("order_id")
    file = request.files.get("image")

    if not issue or not order_id:
        return jsonify({"error": "Missing fields"}), 400

    image_url = None

    if file:
        ext = os.path.splitext(file.filename)[1]
        filename = f"{uuid.uuid4()}{ext}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        image_url = f"/uploads/{filename}"

    ticket_id = "TKT" + str(random.randint(100000, 999999))

    created_at = datetime.now().isoformat()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tickets (
            ticket_id, issue, order_id, image_url, status,
            created_at, resolved_at, refund_type, refund_amount, resolution_note
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        ticket_id,
        issue,
        order_id,
        image_url,
        "Pending",
        created_at,
        None,
        None,
        None,
        None
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "ticket_id": ticket_id,
        "issue": issue,
        "order_id": order_id,
        "image_url": image_url,
        "status": "Pending",
        "created_at": created_at
    })


# ---------------- GET SINGLE ---------------- #
@ticket_bp.route("/ticket/<ticket_id>", methods=["GET"])
def get_ticket(ticket_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tickets WHERE ticket_id = ?", (ticket_id,))
    row = cursor.fetchone()

    conn.close()

    if not row:
        return jsonify({"error": "Ticket not found"}), 404

    return jsonify(dict(row)) 


# ---------------- GROUPED (ADMIN ONLY) ---------------- #
@ticket_bp.route("/grouped-tickets", methods=["GET"])
def get_grouped_tickets():
    if not admin_required():
        return jsonify({"error": "Unauthorized"}), 403

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tickets")
    rows = cursor.fetchall()
    conn.close()

    groups = {}

    for row in rows:
        ticket = dict(row)

        key = (ticket["order_id"], ticket["issue"], ticket["image_url"])

        if key not in groups:
            groups[key] = {
                "order_id": ticket["order_id"],
                "issue": ticket["issue"],
                "image_url": ticket["image_url"],
                "latest_ticket_id": ticket["ticket_id"],
                "latest_status": ticket["status"],
                "created_at": ticket["created_at"],
                "total_tickets": 1
            }
        else:
            groups[key]["total_tickets"] += 1

            if ticket["created_at"] > groups[key]["created_at"]:
                groups[key]["latest_ticket_id"] = ticket["ticket_id"]
                groups[key]["latest_status"] = ticket["status"]
                groups[key]["created_at"] = ticket["created_at"]

    return jsonify(list(groups.values()))


# ---------------- RESOLVE (ADMIN ONLY) ---------------- #
@ticket_bp.route("/resolve/<ticket_id>", methods=["POST"])
def resolve_ticket(ticket_id):
    if not admin_required():
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json

    action = data.get("action")
    amount = data.get("amount")
    note = data.get("note")

    conn = get_db_connection()
    cursor = conn.cursor()

    if action == "full":
        refund_type = "Full"
        refund_amount = "100%"
    elif action == "partial":
        refund_type = "Partial"
        refund_amount = amount
    else:
        refund_type = "None"
        refund_amount = "0"

    cursor.execute("""
        UPDATE tickets
        SET status = ?, resolved_at = ?, refund_type = ?, refund_amount = ?, resolution_note = ?
        WHERE ticket_id = ?
    """, (
        "Resolved",
        datetime.now().isoformat(),
        refund_type,
        refund_amount,
        note,
        ticket_id
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": "Resolved"})