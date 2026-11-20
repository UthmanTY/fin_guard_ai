from ledger.models import *
from decimal import Decimal
import pytest
from pydantic import ValidationError
from ledger.engine import *

def test_account_balance_defaults_to_zero():
    account = Account(account_name="My Savings", account_type=AccountType.SAVINGS)
    assert account.account_balance == Decimal("0")

def test_invalid_account_type():
    with pytest.raises(ValidationError):
        Account(account_name="Test Account", account_type="Student")

def test_empty_account_name():
    with pytest.raises(ValidationError):
        Account(account_name="", account_type=AccountType.SAVINGS)

def test_whitespace_account_name():
    account = Account(account_name="   My Savings   ", account_type=AccountType.SAVINGS)
    assert account.account_name == "My Savings"

def test_whitespace_only_account_name():
    with pytest.raises(ValidationError):
        Account(account_name="   ", account_type=AccountType.SAVINGS)

def test_negative_account_balance():
    with pytest.raises(ValidationError):
        Account(account_type=AccountType.SAVINGS, account_balance=Decimal("-100"))

def test_successful_withdrawal():
    account = Account(account_name="My Savings", account_type=AccountType.SAVINGS, account_balance=Decimal("500"))
    returned_account = withdraw(account, Decimal("200"))
    assert returned_account.account_balance == Decimal("300")

def test_withdrawal_insufficient_funds():
    account = Account(account_name="My Savings", account_type=AccountType.SAVINGS, account_balance=Decimal("500"))
    with pytest.raises(InsufficientFundsError):
        withdraw(account, Decimal("700"))
    assert account.account_balance == Decimal("500")

def test_withdrawal_invalid_amount():
    account = Account(account_name="My Savings", account_type=AccountType.SAVINGS, account_balance=Decimal("500"))
    with pytest.raises(InvalidTransactionError):
        withdraw(account, Decimal("0"))
    with pytest.raises(InvalidTransactionError):
        withdraw(account, Decimal("-100"))
    assert account.account_balance == Decimal("500")

def test_successful_deposit():
    account = Account(account_name="My Savings", account_type=AccountType.SAVINGS, account_balance=Decimal("500"))
    returned_account = deposit(account, Decimal("200"))
    assert returned_account.account_balance == Decimal("700")

def test_deposit_invalid_amount():
    account = Account(account_name="My Savings", account_type=AccountType.SAVINGS, account_balance=Decimal("500"))
    with pytest.raises(InvalidTransactionError):
        deposit(account, Decimal("0"))
    with pytest.raises(InvalidTransactionError):
        deposit(account, Decimal("-100"))
    assert account.account_balance == Decimal("500")

def test_transaction_model_creation():
    transaction = Transaction(transaction_id="TXN-001", transaction_type=TransactionType.DEPOSIT, amount=Decimal("200"))
    assert isinstance(transaction, Transaction)
    assert transaction.timestamp is not None
    assert isinstance(transaction.timestamp, datetime)
    assert transaction.description is None