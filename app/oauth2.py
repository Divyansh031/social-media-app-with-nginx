from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")  # Define the OAuth2 scheme for token retrieval

#SECRET_KEY
#Expiration Time
#Algorithm

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes 

def create_access_token(data: dict):  # data = the payload to encode in the JWT
    to_encode = data.copy()  # Create a copy of the data to avoid modifying the original
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})  # Add the expiration time to the payload
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # Encode the payload, SECRET_KEY  into a JWT
    return encoded_jwt  # Return the encoded JWT token

def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # Decode the JWT token
        id: str = payload.get("user_id")  # Extract the user ID from the payload
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=str(id))  # Create a TokenData object with the user ID
    except JWTError:
        raise credentials_exception 
    return token_data  # Return the TokenData object

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()  # Query the database for the user with the ID from the token
    return user  # Verify the access token and return the current user
