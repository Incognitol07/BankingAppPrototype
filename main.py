import random

acc_list=[]
id_list=[]

class IDGenerator:
    @staticmethod
    def generate_unique_id(existing_ids, start=1000, end=9999):
        i = 0
        while i < 1:
            new_id = random.randint(start, end)
            if new_id not in existing_ids:
                existing_ids.append(new_id)
                return new_id


class Account:
    def __init__(self):
        self._balance=0
        self.total_deposit=0
        self.total_withdrawn=0
        self._account_no=IDGenerator.generate_unique_id(acc_list, 10000000, 99999999)

    @property
    def balance(self):
        return self._balance
    
    @property
    def account_no(self):
        return self._account_no

    def deposit(self, amount:int):
        self.amount=amount
        self.total_deposit+=self.amount
        self._balance+=self.amount
    
    def withdraw(self, amount:int):
        if amount<self._balance:
            self.amount=amount
            self.total_withdrawn+=self.amount
            self._balance-=self.amount
        elif amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        else:
            raise ValueError("Insufficient funds for withdrawal")

    def details(self):
        return (f"Account details:\n Account: {self._account_no}\n Balance: {self._balance}\n Total deposited: {self.total_deposit}\n Total withdrawn: {self.total_withdrawn}")

class Customer:
    def __init__(self, name: str):
        self._name = name
        self._customer_id = IDGenerator.generate_unique_id(id_list, 1000, 9999)
        self._accounts = []

    @property
    def customer_id(self):
        return self._customer_id
    
    @property
    def name(self):
        return self._name
    
    @property
    def accounts(self):
        result=""
        for idx, _account in enumerate(self._accounts, start=1):
            result += f"{idx}. {_account}\n"
        return result if result else "No accounts found"

    def add_account(self):
        account=Account()
        i=0
        while i<1:
            if account.account_no not in self._accounts:
                self._accounts.append(account.account_no)
                i+=1
        print(f"New account: {account.account_no}")
        return account
    
    def remove_account(self, account_no:int):
        if account_no in self._accounts:
            self._accounts.remove(account_no)
            print(f"You removed {account_no}")
        else:
            raise ValueError("Invalid account number")

class Bank:
    def __init__(self, name:str):
        self._name=name
        self._customers=[]


    @property
    def name(self):
        return self._name
    
    @property
    def customers(self):
        result=""
        for idx, _customer in enumerate(self._customers, start=1):
            result += f"{idx}. {_customer}\n"
        return result if result else "No customers found"
    
    def add_customer(self, customer_name:str):
        customer=Customer(customer_name)
        self._customers.append(customer.customer_id)
        print("Customer Added")
        return customer

    def remove_customer(self, customer_id:int):
        if customer_id in self._customers:
            self._customers.remove(customer_id)
            print(f"Customer with ID:{customer_id} removed")
        else:
            print("Customer ID is invalid")
    
    def transfer(self, sender:Account, recipient:Account, amount:int):
        if sender.account_no not in acc_list:
            print("Sender's account number is invalid")
        if recipient.account_no not in acc_list:
            print("Recipient's account number is invalid")
        if amount>sender.balance:
            print("Insufficient funds for transfer")
        else:
            sender.withdraw(amount)
            recipient.deposit(amount)
            print("Transfer successful")



