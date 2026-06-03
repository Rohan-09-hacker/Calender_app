import sqlite3
from datetime import datetime

DB_NAME = "reminders.db"

def init_db():
    """Initializes the local SQLite database and creates the reminders table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_str TEXT NOT NULL,
            time_str TEXT NOT NULL,
            title TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_reminder(date_str, time_str, title):
    """Saves a new reminder directly into the persistent database storage."""
    try:
        # Validate time format quickly before inserting (HH:MM)
        datetime.strptime(time_str, "%H:%M")
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO reminders (date_str, time_str, title) VALUES (?, ?, ?)",
            (date_str, time_str, title)
        )
        conn.commit()
        conn.close()
        return True
    except ValueError:
        return False  # Invalid time format triggered

def get_reminders_for_date(date_str):
    """Fetches all scheduled reminders matching a specific targeted day (YYYY-MM-DD)."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, time_str, title FROM reminders WHERE date_str = ? ORDER BY time_str ASC",
        (date_str,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_reminder(reminder_id):
    """Removes a reminder permanently from the database via its unique entry key ID."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
    conn.commit()
    conn.close()

# --- Quick Engine Setup Test ---
if __name__ == "__main__":
    print("🗄️ Initializing persistent reminder engine database...")
    init_db()
    print("✅ Database successfully linked and setup.")