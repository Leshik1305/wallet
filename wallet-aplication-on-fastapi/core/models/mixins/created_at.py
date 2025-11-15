from datetime import datetime, timezone

from sqlalchemy import func, DateTime
from sqlalchemy.orm import Mapped, mapped_column


def get_current_dt() -> datetime:
    dt = datetime.now(tz=timezone.utc)
    return dt.replace(tzinfo=None)


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        server_default=func.now(),
    )
