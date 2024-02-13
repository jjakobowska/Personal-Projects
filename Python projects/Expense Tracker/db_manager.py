import sqlite3

class DBManager:
    def __init__(self, db_name="expenses.db"):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.setup()

    def setup(self):
        query = """CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )"""
        self.cur.execute(query)
        self.conn.commit()

    def add_expense(self, category, amount, date):
        query = "INSERT INTO expenses (category, amount, date) VALUES (?, ?, ?)"
        self.cur.execute(query, (category, amount, date))
        self.conn.commit()

    def fetch_expenses(self, start_date, end_date):
        query = "SELECT * FROM expenses WHERE date BETWEEN ? AND ?"
        self.cur.execute(query, (start_date, end_date))
        return self.cur.fetchall()

    def close(self):
        self.conn.close()
        
    def delete_expense(self, expense_id):
        query = "DELETE FROM expenses WHERE id = ?"
        self.cur.execute(query, (expense_id,))
        self.conn.commit()

    def update_expense(self, expense_id, category=None, amount=None, date=None):
        updates = []
        params = []

        if category:
            updates.append("category = ?")
            params.append(category)
        if amount:
            updates.append("amount = ?")
            params.append(amount)
        if date:
            updates.append("date = ?")
            params.append(date)

        params.append(expense_id)
        update_query = ", ".join(updates)
        query = f"UPDATE expenses SET {update_query} WHERE id = ?"

        if updates:
            self.cur.execute(query, tuple(params))
            self.conn.commit()
