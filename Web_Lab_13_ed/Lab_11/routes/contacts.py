from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from typing import List

from datetime import date

from shemas import ContactAdd, ContactUpdate, ContactBase
from database.db import get_db
from database.models import User

from repository.contacts_crud import search_contact, add_contact, update_contact, del_contact, all_contacts, search_born_date, search_born_date_7days
from repository.auth import get_current_user

from fastapi import Request
router = APIRouter()

from settings import limiter

@router.post("/contacts/", response_model=ContactBase)
@limiter.limit('1/minute')
def new_add_contact( request: Request, contact: ContactAdd, user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    db_contact = search_contact(db, user_id=user.id, contact_email=contact.email)

    if db_contact:

        raise HTTPException(status_code=400, detail="Email already registered")
    
    return add_contact(db=db, contact=contact, user_id=user.id)


@router.get("/contacts/", response_model=List[ContactBase])
@limiter.limit('1/minute')
def read_contacts( request: Request, user: User = Depends(get_current_user),  skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    contacts = all_contacts(db, user_id = user.id, skip=skip, limit=limit)
    
    return contacts


@router.get("/contacts/{contact_id}", response_model=ContactBase)
@limiter.limit('1/minute')
def read_contact_id(request: Request, contact_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    db_contact = search_contact(db,  user_id=user.id, contact_id=contact_id)

    if db_contact is None:

        raise HTTPException(status_code=404, detail="Contact not found")
    
    return db_contact


@router.get("/contacts/search/", response_model=ContactBase)
@limiter.limit('1/minute')
def read_contact_search( request: Request, user: User = Depends(get_current_user), firstname: str = None, lastname: str = None , email: str = None, db: Session = Depends(get_db)):

    if firstname:
        db_contact = search_contact(db, user_id=user.id, contact_firstname=firstname)
    
    elif lastname:
        db_contact = search_contact(db, user_id=user.id, contact_lastname=lastname)
    
    elif email:
        db_contact = search_contact(db, user_id=user.id, contact_email=email)

    else:

        raise HTTPException(status_code=404, detail="Contact not found")
    
    return db_contact


@router.put("/contacts/{contact_id}", response_model=ContactBase)
@limiter.limit('1/minute')
def update_contact( request: Request, contact_id: int, contact: ContactUpdate,user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    db_contact = search_contact(db, user_id=user.id, contact_id=contact_id)

    if db_contact is None:

        raise HTTPException(status_code=404, detail="Contact not found")
    
    return update_contact(db=db, contact_id=contact_id, contact=contact)


@router.delete("/contacts/{contact_id}", response_model=ContactBase)
@limiter.limit('1/minute')
def delete_contact( request: Request,  contact_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    db_contact = search_contact(db, user_id=user.id, contact_id=contact_id)

    if db_contact is None:

        raise HTTPException(status_code=404, detail="Contact not found")
    
    return del_contact(db=db, contact_id=contact_id)


@router.get("/contacts/contact_born_dates/", response_model=List[ContactBase])
@limiter.limit('1/minute')
def read_contacts_born_date( request: Request, contacts_born_date: date, user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    contacts = search_born_date(db, user_id=user.id, born_date=contacts_born_date)

    return contacts


@router.get("/contacts/borndate_next_7days/", response_model=List[ContactBase])
@limiter.limit('1/minute')
def read_contacts_7days( request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    contacts = search_born_date_7days(db, user_id=user.id)
    
    if not contacts:
        raise HTTPException(status_code=404, detail="No contacts found with birthdays in the next 7 days")
    return contacts