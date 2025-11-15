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
