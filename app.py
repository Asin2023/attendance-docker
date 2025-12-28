from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

def get_db():
    return sqlite3.connect("attendance.db")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        db.execute("INSERT INTO users (username, password) VALUES (?,?)",
                   (username, password))
        db.commit()
        db.close()
        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username=? AND password=?",
                          (username, password)).fetchone()
        db.close()

        if user:
            session["user"] = username
            return redirect("/")
    return render_template("login.html")

@app.route("/", methods=["GET", "POST"])
def index():
    if "user" not in session:
        return redirect("/login")

    db = get_db()

    if request.method == "POST":
        name = request.form["name"]
        status = request.form["status"]
        db.execute("INSERT INTO attendance (name, status) VALUES (?,?)",
                   (name, status))
        db.commit()

    records = db.execute("SELECT * FROM attendance").fetchall()
    db.close()

    return render_template("index.html", records=records)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
