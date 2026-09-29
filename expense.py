
import tkinter as tk
from tkinter import messagebox


# =========================================================
# EXPENSE CLASS
# =========================================================

class Expense:

    def __init__(self, expense_id, name, amount, category):
        self.id = expense_id
        self.name = name
        self.amount = amount
        self.category = category


# =========================================================
# EXPENSE TRACKER CLASS
# =========================================================

class ExpenseTracker:

    def __init__(self):
        self.expenses = []
        self.next_id = 1

        self.load_expenses()

    # -----------------------------------------------------
    # ADD EXPENSE
    # -----------------------------------------------------

    def add_expense(self, name, amount, category):

        name = name.strip()

        if not name:
            return False, "Name cannot be empty."

        try:
            amount = int(amount)

            if amount <= 0:
                return False, "Amount must be greater than 0."

        except ValueError:
            return False, "Please enter a valid number."

        category = category.strip()

        if not category:
            return False, "Category cannot be empty."

        expense = Expense(
            self.next_id,
            name,
            amount,
            category
        )

        self.expenses.append(expense)

        self.next_id += 1

        self.save_expense(expense)

        return True, "Expense added successfully!"

    # -----------------------------------------------------
    # VIEW EXPENSES
    # -----------------------------------------------------

    def view_expenses(self):
        return self.expenses

    # -----------------------------------------------------
    # CALCULATE TOTAL
    # -----------------------------------------------------

    def calculate_expenses(self):

        total = 0

        for expense in self.expenses:
            total += expense.amount

        return total

    # -----------------------------------------------------
    # CATEGORY TOTAL
    # -----------------------------------------------------

    def category_total(self):

        category_totals = {}

        for expense in self.expenses:

            if expense.category not in category_totals:
                category_totals[expense.category] = 0

            category_totals[expense.category] += expense.amount

        return category_totals

    # -----------------------------------------------------
    # SEARCH BY NAME
    # -----------------------------------------------------

    def search_expense(self, search_name):

        search_name = search_name.strip().lower()

        results = []

        for expense in self.expenses:

            if search_name in expense.name.lower():
                results.append(expense)

        return results

    # -----------------------------------------------------
    # SEARCH BY ID
    # -----------------------------------------------------

    def search_by_id(self, expense_id):

        for expense in self.expenses:

            if expense.id == expense_id:
                return expense

        return None

    # -----------------------------------------------------
    # DELETE BY ID
    # -----------------------------------------------------

    def delete_expense(self, expense_id):

        for expense in self.expenses:

            if expense.id == expense_id:

                self.expenses.remove(expense)

                self.save_all_expenses()

                return True, "Expense deleted successfully!"

        return False, "Expense ID not found."

    # -----------------------------------------------------
    # UPDATE BY ID
    # -----------------------------------------------------

    def update_expense(self, expense_id, new_amount):

        for expense in self.expenses:

            if expense.id == expense_id:

                try:

                    new_amount = int(new_amount)

                    if new_amount <= 0:
                        return False, "Amount must be greater than 0."

                except ValueError:
                    return False, "Please enter a valid number."

                expense.amount = new_amount

                self.save_all_expenses()

                return True, "Expense updated successfully!"

        return False, "Expense ID not found."

    # -----------------------------------------------------
    # HIGHEST AND LOWEST
    # -----------------------------------------------------

    def highest_lowest_expense(self):

        if not self.expenses:
            return None, None

        highest = self.expenses[0]

        for expense in self.expenses:

            if expense.amount > highest.amount:
                highest = expense

        lowest = self.expenses[0]

        for expense in self.expenses:

            if expense.amount < lowest.amount:
                lowest = expense

        return highest, lowest

    # -----------------------------------------------------
    # LOAD EXPENSES
    # -----------------------------------------------------

    def load_expenses(self):

        try:

            with open("expenses.txt", "r") as file:

                for line in file:

                    line = line.strip()

                    if not line:
                        continue

                    parts = line.split(",")

                    # New format:
                    # ID,Name,Amount,Category

                    if len(parts) == 4:

                        try:

                            expense_id = int(parts[0])
                            name = parts[1]
                            amount = int(parts[2])
                            category = parts[3]

                        except ValueError:
                            continue

                        expense = Expense(
                            expense_id,
                            name,
                            amount,
                            category
                        )

                        self.expenses.append(expense)

                        if expense_id >= self.next_id:
                            self.next_id = expense_id + 1

                    # Old format:
                    # Name,Amount,Category

                    elif len(parts) == 3:

                        try:

                            name = parts[0]
                            amount = int(parts[1])
                            category = parts[2]

                        except ValueError:
                            continue

                        expense = Expense(
                            self.next_id,
                            name,
                            amount,
                            category
                        )

                        self.expenses.append(expense)

                        self.next_id += 1

        except FileNotFoundError:

            print("No expense file found. Starting fresh.")

        except ValueError:

            print("Invalid data found in expenses.txt.")

    # -----------------------------------------------------
    # SAVE ONE EXPENSE
    # -----------------------------------------------------

    def save_expense(self, expense):

        with open("expenses.txt", "a") as file:

            file.write(
                str(expense.id) + "," +
                expense.name + "," +
                str(expense.amount) + "," +
                expense.category + "\n"
            )

    # -----------------------------------------------------
    # SAVE ALL EXPENSES
    # -----------------------------------------------------

    def save_all_expenses(self):

        with open("expenses.txt", "w") as file:

            for expense in self.expenses:

                file.write(
                    str(expense.id) + "," +
                    expense.name + "," +
                    str(expense.amount) + "," +
                    expense.category + "\n"
                )


