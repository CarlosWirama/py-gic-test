import datetime
import unittest

class Transaction:
    def __init__(self, date, account, txn_type, amount, txn_id):
        self.date = date
        self.account = account
        self.txn_type = txn_type.upper()
        self.amount = round(amount, 2)
        self.txn_id = txn_id

class Account:
    def __init__(self, account_id):
        self.account_id = account_id
        self.transactions = []
        self.balance = 0.0

    def add_transaction(self, date, txn_type, amount):
        if txn_type.upper() == "W" and (self.balance - amount < 0):
            raise ValueError("Insufficient balance")
        
        txn_id = self.generate_transaction_id(date)
        transaction = Transaction(date, self.account_id, txn_type, amount, txn_id)
        self.transactions.append(transaction)
        
        if txn_type.upper() == "D":
            self.balance += amount
        elif txn_type.upper() == "W":
            self.balance -= amount

    def generate_transaction_id(self, date):
        count = sum(1 for txn in self.transactions if txn.date == date)
        return f"{date}-{count + 1:02d}"

    def get_statement(self, year_month):
        statement = [txn for txn in self.transactions if txn.date.startswith(year_month)]
        return statement

class InterestRule:
    def __init__(self, date, rule_id, rate):
        self.date = date
        self.rule_id = rule_id
        self.rate = rate

class Bank:
    def __init__(self):
        self.accounts = {}
        self.interest_rules = []

    def add_transaction(self, date, account_id, txn_type, amount):
        if account_id not in self.accounts:
            self.accounts[account_id] = Account(account_id)
        self.accounts[account_id].add_transaction(date, txn_type, amount)

    def add_interest_rule(self, date, rule_id, rate):
        if rate <= 0 or rate >= 100:
            raise ValueError("Invalid interest rate")
        self.interest_rules = [rule for rule in self.interest_rules if rule.date != date]
        self.interest_rules.append(InterestRule(date, rule_id, rate))
        self.interest_rules.sort(key=lambda r: r.date)

    def calculate_interest(self, account_id, year_month):
        if account_id not in self.accounts:
            return 0.0
        
        statement = self.accounts[account_id].get_statement(year_month)
        if not statement:
            return 0.0
        
        end_of_day_balances = {}
        for txn in statement:
            end_of_day_balances[txn.date] = end_of_day_balances.get(txn.date, 0) + (txn.amount if txn.txn_type == "D" else -txn.amount)
        
        sorted_days = sorted(end_of_day_balances.keys())
        prev_balance = 0
        total_interest = 0
        
        for i, day in enumerate(sorted_days):
            balance = prev_balance + end_of_day_balances[day]
            applicable_rule = max((rule for rule in self.interest_rules if rule.date <= day), key=lambda r: r.date, default=None)
            if applicable_rule:
                num_days = (datetime.datetime.strptime(sorted_days[i], "%Y%m%d") - datetime.datetime.strptime(sorted_days[i-1], "%Y%m%d")).days if i > 0 else 1
                total_interest += (balance * applicable_rule.rate * num_days) / 365
            prev_balance = balance
        
        return round(total_interest, 2)
