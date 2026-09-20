class Expense:
    def __init__(self, name, amount, category):
        self.name = name
        self.amount = amount
        self.category = category


class ExpenseTracker:

    def __init__(self):
        self.expenses = []
        self.load_expenses()

    # ---------------- ADD EXPENSE ----------------

    def add_expense(self):
        print("\n===== Add Expense =====")

        name = input("Enter the name: ").strip()

        if not name:
            print("Name cannot be empty.")
            return

        try:
            amount = int(input("Enter your expense: "))

            if amount <= 0:
                print("Amount must be greater than 0.")
                return

        except ValueError:
            print("Please enter a valid number.")
            return

        category = input("Enter your expense category: ").strip()

        if not category:
            print("Category cannot be empty.")
            return

        expense = Expense(name, amount, category)

        self.expenses.append(expense)
        self.save_expense(expense)

        print("Expense added successfully!")


    # ---------------- VIEW EXPENSES ----------------

    def view_expenses(self):
        print("\n===== All Expenses =====")

        if not self.expenses:
            print("No expenses found.")
            return

        for expense in self.expenses:
            print("-------------------------")
            print("Name     :", expense.name)
            print("Amount   :", expense.amount)
            print("Category :", expense.category)


    # ---------------- CALCULATE TOTAL ----------------

    def calculate_expenses(self):
        total = 0

        for expense in self.expenses:
            total += expense.amount

        print("\n===== Total Expense =====")
        print("Total:", total)


    # ---------------- CATEGORY TOTAL ----------------

    def category_total(self):
        if not self.expenses:
            print("No expenses found.")
            return

        category_totals = {}

        for expense in self.expenses:

            if expense.category not in category_totals:
                category_totals[expense.category] = 0

            category_totals[expense.category] += expense.amount

        print("\n===== Category Summary =====")

        for category, total in category_totals.items():
            print(category, ":", total)


    # ---------------- SEARCH EXPENSE ----------------

    def search_expense(self):
        search_name = input("Enter the name: ").strip().lower()

        found = False

        for expense in self.expenses:

            if search_name in expense.name.lower():
                found = True

                print("\n-------------------------")
                print("Name     :", expense.name)
                print("Amount   :", expense.amount)
                print("Category :", expense.category)

        if not found:
            print("Expense not found.")


    # ---------------- DELETE EXPENSE ----------------

    def delete_expense(self):
        expense_name = input("Enter the name: ").strip().lower()

        for expense in self.expenses:

            if expense_name == expense.name.lower():

                self.expenses.remove(expense)

                # Save updated list to file
                self.save_all_expenses()

                print("Expense deleted successfully!")
                return

        print("Expense not found.")


    # ---------------- UPDATE EXPENSE ----------------

    def update_expense(self):
        search_name = input("Enter the name: ").strip().lower()

        for expense in self.expenses:

            if search_name == expense.name.lower():

                print("\nCurrent amount:", expense.amount)

                try:
                    new_amount = int(
                        input("Enter the new amount: ")
                    )

                    if new_amount <= 0:
                        print("Amount must be greater than 0.")
                        return

                except ValueError:
                    print("Please enter a valid number.")
                    return

                expense.amount = new_amount

                # Save updated list to file
                self.save_all_expenses()

                print("Expense updated successfully!")
                return

        print("Expense not found.")


    # ---------------- HIGHEST / LOWEST ----------------

    def highest_lowest_expense(self):

        if not self.expenses:
            print("No expenses found.")
            return

        highest = self.expenses[0]

        for expense in self.expenses:

            if expense.amount > highest.amount:
                highest = expense

        lowest = self.expenses[0]

        for expense in self.expenses:

            if expense.amount < lowest.amount:
                lowest = expense

        print("\n===== Highest Expense =====")
        print("Name     :", highest.name)
        print("Amount   :", highest.amount)
        print("Category :", highest.category)

        print("\n===== Lowest Expense =====")
        print("Name     :", lowest.name)
        print("Amount   :", lowest.amount)
        print("Category :", lowest.category)


    # ---------------- LOAD EXPENSES ----------------

    def load_expenses(self):

        try:

            with open("expenses.txt", "r") as file:

                for line in file:

                    line = line.strip()

                    if not line:
                        continue

                    parts = line.split(",")

                    if len(parts) != 3:
                        continue

                    name = parts[0]
                    amount = int(parts[1])
                    category = parts[2]

                    expense = Expense(
                        name,
                        amount,
                        category
                    )

                    self.expenses.append(expense)

        except FileNotFoundError:
            print("No expense file found. Starting fresh.")

        except ValueError:
            print("Invalid data found in expenses.txt.")


    # ---------------- SAVE NEW EXPENSE ----------------

    def save_expense(self, expense):

        with open("expenses.txt", "a") as file:

            file.write(
                expense.name + "," +
                str(expense.amount) + "," +
                expense.category + "\n"
            )


    # ---------------- SAVE ALL EXPENSES ----------------

    def save_all_expenses(self):

        with open("expenses.txt", "w") as file:

            for expense in self.expenses:

                file.write(
                    expense.name + "," +
                    str(expense.amount) + "," +
                    expense.category + "\n"
                )


    # ---------------- MENU ----------------

    def menu(self):

        while True:

            print("\n================================")
            print("         EXPENSE TRACKER")
            print("================================")

            print("1. Add Expense")
            print("2. View Expenses")
            print("3. Calculate Total")
            print("4. Category Total")
            print("5. Search Expense")
            print("6. Delete Expense")
            print("7. Update Expense")
            print("8. Highest / Lowest")
            print("9. Exit")

            print("================================")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.add_expense()

            elif choice == "2":
                self.view_expenses()

            elif choice == "3":
                self.calculate_expenses()

            elif choice == "4":
                self.category_total()

            elif choice == "5":
                self.search_expense()

            elif choice == "6":
                self.delete_expense()

            elif choice == "7":
                self.update_expense()

            elif choice == "8":
                self.highest_lowest_expense()

            elif choice == "9":
                print("\nThank you for using Expense Tracker!")
                break

            else:
                print("Invalid choice. Please enter 1-9.")


# ---------------- START PROGRAM ----------------

tracker = ExpenseTracker()
tracker.menu()


         
    
    