from fastapi.security import OAuth2PasswordBearer , SecurityScopes
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Annotated
from models.models_user import *
from fastapi import Depends , HTTPException , status 
from dependencies import *
from queries.user_queries import *




# Create a custom security scheme
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl= "token" , scopes = {
        "admin": "Full access to admin-level resources",
        "user": "Read-only access to user-level resources",
    } )

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=150)  # Default to 150 minutes
    to_encode.update({"exp": expire})  # Add expiration to token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



async def get_current_user(security_scopes: SecurityScopes,token: Annotated[str, Depends(oauth2_scheme)] , conn = Depends(establish_conn)):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = int(payload.get("sub"))
        # print(f'==========================================DAME EN GET_CURRENT_USER {id}')
        if id is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes = token_scopes ,id=id) 
    except JWTError:
        raise credentials_exception
    with conn:
        user = conn.execute(AUTHORIZE_TOKEN_QUERY , (token_data.id ,)).fetchone()
        if user is None:
            raise credentials_exception 
        for scope in security_scopes.scopes:
            if scope not in token_data.scopes:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not enough permissions",
                    headers={"WWW-Authenticate": authenticate_value},
                )
    is_admin = "admin" in token_data.scopes
    return {"user": user[0], "is_admin": is_admin}


async def get_current_active_user(current_user: Annotated[str, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_user_ws(token: Annotated[str, Depends(oauth2_scheme)], conn = Depends(establish_conn)):
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        print('Decoding JWT token...')
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(id=user_id)
    except JWTError as e:
        print(f"JWT decoding error: {e}")
        raise credentials_exception

    try:
        with conn:
            user = conn.execute(AUTHORIZE_TOKEN_QUERY, (token_data.id,)).fetchone()
            print(f'THIS IS THE USER AUTH {user}')
        if user is None:
            raise credentials_exception
    except Exception as e:
        print(f"Database query error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

    return user[0]