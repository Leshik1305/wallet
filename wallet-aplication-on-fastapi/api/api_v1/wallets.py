from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.schemas.wallet import WalletRead, WalletCreate, WalletUpdate
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


@router.get("/{wallet_uuid}", response_model=WalletRead, status_code=status.HTTP_200_OK)
async def get_wallet_by_id(
    id: UUID,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    wallet = await wallets_crud.get_wallet(
        session=session,
        id=id,
    )
    return wallet


@router.patch("/{wallet_uuid}/operation")
async def change_wallet_balance(
    id: UUID,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    wallet_update: WalletUpdate,
):
    wallet = await wallets_crud.change_balance(
        session=session,
        id=id,
        update_wallet=wallet_update,
    )
    return wallet
