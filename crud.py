from datetime import datetime, time

from sqlalchemy.orm import Session

import models
import schemas


def get_client(db: Session, client_id: int):
    return db.query(models.Client).filter(models.Client.id == client_id).first()


def get_client_by_phone_number(db: Session, phone_number: int):
    return db.query(models.Client).filter(models.Client.phone_number == phone_number).first()


def create_client(db: Session, client: schemas.ClientCreate):
    timezone_sign, timezone_time = timezone_parse(client.timezone)
    db_client = models.Client(
                                phone_number = client.phone_number, 
                                mobile_code = client.mobile_code, 
                                tag = client.tag, 
                                timezone_sign = timezone_sign, 
                                timezone_time = timezone_time
                            )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return schemas.Client(
                            id = db_client.id,
                            phone_number = db_client.phone_number,
                            mobile_code = db_client.mobile_code,
                            tag = db_client.tag,
                            timezone = client.timezone
                        )
def delete_client(db: Session, client: models.Client):
    db.delete(client)
    db.commit()
    return schemas.ClientDelete(phone_number=client.phone_number)

def update_client(db:Session, client: schemas.Client):
    db_client: models.Client = get_client_by_phone_number(db = db, phone_number=client.phone_number)
    db_client.mobile_code = client.mobile_code
    db_client.tag = client.tag
    db_client.timezone_sign, db_client.timezone_time = timezone_parse(client.timezone)
    db.commit()
    db.refresh(db_client)
    return schemas.Client(
                            id = db_client.id,
                            phone_number = db_client.phone_number,
                            mobile_code = db_client.mobile_code,
                            tag = db_client.tag,
                            timezone = client.timezone
                                                    )
def timezone_parse(timezone: str):                     
    timezone_sign: bool
    timezone_time: time
    if timezone[0] == '+':
        timezone_sign = True
    else:
        timezone_sign = False
    timezone_time = datetime.strptime(timezone[1:], '%H:%M').time()
    return timezone_sign, timezone_time

def create_newsletter(db:Session, newsletter: schemas.NewsletterCreate):
    db_newsletter = models.Newsletter(    
                                        dt_start = newsletter.dt_start,
                                        msg_text = newsletter.msg_text,
                                        mobile_code = newsletter.mobile_code,
                                        tag = newsletter.tag,
                                        dt_end = newsletter.dt_end
                                    )
    db.add(db_newsletter)
    db.commit()
    db.refresh(db_newsletter)
    return schemas.Newsletter(
                                id = db_newsletter.id,
                                dt_start= db_newsletter.dt_start,
                                msg_text= db_newsletter.msg_text,
                                mobile_code= db_newsletter.mobile_code,
                                tag = db_newsletter.tag,
                                dt_end= db_newsletter.dt_end
                            )
def get_newsletter(db: Session, id: int):
    return db.query(models.Newsletter).filter(models.Newsletter.id == id).first()

def update_newsletter(db:Session, newsletter: schemas.Newsletter, db_newsletter: models.Newsletter):
    db_newsletter.dt_start = newsletter.dt_start
    db_newsletter.msg_text = newsletter.msg_text
    db_newsletter.mobile_code = newsletter.mobile_code
    db_newsletter.tag = newsletter.tag
    db_newsletter.dt_end = newsletter.dt_end
    db.commit()
    db.refresh(db_newsletter)
    return schemas.Newsletter(
                            id = db_newsletter.id,
                            dt_start = db_newsletter.dt_start,
                            msg_text = db_newsletter.msg_text,
                            mobile_code = db_newsletter.mobile_code,
                            tag = db_newsletter.tag,
                            dt_end = db_newsletter.dt_end
                                                    )
def delete_newsletter(db: Session, newsletter: models.Newsletter):
    db.delete(newsletter)
    db.commit()
    return schemas.NewsletterDelete(id = newsletter.id)