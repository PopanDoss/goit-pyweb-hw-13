
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException
from passlib.context import CryptContext

from sqlalchemy.orm import Session
from jose import JWTError, jwt
from starlette import status

from database.db import get_db

from settings import SECRET_KEY, ALGORITHM, oauth2_scheme


def create_email_token( data: dict, SECRET_KEY = SECRET_KEY , ALGORITHM = ALGORITHM ):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"iat": datetime.utcnow(), "exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

async def get_email_from_token(token: str, SECRET_KEY = SECRET_KEY , ALGORITHM = ALGORITHM):
  try:
      payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
      email = payload["sub"]
      return email
  except JWTError as e:
      print(e)
      raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                          detail="Invalid token for email verification")