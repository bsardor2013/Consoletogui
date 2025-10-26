from flask import Flask, render_template, request, redirect, url_for, session
from json import load, dump
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
import os
import random
import codeai
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "change_this_secret")
app.permanent_session_lifetime = timedelta(days=1)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    captcha = random.randint(1000, 9999)
    session["captcha"] = str(captcha)
    error = request.args.get("error")
    return render_template("login.html", captcha=captcha, error=error)

@app.route("/checklogin", methods=["POST"])
def checklogin():
    username = request.form.get("username")
    password = request.form.get("password")
    captcha_input = request.form.get("captcha")
    if not captcha_input or captcha_input != session.get("captcha"):
        return redirect(url_for("login", error="captcha"))
    try:
        with open("users.json", "r") as f:
            users = load(f) or {}
    except FileNotFoundError:
        users = {}
    stored = users.get(username)
    if stored and check_password_hash(stored, password):
        session.permanent = True
        session["username"] = username
        return redirect(url_for("dashboard"))
    return redirect(url_for("login", error="credentials"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            return render_template("register.html", error="missing")
        try:
            with open("users.json", "r") as f:
                users = load(f) or {}
        except FileNotFoundError:
            users = {}
        if username in users:
            return render_template("register.html", error="exists")
        users[username] = generate_password_hash(password)
        with open("users.json", "w") as f:
            dump(users, f)
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    user = session.get("username")
    if not user:
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=user)

@app.route("/protected")
def protected():
    return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
@app.route("/convertconsoletogui")
def convertconsoletogui():
    user = session.get("username")
    if not user:
        return redirect(url_for("login"))
    return render_template("convertconsoletogui.html", user=user)

@app.route("/convert", methods=["POST"])
def convert():
    user = session.get("username")
    if not user:
        return redirect(url_for("login"))
    console_code = request.form.get("python_code")  # changed name
    if not console_code:
        return render_template("convertconsoletogui.html", user=user, gui_code="Нет входного кода")
    gui_code = codeai.Ai(code=console_code).get_code()
    return render_template("convert.html", user=user, gui_code=gui_code)
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")
if __name__ == "__main__":
    app.run(debug=True)