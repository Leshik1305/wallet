from datetime import datetime
from decimal import Decimal
from typing import Annotated
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class WalletBase(BaseModel):
    id: Annotated[UUID, Field(description="Уникальный идентификатор кошелька")]
    balance: Annotated[Decimal, Field(description="Баланс кошелька") ]
    created_at: Annotated[datetime, Field(description="Дата и время создания кошелька")]
    updated_at: Annotated[datetime | None, Field(description="Дата последней операции")]
    is_active: Annotated[bool, Field(default=True, description="Активность кошелька")]


class WalletCreate(WalletBase):
    id: Annotated[UUID, Field(default_factory=uuid4)]
    balance: Annotated[Decimal, Field(..., ge=0)]
    created_at: Annotated[datetime, Field(default_factory=datetime.now)]


class WalletRead(WalletBase):
    pass