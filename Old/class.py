


class Transaction:
    def __init__(self, trans_id, from_id, to_id, amount, time, date, description, t_type):
        self.trans_id = trans_id
        self.from_id = from_id
        self.to_id = to_id
        self.amount = amount
        self.time = time
        self.date = date
        self.description = description
        self.t_type = t_type


class Account:
    def __init__(self, account_id, name, balance, created_t, created_d, last_modified, closed, closure_t, closure_d,
                 notes, transactions=None):
        if transactions is None:
            transactions = []
        self.account_id = account_id
        self.name = name
        self.balance = balance
        self.created_t = created_t
        self.created_d = created_d
        self.last_modified = last_modified
        self.closed = closed
        self.closure_t = closure_t
        self.closure_d = closure_d
        self.notes = notes
        self.transactions = transactions 


class Customer:
    def __init__(self, customer_id, f_name, l_name, phone, email, birthday, address, signup_d, signup_t, notes,
                 accounts=None):
        if accounts is None:
            accounts = []
        self.customer_id = customer_id
        self.f_name = f_name
        self.l_name = l_name
        self.phone = phone
        self.email = email
        self.birthday = birthday
        self.address = address
        self.signup_d = signup_d
        self.signup_t = signup_t
        self.notes = notes
        self.accounts = accounts

#calculate the balance of an account
def calc_balance(account):
    balance = 0
    for transaction in account.transactions:
        if transaction.from_id == account.account_id:
            balance -= transaction.amount
        elif transaction.to_id == account.account_id:
            balance += transaction.amount
    return balance