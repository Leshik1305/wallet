import uuid

from sqlalchemy import UUID, text
from sqlalchemy.orm import Mapped, mapped_column


class IdUuidPkMixin:
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        index=True,
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
