from decimal import Decimal, getcontext
from ledger.models import Account

getcontext().prec = 40

class InsufficientFundsError(Exception):
    pass
    
class InvalidTransactionError(Exception):
    pass

def withdraw(account: Account, amount: Decimal) -> Account:
    """Withdraw money from an account.

    Args:
        account (Account): The account that money is withdrawn from.
        amount (Decimal): The amount to be withdrawn.

    Raises:
        TypeError: If the amount is not a Decimal.
        InvalidTransactionError: If the amount is zero or negative.
        InsufficientFundsError: If the amount is greater than the account's available balance.

    Returns:
        The updated Account object.
    """
    if not isinstance(amount, Decimal):
        raise TypeError("Amount must be a Decimal")
    if amount <= 0:
        raise InvalidTransactionError("Invalid transaction amount")
    if amount > account.account_balance:
        raise InsufficientFundsError("Insufficient funds")
    account.account_balance -= amount
    return account

def deposit(account: Account, amount: Decimal) -> Account:
    """Add money to an account.

    Args:
        account (Account): The account that money is deposited to.
        amount (Decimal): The amount to be deposited.

    Raises:
        TypeError: If the amount is not a Decimal.
        InvalidTransactionError: If the amount is zero or negative.

    Returns:
        The updated Account object.
    """
    if not isinstance(amount, Decimal):
        raise TypeError("Amount must be a Decimal")
    if amount <= 0:
        raise InvalidTransactionError("Invalid transaction amount")
    account.account_balance += amount
    return account
