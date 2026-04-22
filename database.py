import sqlite3

def create_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            amount REAL
        )
    ''')

    conn.commit()
    conn.close()


def insert_data(date, category, amount):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()

    c.execute("INSERT INTO expenses (date, category, amount) VALUES (?, ?, ?)",
              (date, category, amount))

    conn.commit()
    conn.close()


def fetch_data():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()

    c.execute("SELECT * FROM expenses")
    data = c.fetchall()

    conn.close()
    return data