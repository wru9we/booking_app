from httpx import AsyncClient
import pytest


@pytest.mark.parametrize("email,password,status_code", [
    ("testing@mal.com", "testtest", 200),
    ("testing@mal.com", "test1test", 409),
    ("tested@mal.com", "test23test", 200),
    ("ergq", "testtest", 422),

])
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "email": email,
        "password": password,
    })

    assert response.status_code == status_code


@pytest.mark.parametrize("email,password,status_code", [
    ("test@test.com", "test", 200),
    ("wru9we@example.com", "artem", 200),
])
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/login", json={
        "email": email,
        "password": password,
    })

    assert response.status_code == status_code