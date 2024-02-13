import tkinter as tk
from tkinter import messagebox
from db_manager import DBManager

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Expense Tracker")

        # Initialize database manager
        self.db = DBManager()

        # Create buttons
        tk.Button(self.root, text="Add Expense", command=self.add_expense_window).pack(pady=10)
        tk.Button(self.root, text="View Expenses", command=self.view_expenses_window).pack(pady=10)
        tk.Button(self.root, text="Delete Expense", command=self.delete_expense_window).pack(pady=10)
        tk.Button(self.root, text="Modify Expense", command=self.modify_expense_window).pack(pady=10)

    
    def add_expense_window(self):
        window = tk.Toplevel(self.root)
        window.title("Add Expense")

        tk.Label(window, text="Category:").pack()
        category_entry = tk.Entry(window)
        category_entry.pack()

        tk.Label(window, text="Amount:").pack()
        amount_entry = tk.Entry(window)
        amount_entry.pack()

        tk.Label(window, text="Date (YYYY-MM-DD):").pack()
        date_entry = tk.Entry(window)
        date_entry.pack()

        tk.Button(window, text="Submit", command=lambda: self.add_expense(
            category_entry.get(),
            amount_entry.get(),
            date_entry.get(),
            window
        )).pack()

    def add_expense(self, category, amount, date, window):
        try:
            self.db.add_expense(category, float(amount), date)
            messagebox.showinfo("Success", "Expense added successfully")
            window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter the correct values.")


    def view_expenses_window(self):
        window = tk.Toplevel(self.root)
        window.title("View Expenses")

        expenses = self.db.fetch_expenses("2000-01-01", "2999-12-31")  # Fetch all expenses
        text_area = tk.Text(window, height=10, width=50)
        text_area.pack()

        for expense in expenses:
            text_area.insert(tk.END, f"ID: {expense[0]}, Category: {expense[1]}, Amount: {expense[2]}, Date: {expense[3]}\n")
        text_area.config(state=tk.DISABLED)


    def delete_expense_window(self):
        window = tk.Toplevel(self.root)
        window.title("Delete Expense")

        tk.Label(window, text="Expense ID:").pack()
        expense_id_entry = tk.Entry(window)
        expense_id_entry.pack()

        tk.Button(window, text="Delete", command=lambda: self.delete_expense(
            expense_id_entry.get(),
            window
        )).pack()

    def delete_expense(self, expense_id, window):
        try:
            expense_id = int(expense_id)
            self.db.delete_expense(expense_id)
            messagebox.showinfo("Success", "Expense deleted successfully")
            window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid ID. Please enter a numeric value.")
        except Exception as e:
            messagebox.showerror("Error", str(e))


    def modify_expense_window(self):
        window = tk.Toplevel(self.root)
        window.title("Modify Expense")

        tk.Label(window, text="Expense ID:").pack()
        expense_id_entry = tk.Entry(window)
        expense_id_entry.pack()

        tk.Label(window, text="New Category (leave blank to keep unchanged):").pack()
        new_category_entry = tk.Entry(window)
        new_category_entry.pack()

        tk.Label(window, text="New Amount (leave blank to keep unchanged):").pack()
        new_amount_entry = tk.Entry(window)
        new_amount_entry.pack()

        tk.Label(window, text="New Date (YYYY-MM-DD, leave blank to keep unchanged):").pack()
        new_date_entry = tk.Entry(window)
        new_date_entry.pack()

        tk.Button(window, text="Modify", command=lambda: self.modify_expense(
            expense_id_entry.get(),
            new_category_entry.get(),
            new_amount_entry.get(),
            new_date_entry.get(),
            window
        )).pack()

    def modify_expense(self, expense_id, new_category, new_amount, new_date, window):
        try:
            expense_id = int(expense_id)
            new_amount = float(new_amount) if new_amount else None

            self.db.update_expense(expense_id, new_category, new_amount, new_date)
            messagebox.showinfo("Success", "Expense modified successfully")
            window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please check your values.")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
