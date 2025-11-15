from datetime import datetime

from sqlalchemy import Boolean, Numeric, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from . import Base
from .mixins.created_at import CreatedAtMixin
from .mixins.uuid_pk import IdUuidPkMixin


class Wallet(IdUuidPkMixin, CreatedAtMixin, Base):
    balance: Mapped[float] = mapped_column(
        Numeric(10, 2),
    )
    updated: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    def __repr__(self):
        return f"Wallet - {self.id}. Balance - {self.balance}"
