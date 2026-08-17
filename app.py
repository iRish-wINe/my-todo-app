import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# --- DATABASE SETUP ---
def init_db():
    # Connects to a local file database (it will automatically create it if it doesn't exist)
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    # Create a table to store tasks with an automated unique ID number
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Initialize the database file immediately when the app starts
init_db()

# Helper function to easily run database queries
def query_db(query, args=(), one=False):
    conn = sqlite3.connect("todo.db")
    # This magic line makes sqlite return rows as dictionaries so our HTML code still works perfectly!
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, args)
    rv = cursor.fetchall()
    conn.commit()
    conn.close()
    return (rv[0] if rv else None) if one else rv

# --- ROUTES ---
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        typed_text = request.form.get("todo_item")
        if typed_text:
            # INSERT the new task item directly into our database table
            query_db("INSERT INTO tasks (name) VALUES (?)", (typed_text,))
            
    # SELECT and retrieve all tasks currently saved in our database
    saved_tasks = query_db("SELECT * FROM tasks")
    return render_template("index.html", tasks=saved_tasks)

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    # DELETE the specific task row matching this ID from our database table
    query_db("DELETE FROM tasks WHERE id = ?", (task_id,))
    return redirect(url_for("home"))
@app.route("/clear")
def clear_all():
    # This SQL command deletes every single row inside the tasks table
    query_db("DELETE FROM tasks")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
