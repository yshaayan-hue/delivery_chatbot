import os
from flask import Flask, render_template, send_from_directory, session, redirect
from backend.routes.ticket_routes import ticket_bp
from backend.routes.auth_routes import auth_bp
from backend.database import init_db

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

app.secret_key = "supersecret123"

init_db()

app.register_blueprint(ticket_bp, url_prefix="/api")
app.register_blueprint(auth_bp, url_prefix="/api/auth")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/track")
def track():
    return render_template("track.html")


@app.route("/admin")
def admin_login():
    return render_template("admin_login.html")


@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin"):
        return redirect("/admin")
    return render_template("admin.html")


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    upload_folder = os.path.join(BASE_DIR, "uploads")
    return send_from_directory(upload_folder, filename)

    # ---------------- TICKET DETAILS PAGE ---------------- #
@app.route("/ticket/<ticket_id>")
def ticket_details_page(ticket_id):
    return render_template("details.html", ticket_id=ticket_id)


if __name__ == "__main__":
    app.run(debug=True)