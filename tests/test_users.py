from fastapi.testclient import TestClient
import pytest
from app.main import app 
from app import schemas
from .database import client, session



def test_root(client):
    res = client.get("/")
    print (res.json())


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "test123@gmail.com", "password": "password123"})

    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "test123@gmail.com"
    assert res.status_code == 201    