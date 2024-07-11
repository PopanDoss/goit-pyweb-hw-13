from sqlalchemy.orm import Session
from database.models import Contact
from shemas import ContactAdd, ContactUpdate, ContactBase

from datetime import date, timedelta


def search_contact(db: Session, user_id: int, contact_id: int = None, contact_firstname: str = None, contact_lastname: str = None, contact_email: str = None):

    if contact_firstname:
        return db.query(Contact).filter(Contact.firstname == contact_firstname, Contact.created_by_id == user_id).first()
    
    elif contact_lastname:
        return db.query(Contact).filter(Contact.lastname == contact_lastname, Contact.created_by_id == user_id).first()

    elif contact_id:
        return db.query(Contact).filter(Contact.id == contact_id, Contact.created_by_id == user_id).first()
    
    elif contact_email:
        return db.query(Contact).filter(Contact.email == contact_email, Contact.created_by_id == user_id).first()


def all_contacts(db: Session, user_id: int, skip: int = 0, limit: int = 100):

    return db.query(Contact).filter(Contact.created_by_id == user_id).offset(skip).limit(limit).all()


def add_contact(db: Session, contact: ContactAdd,  user_id: int):

    db_contact = Contact(**contact.dict(), created_by_id=user_id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def update_contact(db: Session, contact_id: int, contact: ContactUpdate):

    db_contact = search_contact(db, contact_id=contact_id)

    if db_contact:

        for key, value in contact.dict(exclude_unset=True).items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact


def del_contact(db: Session, contact_id: int):

    db_contact = search_contact(db, contact_id=contact_id)
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact


def search_born_date(db: Session, user_id: int, born_date: date):

    return db.query(Contact).filter(Contact.born_date == born_date, Contact.created_by_id == user_id).all()

def search_born_date_7days(db: Session, user_id: int,):
    today = date.today()
    last_date = today + timedelta(days=7)
    return db.query(Contact).filter(Contact.born_date >= today, Contact.born_date <= last_date, Contact.created_by_id == user_id).all()
