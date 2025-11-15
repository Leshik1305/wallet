from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Annotated
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class OperationEnum(StrEnum):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"


class WalletBase(BaseModel):
    id: Annotated[UUID, Field(description="Уникальный идентификатор кошелька")]
    balance: Annotated[Decimal, Field(description="Баланс кошелька")]
    created_at: Annotated[datetime, Field(description="Дата и время создания кошелька")]
    updated: Annotated[datetime | None, Field(description="Дата последней операции")]
    is_active: Annotated[bool, Field(default=True, description="Активность кошелька")]


class WalletCreate(WalletBase):
    id: Annotated[UUID, Field(default_factory=uuid4)]
    balance: Annotated[Decimal, Field(..., ge=0)]
    created_at: Annotated[datetime, Field(default_factory=datetime.now)]
    updated: Annotated[None, Field(default=None)]


class WalletRead(WalletBase):
    pass


class WalletUpdate(WalletBase):
    amount: Annotated[Decimal, Field(..., gt=0)]
    updated: Annotated[datetime, Field(default_factory=datetime.now)]
    operation: Annotated[OperationEnum, Field(default=OperationEnum.DEPOSIT)]
