import random
from pyfiglet import Figlet
import os

def clear_terminal():
    """Clears the terminal screen."""
    os.system('cls')  # On Windows; use 'clear' for Unix-based systems

class Account:
    """Represents a bank account with a unique account number and balance."""
    _assigned_account_numbers = set()  # Track assigned account numbers to ensure uniqueness

    def __init__(self):
        """Initialize the account with a balance of 0 and a unique account number."""
        self._balance = 0
        self.total_deposit = 0
        self.total_withdrawn = 0
        self._account_no = self._generate_unique_account_no()

    @classmethod
    def _generate_unique_account_no(cls):
        """Generate a unique account number."""
        while True:
            new_account_no = random.randint(10000000, 99999999)
            if new_account_no not in cls._assigned_account_numbers:
                cls._assigned_account_numbers.add(new_account_no)
                return new_account_no

    @property
    def balance(self):
        """Return the current balance of the account."""
        return self._balance

    @property
    def account_no(self):
        """Return the account number."""
        return self._account_no

    def deposit(self, amount: int):
        """Deposit a specified amount into the account."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.total_deposit += amount
        self._balance += amount

    def withdraw(self, amount: int):
        """Withdraw a specified amount from the account."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds for withdrawal")
        self.total_withdrawn += amount
        self._balance -= amount

    def details(self):
        """Return a string representation of the account details."""
        return (
            f"Account details:\n"
            f"Account No: {self._account_no}\n"
            f"Balance: {self._balance}\n"
            f"Total Deposited: {self.total_deposit}\n"
            f"Total Withdrawn: {self.total_withdrawn}"
        )

class Customer:
    """Represents a bank customer with multiple accounts and a PIN."""
    _assigned_customer_ids = set()  # Track assigned customer IDs to ensure uniqueness

    def __init__(self, name: str):
        """Initialize the customer with a unique ID and optional PIN."""
        self._name = name
        self._customer_id = self._generate_unique_customer_id()
        self._accounts = {}  # Dictionary mapping account_no to Account objects
        self._pin = None  # Initialize the PIN as None

    @classmethod
    def _generate_unique_customer_id(cls):
        """Generate a unique customer ID."""
        while True:
            new_customer_id = random.randint(1000, 9999)
            if new_customer_id not in cls._assigned_customer_ids:
                cls._assigned_customer_ids.add(new_customer_id)
                return new_customer_id

    @property
    def customer_id(self):
        """Return the customer ID."""
        return self._customer_id

    @property
    def name(self):
        """Return the customer's name."""
        return self._name

    @property
    def accounts(self):
        """Return a string representation of the customer's accounts and their balances."""
        if not self._accounts:
            return "No accounts found"
        result = ""
        for idx, account_no in enumerate(self._accounts, start=1):
            account = self._accounts[account_no]
            result += f"{idx}. Account No: {account.account_no}, Balance: {account.balance}\n"
        return result

    def add_account(self):
        """Create a new account for the customer and return it."""
        account = Account()
        self._accounts[account.account_no] = account
        print(f"New account created with Account No: {account.account_no}")
        return account

    def get_account(self, account_no: int):
        """Retrieve an account by its account number."""
        if account_no in self._accounts:
            return self._accounts[account_no]
        else:
            raise ValueError(f"Account No: {account_no} not found")

    def remove_account(self, account_no: int):
        """Remove an account by its account number."""
        if account_no in self._accounts:
            del self._accounts[account_no]
            print(f"Removed Account No: {account_no} successfully")
        else:
            print(f"Account No: {account_no} not found")

    def set_pin(self, pin: str):
        """Set or update the PIN for the customer."""
        self._pin = pin

    def verify_pin(self, pin: str):
        """Verify the PIN entered by the user."""
        return self._pin == pin