# =========================================================
# CREATE TRACKER
# =========================================================

tracker = ExpenseTracker()


# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()

root.title("Expense Tracker")

root.geometry("750x750")

root.resizable(False, False)


# =========================================================
# TITLE
# =========================================================

title_label = tk.Label(
    root,
    text="EXPENSE TRACKER",
    font=("Arial", 24, "bold")
)

title_label.pack(pady=20)


# =========================================================
# INPUT FRAME
# =========================================================

input_frame = tk.Frame(root)

input_frame.pack(pady=10)


# ---------------------------------------------------------
# NAME
# ---------------------------------------------------------

name_label = tk.Label(
    input_frame,
    text="Expense Name:",
    font=("Arial", 11)
)

name_label.grid(
    row=0,
    column=0,
    padx=10,
    pady=8
)

name_entry = tk.Entry(
    input_frame,
    width=35
)

name_entry.grid(
    row=0,
    column=1,
    padx=10,
    pady=8
)


# ---------------------------------------------------------
# AMOUNT
# ---------------------------------------------------------

amount_label = tk.Label(
    input_frame,
    text="Amount:",
    font=("Arial", 11)
)

amount_label.grid(
    row=1,
    column=0,
    padx=10,
    pady=8
)

amount_entry = tk.Entry(
    input_frame,
    width=35
)

amount_entry.grid(
    row=1,
    column=1,
    padx=10,
    pady=8
)


# ---------------------------------------------------------
# CATEGORY
# ---------------------------------------------------------

category_label = tk.Label(
    input_frame,
    text="Category:",
    font=("Arial", 11)
)

category_label.grid(
    row=2,
    column=0,
    padx=10,
    pady=8
)

category_entry = tk.Entry(
    input_frame,
    width=35
)

category_entry.grid(
    row=2,
    column=1,
    padx=10,
    pady=8
)


# =========================================================
# TEXT DISPLAY
# =========================================================

expense_list = tk.Text(
    root,
    width=75,
    height=10
)

expense_list.pack(pady=10)


# =========================================================
# REFRESH EXPENSES
# =========================================================

def refresh_expenses():

    expense_list.delete("1.0", tk.END)

    expenses = tracker.view_expenses()

    if not expenses:

        expense_list.insert(
            tk.END,
            "No expenses found."
        )

        return

    for expense in expenses:

        expense_list.insert(
            tk.END,
            f"ID       : {expense.id}\n"
            f"Name     : {expense.name}\n"
            f"Amount   : ₹{expense.amount}\n"
            f"Category : {expense.category}\n"
            f"{'-' * 45}\n"
        )


# =========================================================
# CLEAR INPUTS
# =========================================================

def clear_entries():

    name_entry.delete(0, tk.END)

    amount_entry.delete(0, tk.END)

    category_entry.delete(0, tk.END)


# =========================================================
# ADD EXPENSE
# =========================================================

def gui_add_expense():

    name = name_entry.get()

    amount = amount_entry.get()

    category = category_entry.get()

    success, message = tracker.add_expense(
        name,
        amount,
        category
    )

    if success:

        messagebox.showinfo(
            "Success",
            message
        )

        clear_entries()

        refresh_expenses()

    else:

        messagebox.showerror(
            "Error",
            message
        )


