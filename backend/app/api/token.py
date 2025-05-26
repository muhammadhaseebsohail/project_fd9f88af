Sure, here's a sample code snippet that describes the task:

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "YOUR_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    password: str

class UserInDB(User):
    hashed_password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

def fake_hash_password(password: str):
    return pwd_context.hash(password)

def fake_decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    return token_data

def fake_users_db(username: str):
    hashed_password = fake_hash_password("fakehashedpassword")
    return {"username": username, "hashed_password": hashed_password}

@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = fake_users_db(form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    hashed_password = fake_hash_password(form_data.password)
    if not pwd_context.verify(user.get("hashed_password"), hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.get("username")}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/")
def read_users_me(token: str = Depends(oauth2_scheme)):
    """
    Read user information
    """
    user = fake_users_db(token_info.username)
    if user is None:
        raise HTTPException(status_code=400, detail="User not found")
    return {"username": user.get('username'), "hashed_password": user.get('hashed_password')}
```

The code contains the following parts:
- The `/token` POST endpoint that accepts a username and password in form data and returns an access token.
- The `/users/me/` GET endpoint that requires a valid Authorization header with a Bearer token and returns the logged-in user's information.
- Helper functions to hash passwords, decode tokens, and simulate a user database.
- Pydantic models for the user, token data, and the user in the database.

Please replace `"YOUR_SECRET_KEY"` with your actual secret key. Remember that it should be a complex and secure key. You can generate it by running `openssl rand -hex 32` in the terminal.

This code is for demonstration purposes and should be adapted to your actual user model and database setup. The passwords should be hashed and stored securely, and the tokens should be generated and validated securely.