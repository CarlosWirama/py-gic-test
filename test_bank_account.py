import unittest
from bank_account import Bank

class BankTests(unittest.TestCase):
    def setUp(self):
        self.bank = Bank()

    def test_transaction_deposit_withdraw(self):
        self.bank.add_transaction("20230601", "AC001", "D", 100.00)
        self.bank.add_transaction("20230602", "AC001", "W", 50.00)
        self.assertEqual(self.bank.accounts["AC001"].balance, 50.00)

    def test_insufficient_funds(self):
        self.bank.add_transaction("20230601", "AC001", "D", 50.00)
        with self.assertRaises(ValueError):
            self.bank.add_transaction("20230602", "AC001", "W", 100.00)

    def test_interest_calculation(self):
        self.bank.add_transaction("20230601", "AC001", "D", 200.00)
        self.bank.add_interest_rule("20230601", "RULE01", 2.0)
        interest = self.bank.calculate_interest("AC001", "202306")
        self.assertGreater(interest, 0)

    def test_transaction_id_format(self):
        self.bank.add_transaction("20230601", "AC001", "D", 100.00)
        self.bank.add_transaction("20230601", "AC001", "W", 50.00)
        self.assertEqual(self.bank.accounts["AC001"].transactions[0].txn_id, "20230601-01")
        self.assertEqual(self.bank.accounts["AC001"].transactions[1].txn_id, "20230601-02")

    def test_invalid_interest_rate(self):
        with self.assertRaises(ValueError):
            self.bank.add_interest_rule("20230601", "RULE01", -1.0)
        with self.assertRaises(ValueError):
            self.bank.add_interest_rule("20230601", "RULE02", 101.0)

    def test_print_statement_no_transactions(self):
        statement = self.bank.calculate_interest("AC999", "202306")
        self.assertEqual(statement, 0.0)

if __name__ == '__main__':
    unittest.main()
