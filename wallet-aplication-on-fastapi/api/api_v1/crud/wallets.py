from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Wallet
from core.schemas.wallet import WalletCreate, WalletUpdate, OperationEnum


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


async def change_balance(
    session: AsyncSession,
    id: UUID,
    update_wallet: WalletUpdate,
) -> Wallet:
    wallet = await get_wallet(session=session, id=id)
    if update_wallet.operation == OperationEnum.DEPOSIT:
        await session.execute(
            update(Wallet)
            .where(Wallet.id == id)
            .values(
                balance=wallet.balance + update_wallet.amount,
                updated=update_wallet.updated,
            )
        )
        await session.commit()
        await session.refresh(wallet)
        return wallet
    if update_wallet.amount > wallet.balance:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Недостаточно средств на счету",
        )
    await session.execute(
        update(Wallet)
        .where(Wallet.id == id)
        .values(
            balance=wallet.balance - update_wallet.amount,
            updated=update_wallet.updated,
        )
    )
    await session.commit()
    await session.refresh(wallet)
    return wallet
