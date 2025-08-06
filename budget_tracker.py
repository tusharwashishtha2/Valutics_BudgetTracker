import os

class Transaction:
    """Represents an individual income or expense entry."""

    def _init_(self, type, amount, category, notes=""):
        self.type = type.lower()
        self.amount = float(amount)
        self.category = category
        self.notes = notes

    def _str_(self):
        """
        Provides a user-friendly string for displaying the transaction.
        """
        return f"Type: {self.type.capitalize()}, Amount: ${self.amount:.2f}, Category: {self.category}, Notes: {self.notes}"

    def to_file_format(self):
        """
        Converts the transaction object into a consistent string format for file storage.
        """
        return f"{self.type}|{self.amount}|{self.category}|{self.notes}\n"

class BudgetTracker:
    """Manages the collection of transactions and user operations."""

    def _init_(self, filename="transactions.txt"):
        self.filename = filename
        self.transactions = []
        self.load_transactions()

    def add_transaction(self, trans_type, amount, category, notes=""):
        """Adds a new transaction to the tracker after validation."""
        try:
            amount = float(amount)
            if amount <= 0:
                print("Amount must be a positive number.")
                return
            if trans_type.lower() not in ['income', 'expense']:
                print("Invalid transaction type. Must be 'income' or 'expense'.")
                return

            new_transaction = Transaction(trans_type, amount, category, notes)
            self.transactions.append(new_transaction)
            self.save_transactions()
            print("Transaction added successfully.")
        except ValueError:
            print("Invalid amount. Please enter a valid number.")

    def list_all_transactions(self):
        """Displays all recorded transactions in a readable format."""
        if not self.transactions:
            print("No transactions to display.")
            return

        print("\n--- All Transactions ---")
        for i, t in enumerate(self.transactions, 1):
            print(f"{i}. {t}")
        print("------------------------\n")

    def filter_transactions(self, filter_by, value):
        """Filters transactions by type or category and displays them."""
        filtered_list = []
        if filter_by.lower() == 'type':
            filtered_list = [t for t in self.transactions if t.type == value.lower()]
        elif filter_by.lower() == 'category':
            filtered_list = [t for t in self.transactions if t.category.lower() == value.lower()]
        else:
            print("Invalid filter option. Use 'type' or 'category'.")
            return

        if not filtered_list:
            print(f"No transactions found for {filter_by}: {value}.")
            return

        print(f"\n--- Transactions filtered by {filter_by}: {value} ---")
        for t in filtered_list:
            print(t)
        print("------------------------------------------\n")

    def view_summary(self):
        """Calculates and displays total income, total expenses, and net balance."""
        total_income = sum(t.amount for t in self.transactions if t.type == 'income')
        total_expenses = sum(t.amount for t in self.transactions if t.type == 'expense')
        net_balance = total_income - total_expenses

        print("\n--- Financial Summary ---")
        print(f"Total Income: ${total_income:.2f}")
        print(f"Total Expenses: ${total_expenses:.2f}")
        print(f"Net Balance: ${net_balance:.2f}")
        print("-------------------------\n")

    def save_transactions(self):
        """Saves all transaction data to the transactions.txt file."""
        with open(self.filename, 'w') as f:
            for t in self.transactions:
                f.write(t.to_file_format())
        # print("Transactions saved successfully.")  # This can be commented out for cleaner output

    def load_transactions(self):
        """Loads transactions from the file on startup if it exists."""
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                for line in f:
                    try:
                        parts = line.strip().split('|')
                        if len(parts) == 4:
                            self.transactions.append(Transaction(*parts))
                        else:
                            print(f"Warning: Skipping malformed line in file: {line.strip()}")
                    except (ValueError, IndexError) as e:
                        print(f"Error loading transaction: {e}. Skipping line: {line.strip()}")
        # print("Transactions loaded on startup.")  # This can be commented out for cleaner output

def main():
    """Main function to run the command-line interface."""
    tracker = BudgetTracker()

    while True:
        print("\n--- Budget Tracker Menu ---")
        print("1. Add a Transaction")
        print("2. List All Transactions")
        print("3. Filter Transactions")
        print("4. View Summary")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            trans_type = input("Enter type (income/expense): ")
            amount = input("Enter amount: ")
            category = input("Enter category: ")
            notes = input("Enter optional notes: ")
            tracker.add_transaction(trans_type, amount, category, notes)

        elif choice == '2':
            tracker.list_all_transactions()

        elif choice == '3':
            filter_by = input("Filter by 'type' or 'category'?: ")
            if filter_by in ['type', 'category']:
                value = input(f"Enter the {filter_by} to filter by: ")
                tracker.filter_transactions(filter_by, value)
            else:
                print("Invalid filter option.")

        elif choice == '4':
            tracker.view_summary()

        elif choice == '5':
            print("Exiting application. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if _name_ == "_main_":
    main()