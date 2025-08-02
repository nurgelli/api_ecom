from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User as DBUser
from app.schemas.user import UserCreate, User as UserSchema
from app.core.security import security
from app.api.deps import get_current_active_user

router = APIRouter()



@router.post('/users/', response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(DBUser).filter(DBUser.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    db_user = db.query(DBUser).filter(DBUser.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
        
    hashed_password = security.get_password_hash(user.password)
    
    new_user = DBUser(
        email=user.email,
        hashed_password=hashed_password,
        is_active=True,
        is_superuser=False
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
@router.get("/users/me", response_model=UserSchema)
def read_users_me(
    current_user: UserSchema = Depends(get_current_active_user),
):
    return current_user