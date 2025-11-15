from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Wallet
from core.schemas.wallet import WalletCreate


async def create_wallet(
    session: AsyncSession,
    wallet_create: WalletCreate,
) -> Wallet:
    wallet = Wallet(**wallet_create.model_dump())
    session.add(wallet)
    await session.commit()
    await session.refresh(wallet)
    return wallet


async def get_wallet(
    session: AsyncSession,
    id: UUID,
) -> Wallet:
    stmt = select(Wallet).where(Wallet.id == id, Wallet.is_active)
    wallet = await session.scalar(stmt)
    if not wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Кошелек по данному ID не найден",
        )
    return wallet
