from flask import Flask, render_template, send_from_directory, request, redirect, session, url_for

# ---------------- ADMIN LOGIN ---------------- #

@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        password = request.form.get("password")

        if password == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect("/admin")
        else:
            return "Wrong password"

    return render_template("admin_login.html")


# ---------------- PROTECTED ADMIN ---------------- #

@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect("/admin-login")

    return render_template("admin.html")


# ---------------- LOGOUT ---------------- #

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/")