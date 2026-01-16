from sqlmodel import Session, select
from models.todo_models import User, UserCreate
from typing import Optional
from utils.jwt_handler import get_password_hash, verify_password

def get_user_by_email(session: Session, email: str) -> Optional[User]:
    """Get a user by email"""
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    return user

def create_user_in_db(session: Session, user_create: UserCreate) -> User:
    """Create a new user in the database with hashed password"""
    # Hash the password before storing
    hashed_password = get_password_hash(user_create.password)
    
    db_user = User(
        email=user_create.email,
        name=user_create.name,
        password=hashed_password  # Store hashed password
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    """Authenticate a user by email and password"""
    user = get_user_by_email(session, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user