# =========================================================
# CALCULATE TOTAL
# =========================================================

def gui_calculate_total():

    total = tracker.calculate_expenses()

    messagebox.showinfo(
        "Total Expenses",
        f"Total Expense: ₹{total}"
    )


# =========================================================
# CATEGORY TOTAL
# =========================================================

def gui_category_total():

    category_totals = tracker.category_total()

    if not category_totals:

        messagebox.showinfo(
            "Category Total",
            "No expenses found."
        )

        return

    result = "===== Category Summary =====\n\n"

    for category, total in category_totals.items():

        result += f"{category} : ₹{total}\n"

    messagebox.showinfo(
        "Category Total",
        result
    )


# =========================================================
# SEARCH BY NAME
# =========================================================

def gui_search_expense():

    search_name = search_entry.get()

    results = tracker.search_expense(search_name)

    expense_list.delete(
        "1.0",
        tk.END
    )

    if not results:

        expense_list.insert(
            tk.END,
            "Expense not found."
        )

        return

    for expense in results:

        expense_list.insert(
            tk.END,
            f"ID       : {expense.id}\n"
            f"Name     : {expense.name}\n"
            f"Amount   : ₹{expense.amount}\n"
            f"Category : {expense.category}\n"
            f"{'-' * 45}\n"
        )


# =========================================================
# SEARCH BY ID
# =========================================================

def gui_search_by_id():

    id_value = id_entry.get().strip()

    if not id_value:

        messagebox.showerror(
            "Error",
            "Enter an ID."
        )

        return

    try:

        expense_id = int(id_value)

    except ValueError:

        messagebox.showerror(
            "Error",
            "Please enter a valid ID."
        )

        return

    expense = tracker.search_by_id(expense_id)

    expense_list.delete(
        "1.0",
        tk.END
    )

    if expense is None:

        expense_list.insert(
            tk.END,
            "Expense ID not found."
        )

        return

    expense_list.insert(
        tk.END,
        f"ID       : {expense.id}\n"
        f"Name     : {expense.name}\n"
        f"Amount   : ₹{expense.amount}\n"
        f"Category : {expense.category}\n"
        f"{'-' * 45}\n"
    )


# =========================================================
# DELETE EXPENSE
# =========================================================

def gui_delete_expense():

    id_value = id_entry.get().strip()

    if not id_value:

        messagebox.showerror(
            "Error",
            "Enter the expense ID."
        )

        return

    try:

        expense_id = int(id_value)

    except ValueError:

        messagebox.showerror(
            "Error",
            "Please enter a valid ID."
        )

        return

    expense = tracker.search_by_id(expense_id)

    if expense is None:

        messagebox.showerror(
            "Error",
            "Expense ID not found."
        )

        return

    result = messagebox.askyesno(
        "Confirm Delete",
        f"Delete Expense ID {expense_id}?\n\n"
        f"Name: {expense.name}\n"
        f"Amount: ₹{expense.amount}"
    )

    if not result:

        return

    success, message = tracker.delete_expense(
        expense_id
    )

    if success:

        messagebox.showinfo(
            "Success",
            message
        )

        id_entry.delete(
            0,
            tk.END
        )

        refresh_expenses()

    else:

        messagebox.showerror(
            "Error",
            message
        )


# =========================================================
# UPDATE EXPENSE
# =========================================================

def gui_update_expense():

    id_value = id_entry.get().strip()

    new_amount = amount_entry.get().strip()

    if not id_value:

        messagebox.showerror(
            "Error",
            "Enter the expense ID."
        )

        return

    if not new_amount:

        messagebox.showerror(
            "Error",
            "Enter the new amount in the Amount box."
        )

        return

    try:

        expense_id = int(id_value)

    except ValueError:

        messagebox.showerror(
            "Error",
            "Please enter a valid ID."
        )

        return

    success, message = tracker.update_expense(
        expense_id,
        new_amount
    )

    if success:

        messagebox.showinfo(
            "Success",
            message
        )

        id_entry.delete(
            0,
            tk.END
        )

        amount_entry.delete(
            0,
            tk.END
        )

        refresh_expenses()

    else:

        messagebox.showerror(
            "Error",
            message
        )


# =========================================================
# HIGHEST / LOWEST
# =========================================================