class Bank:
    """Represents a bank with multiple customers and functionality to handle transactions."""
    def __init__(self, name: str):
        """Initialize the bank with a name and an empty customer dictionary."""
        self._name = name
        self._customers = {}  # Dictionary mapping customer_id to Customer objects

    @property
    def name(self):
        """Return the bank's name."""
        return self._name

    @property
    def customers(self):
        """Return a string representation of the bank's customers."""
        if not self._customers:
            return "No customers found"
        result = ""
        for idx, customer_id in enumerate(self._customers, start=1):
            customer = self._customers[customer_id]
            result += f"{idx}. Customer ID: {customer.customer_id}, Name: {customer.name}\n"
        return result

    def add_customer(self, customer_name: str, pin: str):
        """Add a new customer to the bank with a specified PIN."""
        customer = Customer(customer_name)
        customer.set_pin(pin)  # Set the PIN when adding the customer
        self._customers[customer.customer_id] = customer
        print(f"Customer Added with ID {customer.customer_id}")
        return customer

    def get_customer(self, customer_id: int):
        """Retrieve a customer by their ID."""
        if customer_id in self._customers:
            return self._customers[customer_id]
        else:
            raise ValueError(f"Customer ID {customer_id} not found")

    def remove_customer(self, customer_id: int):
        """Remove a customer by their ID."""
        if customer_id in self._customers:
            del self._customers[customer_id]
            print(f"Customer with ID {customer_id} removed")
        else:
            print("Customer ID is invalid")

    def transfer(self, sender_account: Account, recipient_account: Account, amount: int, pin: str):
        """Transfer funds between accounts after verifying the sender's PIN."""
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")
        if amount > sender_account.balance:
            raise ValueError("Insufficient funds for transfer")
        
        # Verify PIN for the sender
        sender_customer = self._find_customer_by_account(sender_account)
        if not sender_customer.verify_pin(pin):
            raise ValueError("Invalid PIN")
        
        # Perform transfer
        sender_account.withdraw(amount)
        recipient_account.deposit(amount)
        print("Transfer successful")

    def _find_customer_by_account(self, account: Account):
        """Find the customer who owns the given account."""
        for customer in self._customers.values():
            if account.account_no in customer._accounts:
                return customer
        raise ValueError("Account not found in any customer")
    
    @classmethod
    def set_pin(cls, pin: str):
        """Set or update the PIN for the bank."""
        cls._pin = pin

    def verify_pin(self, pin: str):
        """Verify the PIN entered by the bank."""
        return self._pin == pin

