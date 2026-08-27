from flask import Flask, request, redirect, session, url_for, render_template_string
import sqlite3
import bcrypt
import re

app = Flask(__name__)
app.secret_key = "change_this_to_a_random_secret_key"


# Create database and users table
def create_database():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password BLOB NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Home page
@app.route("/")
def home():
    if "username" in session:
        return f"""
        <h2>Welcome, {session['username']}!</h2>
        <p>You are logged in securely.</p>
        <a href="/logout">Logout</a>
        """

    return """
    <h2>Secure Login System</h2>
    <a href="/register">Register</a> |
    <a href="/login">Login</a>
    """


# User Registration
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        # Basic input validation
        if len(username) < 3:
            return "Username must contain at least 3 characters."

        if len(password) < 6:
            return "Password must contain at least 6 characters."

        # Allow only letters, numbers and underscore in username
        if not re.match("^[a-zA-Z0-9_]+$", username):
            return "Username can only contain letters, numbers and underscores."

        # Hash password using bcrypt
        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )

        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()

            # Parameterized query protects against SQL injection
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password)
            )

            conn.commit()
            conn.close()

            return redirect("/login")

        except sqlite3.IntegrityError:
            return "Username already exists."

    return render_template_string("""
        <h2>Register</h2>

        <form method="POST">
            Username:<br>
            <input type="text" name="username" required><br><br>

            Password:<br>
            <input type="password" name="password" required><br><br>

            <button type="submit">Register</button>
        </form>

        <br>
        <a href="/">Home</a>
    """)


# User Login
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        # Parameterized query prevents SQL injection
        cursor.execute(
            "SELECT password FROM users WHERE username = ?",
            (username,)
        )

        user = cursor.fetchone()
        conn.close()

        # Check hashed password
        if user and bcrypt.checkpw(
            password.encode("utf-8"),
            user[0]
        ):
            session["username"] = username
            return redirect("/")

        return "Invalid username or password."

    return render_template_string("""
        <h2>Login</h2>

        <form method="POST">
            Username:<br>
            <input type="text" name="username" required><br><br>

            Password:<br>
            <input type="password" name="password" required><br><br>

            <button type="submit">Login</button>
        </form>

        <br>
        <a href="/">Home</a>
    """)


# Logout
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/")


if __name__ == "__main__":
    create_database()
    app.run(debug=True)