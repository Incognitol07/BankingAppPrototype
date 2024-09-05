import random
from pyfiglet import Figlet
import os

def clear_terminal():
    os.system('clear')

class Account:
    _assigned_account_numbers = set()

    def __init__(self):
        self._balance = 0
        self.total_deposit = 0
        self.total_withdrawn = 0
        self._account_no = self._generate_unique_account_no()

    @classmethod
    def _generate_unique_account_no(cls):
        while True:
            new_account_no = random.randint(10000000, 99999999)
            if new_account_no not in cls._assigned_account_numbers:
                cls._assigned_account_numbers.add(new_account_no)
                return new_account_no

    @property
    def balance(self):
        return self._balance

    @property
    def account_no(self):
        return self._account_no

    def deposit(self, amount: int):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.total_deposit += amount
        self._balance += amount

    def withdraw(self, amount: int):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds for withdrawal")
        self.total_withdrawn += amount
        self._balance -= amount

    def details(self):
        return (
            f"Account details:\n"
            f"Account No: {self._account_no}\n"
            f"Balance: {self._balance}\n"
            f"Total Deposited: {self.total_deposit}\n"
            f"Total Withdrawn: {self.total_withdrawn}"
        )

class Customer:
    _assigned_customer_ids = set()

    def __init__(self, name: str):
        self._name = name
        self._customer_id = self._generate_unique_customer_id()
        self._accounts = {}  # Dictionary mapping account_no to Account objects
        self._pin = None  # Initialize the PIN as None

    @classmethod
    def _generate_unique_customer_id(cls):
        while True:
            new_customer_id = random.randint(1000, 9999)
            if new_customer_id not in cls._assigned_customer_ids:
                cls._assigned_customer_ids.add(new_customer_id)
                return new_customer_id

    @property
    def customer_id(self):
        return self._customer_id

    @property
    def name(self):
        return self._name

    @property
    def accounts(self):
        if not self._accounts:
            return "No accounts found"
        result = ""
        for idx, account_no in enumerate(self._accounts, start=1):
            account = self._accounts[account_no]
            result += f"{idx}. Account No: {account.account_no}, Balance: {account.balance}\n"
        return result

    def add_account(self):
        account = Account()
        self._accounts[account.account_no] = account
        print(f"New account created with Account No: {account.account_no}")
        return account

    def get_account(self, account_no: int):
        if account_no in self._accounts:
            return self._accounts[account_no]
        else:
            raise ValueError(f"Account No: {account_no} not found")

    def remove_account(self, account_no: int):
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
    def __init__(self, name: str):
        self._name = name
        self._customers = {}  # Dictionary mapping customer_id to Customer objects

    @property
    def name(self):
        return self._name

    @property
    def customers(self):
        if not self._customers:
            return "No customers found"
        result = ""
        for idx, customer_id in enumerate(self._customers, start=1):
            customer = self._customers[customer_id]
            result += f"{idx}. Customer ID: {customer.customer_id}, Name: {customer.name}\n"
        return result

    def add_customer(self, customer_name: str, pin: str):
        customer = Customer(customer_name)
        customer.set_pin(pin)  # Set the PIN when adding the customer
        self._customers[customer.customer_id] = customer
        print(f"Customer Added with ID {customer.customer_id}")
        return customer

    def get_customer(self, customer_id: int):
        if customer_id in self._customers:
            return self._customers[customer_id]
        else:
            raise ValueError(f"Customer ID {customer_id} not found")

    def remove_customer(self, customer_id: int):
        if customer_id in self._customers:
            del self._customers[customer_id]
            print(f"Customer with ID {customer_id} removed")
        else:
            print("Customer ID is invalid")

    def transfer(self, sender_account: Account, recipient_account: Account, amount: int, pin: str):
        # Ensure both accounts exist
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")
        if amount > sender_account.balance:
            raise ValueError("Insufficient funds for transfer")
        
        # Verify PIN
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


