Sure, here is how you can write unit tests for your FastAPI application using pytest and FastAPI's TestClient. 

```python
from fastapi.testclient import TestClient
import pytest
from main import app, fake_hash_password, fake_users_db, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from jose import jwt

client = TestClient(app)

def test_read_users_me_success():
    response = client.get(
        "/users/me/",
        headers={"Authorization": "Bearer test_token"},
    )
    assert response.status_code == 200
    assert response.json() == {"username": "test_user", "hashed_password":  'fakehashedpassword'}

def test_read_users_me_fail():
    response = client.get("/users/me/")
    assert response.status_code == 401

def test_login_for_access_token_success():
    response = client.post(
        "/token",
        data={"username": "test_user", "password": "test_password"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_for_access_token_fail():
    response = client.post(
        "/token",
        data={"username": "wrong_user", "password": "wrong_password"},
    )
    assert response.status_code == 401

def test_token_expiry():
    user = fake_users_db("test_user")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = jwt.encode(
        {"sub": user.get("username"), "exp": timedelta(minutes=5)},
        "YOUR_SECRET_KEY",
        algorithm="HS256",
    )
    response = client.get(
        "/users/me/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}
```

The tests included are:
    
- `test_read_users_me_success` tests the route `/users/me` with a valid token and checks if the response data is correct.
- `test_read_users_me_fail` tests the route `/users/me` without a token and checks if it correctly responds with a 401 status.
- `test_login_for_access_token_success` tests the route `/token` with a valid username and password and checks if the response contains a token.
- `test_login_for_access_token_fail` tests the route `/token` with an invalid username and password and checks if it correctly responds with a 401 status.
- `test_token_expiry` tests that the token expires after the correct amount of time.

Please replace `"YOUR_SECRET_KEY"` with your actual secret key in the test `test_token_expiry`.

Remember that these tests are based on the fake user database and password hashing functions. In your actual tests, you should use your real database and password hashing functions.

Please also note that the test `test_token_expiry` uses a hardcoded 5 minutes expiry time. In your actual tests, you should use your real token expiry time.

To run the tests, simply execute `pytest` in the terminal.