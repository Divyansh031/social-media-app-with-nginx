from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from ..import schemas, models, utils
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(prefix="/users", tags=["Users"])  # Create a router for user-related endpoints


# User Endpoints


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut, responses={status.HTTP_409_CONFLICT: {"description": "User already exists"},})
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # 1. Check if a user with the provided email already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()

    if existing_user:
        # 2. If the user exists, raise an HTTP exception 
        #    (409 Conflict is often used for resource conflicts)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email '{user.email}' already exists"
        )

    # 3. If the user doesn't exist, proceed with creation
    # Hash the password before storing it
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{id}", response_model = schemas.UserOut) 
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id:{id} was not found")
    
    return user