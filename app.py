from flask import Flask, request
import sqlite3
app = Flask(__name__)
DB_NAME = "feedback.db"
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            rating INTEGER NOT NULL,
            message TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
@app.route("/", methods=["GET"])
def index():
    return """
    <h2>Student Feedback Form</h2>
    <form method="POST" action="/submit">
        <label>Name:</label><br>
        <input type="text" name="name" required><br><br>

        <label>Email:</label><br>
        <input type="email" name="email" required><br><br>

        <label>Rating (1 to 5):</label><br>
        <input type="number" name="rating" min="1" max="5" required><br><br>

        <label>Feedback:</label><br>
        <textarea name="message" rows="4" cols="40" required></textarea><br><br>

        <button type="submit">Submit Feedback</button>
    </form>

    <br>
    <a href="/feedbacks">View All Feedback</a>
    """
@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    email = request.form.get("email")
    rating = request.form.get("rating")
    message = request.form.get("message")
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO feedback (name, email, rating, message) VALUES (?, ?, ?, ?)",
        (name, email, rating, message),
    )
    conn.commit()
    conn.close()
    return """
    <h3>Thank you! Your feedback has been submitted.</h3>
    <a href="/">Submit Another</a><br>
    <a href="/feedbacks">View All Feedback</a>
    """
@app.route("/feedbacks", methods=["GET"])
def view_feedbacks():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT name, email, rating, message FROM feedback ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    html = "<h2>All Feedback</h2>"
    html += '<a href="/">Back to Form</a><br><br>'
    if not rows:
        html += "<p>No feedback submitted yet.</p>"
        return html
    html += """
    <table border="1" cellpadding="8" cellspacing="0">
        <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Rating</th>
            <th>Message</th>
        </tr>
    """
    for row in rows:
        name, email, rating, message = row
        html += f"""
        <tr>
            <td>{name}</td>
            <td>{email}</td>
            <td>{rating}</td>
            <td>{message}</td>
        </tr>
        """
    html += "</table>"
    return html
if __name__ == "__main__":
    init_db()
    app.run(debug=True)