class CLI:
    """Command Line Interface for interacting with the banking system."""

    def __init__(self):
        """Initialize the CLI with a figlet font for display purposes."""
        self.figlet = Figlet(font="coil_cop")
        self.title = "WELCOME TO CORZON"
        self.bank = None  # Initialize bank variable here

    def run(self):
        """Run the CLI to interact with the user and perform banking operations."""
        print(self.figlet.renderText(self.title))
        while True:
            print("The Simple Banking System....")
            print("""
            Main Menu:
                1. New Customer
                2. Existing Customer
                3. Bank Mode
                4. Exit
            """)
            choice = input("Choose an option: ")

            if choice == "1":
                self.new_customer()
            elif choice == "2":
                self.existing_customer()
            elif choice == "3":
                self.bank_mode()
            elif choice == "4":
                print("Exiting the system...")
                break
            else:
                print("Invalid option. Please choose again.")

    def new_customer(self):
        """Handle new customer registration."""
        if self.bank is None:
            self.initialize_bank()
        print("New Customer Registration")
        customer_name = input("Enter your name: ")
        pin = int(input("Set a 4-digit PIN: "))
        customer = self.bank.add_customer(customer_name, pin)
        print(f"Customer created successfully. Your ID is {customer.customer_id}")
        self.customer_mode(customer)

    def existing_customer(self):
        """Handle existing customer login."""
        if self.bank is None:
            print("No bank is initialized. Please initialize the bank in Bank Mode.")
            return
        try:
            customer_id = int(input("Enter your customer ID: "))
            pin = input("Enter your PIN: ")
            customer = self.bank.get_customer(customer_id)
            if customer.verify_pin(pin):
                print("Login successful.")
                self.customer_mode(customer)
            else:
                print("Invalid PIN.")
        except ValueError:
            print("Customer ID not found.")

    def bank_mode(self):
        """Bank operations."""
        if self.bank is None:
            self.initialize_bank()
            clear_terminal()
        while True:
            print(self.figlet.renderText(self.bank_name))
            print("""
            Bank Mode:
                1. View all customers
                2. Add a new customer
                3. Remove a customer
                4. Exit to main menu
            """)
            choice = input("Choose an option: ")

            if choice == "1":
                print(self.bank.customers)
            elif choice == "2":
                self.add_bank_customer()
            elif choice == "3":
                self.remove_bank_customer()
            elif choice == "4":
                print("Exiting to main menu...")
                break
            else:
                print("Invalid option. Please try again.")

    def initialize_bank(self):
        """Initialize the bank with a name and PIN."""
        print("Initializing the Bank...")
        self.bank_name = input("Enter the bank's name: ")
        self.bank = Bank(self.bank_name)
        while True:
            bank_pin = input("Set your 4-digit bank PIN: ")
            confirm_pin = input("Confirm your bank PIN: ")
            if bank_pin == confirm_pin:
                Bank.set_pin(bank_pin)
                print("Bank PIN set successfully.")
                break
            else:
                print("PINs do not match. Please try again.")

    def add_bank_customer(self):
        """Add a new customer manually from the bank mode."""
        customer_name = input("Enter the new customer's name: ")
        pin = input("Set a 4-digit PIN for the customer: ")
        customer = self.bank.add_customer(customer_name, pin)
        print(f"Customer added successfully. Customer ID: {customer.customer_id}")

    def remove_bank_customer(self):
        """Remove a customer from the bank mode."""
        try:
            customer_id = int(input("Enter the customer ID to remove: "))
            self.bank.remove_customer(customer_id)
        except ValueError:
            print("Invalid customer ID.")

    def customer_mode(self, customer):
        """Menu for customer operations."""
        while True:
            print(self.figlet.renderText(self.bank_name))

            # Display customer ID and account numbers at the top
            print(f"Customer ID: {customer.customer_id}")
            if customer.accounts != "No accounts found":
                print(f"Accounts:\n{customer.accounts}")
            else:
                print("No accounts available.")

            print("""
            Customer Mode:
                1. View all accounts and balances
                2. View details of a specific account
                3. Add a new account
                4. Delete an account
                5. Deposit money
                6. Withdraw money
                7. Transfer money
                8. Exit to main menu
            """)
            choice = input("Choose an option: ")

            if choice == "1":
                print(customer.accounts)
            elif choice == "2":
                try:
                    account_no = int(input("Enter the account number: "))
                    account = customer.get_account(account_no)
                    print(account.details())
                except ValueError:
                    print("Account not found.")
            elif choice == "3":
                customer.add_account()
            elif choice == "4":
                try:
                    account_no = int(input("Enter the account number to delete: "))
                    customer.remove_account(account_no)
                except ValueError:
                    print("Account not found.")
            elif choice == "5":
                self.deposit_money(customer)
            elif choice == "6":
                self.withdraw_money(customer)
            elif choice == "7":
                self.transfer_money(customer)
            elif choice == "8":
                print("Exiting to main menu...")
                break
            else:
                print("Invalid option. Please try again.")


    def deposit_money(self, customer):
        """Handle depositing money into an account."""
        try:
            account_no = int(input("Enter the account number to deposit into: "))
            account = customer.get_account(account_no)
            amount = int(input("Enter the amount to deposit: $"))
            account.deposit(amount)
            print(f"Deposit successful. New balance: {account.balance}")
        except ValueError as e:
            print(f"Error: {e}")

    def withdraw_money(self, customer):
        """Handle withdrawing money from an account."""
        try:
            account_no = int(input("Enter the account number to withdraw from: "))
            account = customer.get_account(account_no)
            amount = int(input("Enter the amount to withdraw: $"))
            account.withdraw(amount)
            print(f"Withdrawal successful. New balance: {account.balance}")
        except ValueError as e:
            print(f"Error: {e}")

    def transfer_money(self, customer):
        """Handle money transfer between accounts."""
        try:
            sender_acc_no = int(input("Enter your account number: "))
            sender_account = customer.get_account(sender_acc_no)
            recipient_acc_no = int(input("Enter recipient's account number: "))
            recipient_customer = self.bank.get_customer(
                int(input("Enter recipient's customer ID: ")))
            recipient_account = recipient_customer.get_account(recipient_acc_no)
            amount = int(input("Enter the amount to transfer: $"))
            pin = input("Enter your PIN for verification: ")
            self.bank.transfer(sender_account, recipient_account, amount, pin)
        except ValueError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    cli = CLI()
    cli.run()
