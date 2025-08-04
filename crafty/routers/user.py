from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crafty.crud.user import create_user, delete_user, get_user, get_users
from crafty.db.session import get_db
from crafty.decorators import handle_http_exceptions
from crafty.exceptions import (InvalidUserTypeError, UserAlreadyExistsError,
                               UserNotFoundError)
from crafty.schemas.user import UserCreate, UserResponse
from crafty.schemas.user import BuyerCreate, SellerCreate


router = APIRouter(tags=["users"], prefix="/users")

exception_mapping = {
    UserAlreadyExistsError: 400,
    InvalidUserTypeError: 400,
    UserNotFoundError: 404,
}


@router.post("/buyers/", response_model=UserResponse)
@handle_http_exceptions(exception_mapping)
async def create_buyer(user: BuyerCreate, db: Session = Depends(get_db)) -> UserResponse:
    """Create a new user of type buyer.

    Args:
        user (UserCreate): The user data to create.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        UserResponse: The created user object.

    Raises:
        HTTPException: If a user with the same email or username already exists,
                       or other internal errors occur.
    """
    return create_user(db, user)


@router.post("/sellers/", response_model=UserResponse)
@handle_http_exceptions(exception_mapping)
async def create_seller(user: SellerCreate, db: Session = Depends(get_db)) -> UserResponse:
    """Create a new user of type seller.

    Args:
        user (UserCreate): The user data to create.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        UserResponse: The created user object.

    Raises:
        HTTPException: If a user with the same email or username already exists,
                       or other internal errors occur.
    """
    return create_user(db, user)

@router.get("/", response_model=List[UserResponse])
async def read_users(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> List[UserResponse]:
    """
    Retrieve a list of users with optional pagination.

    Args:
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 10.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        List[UserResponse]: A list of user objects.
    """
    return get_users(db, skip=skip, limit=limit)


@router.get("/email/{email}", response_model=UserResponse)
@handle_http_exceptions(exception_mapping)
async def read_user_by_email(email: str, db: Session = Depends(get_db)) -> UserResponse:
    """
    Get a user by their email.

    Args:
        email (str): The email of the user to retrieve.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        UserResponse: The retrieved user object.

    Raises:
        HTTPException: If the user is not found or other internal errors occur.
    """
    return get_user(db, email, "email")


@router.get("/username/{username}", response_model=UserResponse)
@handle_http_exceptions(exception_mapping)
async def read_user_by_username(
    username: str, db: Session = Depends(get_db)
) -> UserResponse:
    """
    Get a user by their username.

    Args:
        username (str): The username of the user to retrieve.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        UserResponse: The retrieved user object.

    Raises:
        HTTPException: If the user is not found or other internal errors occur.
    """
    return get_user(db, username, "username")


@router.get("/id/{user_id}", response_model=UserResponse)
@handle_http_exceptions(exception_mapping)
async def read_user_by_id(user_id: int, db: Session = Depends(get_db)) -> UserResponse:
    """
    Get a user by their ID.

    Args:
        user_id (int): The ID of the user to retrieve.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        UserResponse: The retrieved user object.

    Raises:
        HTTPException: If the user is not found or other internal errors occur.
    """
    return get_user(db, user_id, "id")


@router.delete("/{user_id}", status_code=204)
@handle_http_exceptions(exception_mapping)
async def delete_existing_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user.

    Args:
        user_id (int): The ID of the user to delete.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If the user is not found or other internal errors occur.
    """
    delete_user(db, user_id, "id")
