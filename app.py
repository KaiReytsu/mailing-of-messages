from fastapi import Depends, FastAPI, HTTPException
from fastapi_utils.tasks import repeat_every
from sqlalchemy.orm import Session

import crud
import models
import schemas
from db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/clients/", response_model=schemas.Client)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    db_client = crud.get_client_by_phone_number(db, phone_number=client.phone_number)
    if db_client:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    return crud.create_client(db=db, client=client)

@app.delete("/clients/{phone_number}", response_model=schemas.ClientDelete)
def delete_client(phone_number: int, db: Session = Depends(get_db)):
    db_client = crud.get_client_by_phone_number(db, phone_number=phone_number)
    if db_client:
        return crud.delete_client(db=db, client=db_client)
    raise HTTPException(status_code=404, detail="There is no client with that phone number")
    
@app.patch("/clients/", response_model=schemas.ClientUpdate)
def update_client(client: schemas.ClientUpdate, db: Session = Depends(get_db)):
    db_client = crud.get_client_by_phone_number(db, phone_number=client.phone_number)
    if not db_client:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    return crud.update_client(db=db, client=client)

@app.post("/newsletter/", response_model=schemas.Newsletter)
def create_newsletter(newsletter: schemas.NewsletterCreate, db: Session = Depends(get_db)):
    return crud.create_newsletter(db=db, newsletter=newsletter)

@app.patch("/newsletter/", response_model=schemas.Newsletter)
def update_newsletter(newsletter: schemas.Newsletter, db: Session = Depends(get_db)):
    db_newsletter = crud.get_newsletter(db, id = newsletter.id)
    if not db_newsletter:
        raise HTTPException(status_code=400, detail="There is no such newsletter")
    return crud.update_newsletter(db=db, newsletter=newsletter, db_newsletter=db_newsletter)

@app.delete("/newsletter/{id}", response_model=schemas.NewsletterDelete)
def delete_newsletter(id: int, db: Session = Depends(get_db)):
    db_newsletter = crud.get_newsletter(db, id=id)
    if db_newsletter:
        return crud.delete_newsletter(db=db, newsletter=db_newsletter)
    raise HTTPException(status_code=404, detail="There is no such newsletter")

# @app.on_event("startup")
# @repeat_every(seconds=60)
# def funcname():
#     pass
