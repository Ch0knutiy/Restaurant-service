import httpx
import pytest


@pytest.fixture
def client():
    return httpx.AsyncClient()


@pytest.fixture
def host() -> str:
    return 'fastapi_ylab'
