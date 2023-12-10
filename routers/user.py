from fastapi import APIRouter, status, Response, HTTPException, Depends
import models, schemas, utils
from database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

# CRUD Operations for Users

# Create
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_posts(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = utils.hash(user.password)

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Read
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.User)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")

    return user
