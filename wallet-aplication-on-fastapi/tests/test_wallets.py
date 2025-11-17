import asyncio
import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from core.models import Base, db_helper
from main import main_app

TEST_DATABASE_URL = "postgresql+asyncpg://admin:1234@localhost:5432/test"


@pytest.fixture(scope="module", autouse=True)
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
async def client():
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
    main_app.dependency_overrides[db_helper.session_getter] = lambda: SessionLocal()

    async with AsyncClient(app=main_app, base_url="http://test") as aclient:
        yield aclient
    await engine.dispose()


@pytest.mark.anyio
async def test_create_wallet(client):
    """Тест на создание нового кошелька"""
    response = await client.post("/api/v1/wallets", json={"balance": 100})
    assert response.status_code == 201
    data = response.json()
    print(data)
    assert isinstance(data["id"], str)
    assert float(data["balance"]) == 100.0
    assert isinstance(uuid.UUID(data["id"]), uuid.UUID)
    assert data["is_active"] == True


@pytest.mark.anyio
async def test_read_wallet(client):
    """Тест на получение кошелька по UUID"""
    response = await client.post("/api/v1/wallets", json={"balance": 100})
    wallet_data = response.json()
    wallet_uuid = wallet_data["id"]
    print(type(wallet_uuid))

    response = await client.get(f"/api/v1/wallets/{wallet_uuid}")
    if response.status_code != 200:
        print("Error details:", response.text)
    print(response)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == wallet_uuid
    assert float(data["balance"]) == 100.00
    random_uuid = uuid.uuid4()
    assert data["id"] != random_uuid


@pytest.mark.anyio
async def test_update_wallet(client):
    """Тесты на изменение баланса кошелька"""
    response = await client.post("/api/v1/wallets", json={"balance": 100})
    wallet_data = response.json()
    wallet_id = wallet_data["id"]

    first_update = {"amount": 100, "operation": "deposit"}
    response = await client.patch(
        f"/api/v1/wallets/{wallet_id}/operation", json=first_update
    )
    assert response.status_code == 200
    data = response.json()
    assert float(data["balance"]) == 200.00

    second_update = {"amount": 100, "operation": "withdraw"}
    response = await client.patch(
        f"/api/v1/wallets/{wallet_id}/operation", json=second_update
    )
    assert response.status_code == 200
    data = response.json()
    assert float(data["balance"]) == 100.00

    third_update = {"amount": 200, "operation": "withdraw"}
    response = await client.patch(
        f"/api/v1/wallets/{wallet_id}/operation", json=first_update
    )
    assert response.status_code == 400
