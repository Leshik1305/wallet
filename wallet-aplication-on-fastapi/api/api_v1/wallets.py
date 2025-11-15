from typing import Annotated

from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.schemas.wallet import WalletRead, WalletCreate
from .crud import wallets as wallets_crud

router = APIRouter(tags=["Wallets"])


@router.post("", response_model=WalletRead, status_code=status.HTTP_201_CREATED)
async def create_wallet(
    wallet_create: WalletCreate,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    wallet = await wallets_crud.create_wallet(
        session=session,
        wallet_create=wallet_create,
    )
    return wallet