def gui_highest_lowest():

    highest, lowest = tracker.highest_lowest_expense()

    if highest is None:

        messagebox.showinfo(
            "Highest / Lowest",
            "No expenses found."
        )

        return

    result = (
        "===== Highest Expense =====\n\n"
        f"ID       : {highest.id}\n"
        f"Name     : {highest.name}\n"
        f"Amount   : ₹{highest.amount}\n"
        f"Category : {highest.category}\n\n"

        "===== Lowest Expense =====\n\n"
        f"ID       : {lowest.id}\n"
        f"Name     : {lowest.name}\n"
        f"Amount   : ₹{lowest.amount}\n"
        f"Category : {lowest.category}"
    )

    messagebox.showinfo(
        "Highest / Lowest",
        result
    )


# =========================================================
# BUTTON FRAME
# =========================================================

button_frame = tk.Frame(root)

button_frame.pack(pady=5)


# ---------------------------------------------------------
# ADD
# ---------------------------------------------------------

add_button = tk.Button(
    button_frame,
    text="Add Expense",
    width=18,
    command=gui_add_expense
)

add_button.grid(
    row=0,
    column=0,
    padx=5,
    pady=5
)


# ---------------------------------------------------------
# VIEW
# ---------------------------------------------------------

view_button = tk.Button(
    button_frame,
    text="View Expenses",
    width=18,
    command=refresh_expenses
)

view_button.grid(
    row=0,
    column=1,
    padx=5,
    pady=5
)


# ---------------------------------------------------------
# TOTAL
# ---------------------------------------------------------

total_button = tk.Button(
    button_frame,
    text="Calculate Total",
    width=18,
    command=gui_calculate_total
)

total_button.grid(
    row=0,
    column=2,
    padx=5,
    pady=5
)


# ---------------------------------------------------------
# CATEGORY
# ---------------------------------------------------------

category_button = tk.Button(
    button_frame,
    text="Category Total",
    width=18,
    command=gui_category_total
)

category_button.grid(
    row=1,
    column=0,
    padx=5,
    pady=5
)


# ---------------------------------------------------------
# HIGHEST / LOWEST
# ---------------------------------------------------------

highest_lowest_button = tk.Button(
    button_frame,
    text="Highest / Lowest",
    width=18,
    command=gui_highest_lowest
)

highest_lowest_button.grid(
    row=1,
    column=1,
    padx=5,
    pady=5
)


# =========================================================
# SEARCH FRAME
# =========================================================

search_frame = tk.Frame(root)

search_frame.pack(pady=8)


# ---------------------------------------------------------
# SEARCH BY NAME
# ---------------------------------------------------------

search_label = tk.Label(
    search_frame,
    text="Search Name:"
)

search_label.grid(
    row=0,
    column=0,
    padx=5,
    pady=5
)


search_entry = tk.Entry(
    search_frame,
    width=25
)

search_entry.grid(
    row=0,
    column=1,
    padx=5,
    pady=5
)


search_button = tk.Button(
    search_frame,
    text="Search Name",
    width=15,
    command=gui_search_expense
)

search_button.grid(
    row=0,
    column=2,
    padx=5,
    pady=5
)


# ---------------------------------------------------------
# SEARCH / UPDATE / DELETE BY ID
# ---------------------------------------------------------

id_label = tk.Label(
    search_frame,
    text="Expense ID:"
)

id_label.grid(
    row=1,
    column=0,
    padx=5,
    pady=5
)


id_entry = tk.Entry(
    search_frame,
    width=25
)

id_entry.grid(
    row=1,
    column=1,
    padx=5,
    pady=5
)


id_search_button = tk.Button(
    search_frame,
    text="Search ID",
    width=15,
    command=gui_search_by_id
)

id_search_button.grid(
    row=1,
    column=2,
    padx=5,
    pady=5
)


# =========================================================
# ID ACTION BUTTONS
# =========================================================

action_frame = tk.Frame(root)

action_frame.pack(pady=5)


# ---------------------------------------------------------
# UPDATE
# ---------------------------------------------------------

update_button = tk.Button(
    action_frame,
    text="Update Amount",
    width=18,
    command=gui_update_expense
)

update_button.grid(
    row=0,
    column=0,
    padx=5
)


# ---------------------------------------------------------
# DELETE
# ---------------------------------------------------------

delete_button = tk.Button(
    action_frame,
    text="Delete Expense",
    width=18,
    command=gui_delete_expense
)

delete_button.grid(
    row=0,
    column=1,
    padx=5
)


# =========================================================
# INITIAL DISPLAY
# =========================================================

refresh_expenses()


# =========================================================
# START GUI
# =========================================================

root.mainloop()




         
    
    