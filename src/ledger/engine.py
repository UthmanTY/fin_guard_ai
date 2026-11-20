class InsufficientFundsError(Exception):
    pass
    

class InvalidTransactionError(Exception):
    pass

def withdraw(account, amount):
    if amount <= 0:
        raise InvalidTransactionError("Invalid transaction amount")

    if amount > account.account_balance:
        raise InsufficientFundsError("Insufficient funds")

    account.account_balance -= amount

    return account

def deposit(account, amount):
    if amount <= 0:
        raise InvalidTransactionError("Invalid transaction amount")

    account.account_balance += amount

    return account