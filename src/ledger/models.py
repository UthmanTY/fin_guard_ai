from enum import Enum
from decimal import Decimal
from datetime import datetime, timezone
from pydantic import BaseModel, Field, field_validator, ConfigDict

class AccountType(Enum):
    SAVINGS = "Savings"
    CURRENT = "Current"
    BUSINESS = "Business"

class TransactionType(Enum):
    DEPOSIT = "Deposit"
    WITHDRAWAL = "Withdrawal"

class Account(BaseModel):
    @field_validator("account_name", mode="before")
    @classmethod
    def clean_account_name(cls, value):
        return value.strip()
    account_name: str = Field(min_length=1)
    account_type: AccountType
    account_balance: Decimal = Field(Decimal("0"), ge=0)

class Transaction(BaseModel):

    model_config = ConfigDict(frozen=True)

    transaction_id: str
    transaction_type: TransactionType
    amount: Decimal = Field(gt=0)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    description: str | None = None
