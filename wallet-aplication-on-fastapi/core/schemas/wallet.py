from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field


class OperationEnum(StrEnum):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"


class WalletBase(BaseModel):
    balance: Annotated[Decimal, Field(..., ge=0, description="Баланс кошелька")]
    is_active: Annotated[bool, Field(default=True, description="Активность кошелька")]


class WalletCreate(WalletBase):
    pass


class WalletRead(WalletBase):
    id: Annotated[UUID, Field(description="Уникальный идентификатор кошелька")]
    created_at: Annotated[datetime, Field(description="Дата и время создания кошелька")]
    updated: Annotated[datetime | None, Field(description="Дата последней операции")]


class WalletUpdate(BaseModel):
    amount: Annotated[Decimal, Field(..., gt=0)]
    operation: Annotated[OperationEnum, Field(default=OperationEnum.DEPOSIT)]
