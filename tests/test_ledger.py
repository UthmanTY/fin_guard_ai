from decimal import Decimal
from datetime import datetime
import pytest
from pydantic import ValidationError
from ledger.models import Account, AccountType, Transaction, TransactionType
from ledger.engine import deposit, withdraw, InsufficientFundsError, InvalidTransactionError

def test_account_balance_defaults_to_zero():
    account = Account(
        account_name="My Savings",
        account_type=AccountType.SAVINGS
    )
    assert account.account_balance == Decimal("0")

def test_invalid_account_type():
    with pytest.raises(ValidationError):
        Account(
            account_name="Test Account",
            account_type="Student"
        )

def test_empty_account_name():
    with pytest.raises(ValidationError):
        Account(
            account_name="",
            account_type=AccountType.SAVINGS
        )

def test_whitespace_account_name():
    account = Account(
        account_name="   My Savings   ",
        account_type=AccountType.SAVINGS
    )
    assert account.account_name == "My Savings"

def test_whitespace_only_account_name():
    with pytest.raises(ValidationError):
        Account(
            account_name="   ",
            account_type=AccountType.SAVINGS
        )

def test_negative_account_balance():
    with pytest.raises(ValidationError):
        Account(
            account_type=AccountType.SAVINGS,
            account_balance=Decimal("-100")
        )

def test_successful_withdrawal():
    account = Account(
        account_name="My Savings",
        account_type=AccountType.SAVINGS,
        account_balance=Decimal("500")
    )
    returned_account = withdraw(account, Decimal("200"))
    assert returned_account.account_balance == Decimal("300")

def test_withdrawal_insufficient_funds():
    account = Account(
        account_name="My Savings",
        account_type=AccountType.SAVINGS,
        account_balance=Decimal("500")
        )
    with pytest.raises(InsufficientFundsError):
        withdraw(account, Decimal("700"))
    assert account.account_balance == Decimal("500")

@pytest.mark.parametrize(
    "amount",
    [Decimal("0"), Decimal("-100"), Decimal("-50")]
)
def test_withdrawal_invalid_amount(amount):
    account = Account(
        account_name="My Savings",
        account_type=AccountType.SAVINGS,
        account_balance=Decimal("500")
        )
    with pytest.raises(InvalidTransactionError):
        withdraw(account, amount)
    assert account.account_balance == Decimal("500")

def test_successful_deposit():
    account = Account(
        account_name="My Savings",
        account_type=AccountType.SAVINGS,
        account_balance=Decimal("500")
    )
    returned_account = deposit(account, Decimal("200"))
    assert returned_account.account_balance == Decimal("700")
@pytest.mark.parametrize(
        "amount",
        [Decimal("0"), Decimal("-100"), Decimal("-50")]
)
def test_deposit_invalid_amount(amount):
    account = Account(
        account_name="My Savings",
        account_type=AccountType.SAVINGS,
        account_balance=Decimal("500")
    )
    with pytest.raises(InvalidTransactionError):
        deposit(account, amount)
    assert account.account_balance == Decimal("500")

def test_transaction_model_creation():
    transaction = Transaction(
        transaction_id="TXN-001",
        transaction_type=TransactionType.DEPOSIT,
        amount=Decimal("200")
    )
    assert isinstance(transaction, Transaction)
    assert transaction.timestamp is not None
    assert isinstance(transaction.timestamp, datetime)
    assert transaction.description is None

def test_invalid_transaction():
    with pytest.raises(ValidationError):
        Transaction(
            transaction_id="TXN-001",
            transaction_type=TransactionType.DEPOSIT,
            amount=Decimal("0")
        )
    with pytest.raises(ValidationError):
        Transaction(
            transaction_id="TXN-002",
            transaction_type=TransactionType.WITHDRAWAL
        )

def test_withdrawal_invalid_datetype():
    account = Account(
        account_name="My Savings",
        account_type=AccountType.SAVINGS,
        account_balance=Decimal("500")
    )
    with pytest.raises(TypeError):
        withdraw(account, 200.50)
    assert account.account_balance == Decimal("500")

def test_deposit_invalid_datetype():
    account = Account(
        account_name="My Savings",
        account_type=AccountType.SAVINGS,
        account_balance=Decimal("500")
    )
    with pytest.raises(TypeError):
        deposit(account, 200.50)
    assert account.account_balance == Decimal("500")

def test_withdrawal_exact_balance():
    account = Account(
        account_name="My Savings",
        account_type=AccountType.SAVINGS,
        account_balance=Decimal("500")
    )
    updated_account = withdraw(account, Decimal("500"))
    assert updated_account.account_balance == Decimal("0")

def test_deposit_small_decimal_amount():
    account = Account(
            account_name="My Savings",
            account_type=AccountType.SAVINGS,
            account_balance=Decimal("500")
        )
    updated_account = deposit(account, Decimal("0.01"))
    assert updated_account.account_balance == Decimal("500.01")

def test_deposit_large_amount():
    account = Account(
                account_name="My Savings",
                account_type=AccountType.SAVINGS,
                account_balance=Decimal("500")
            )
    updated_account = deposit(account, Decimal("999999999999999999999999999999.99"))
    assert updated_account.account_balance == Decimal("1000000000000000000000000000499.99")