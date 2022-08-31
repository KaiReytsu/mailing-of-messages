import re
from datetime import datetime
from typing import List

from pydantic import BaseModel, validator


class ClientBase(BaseModel):
    phone_number: int
    mobile_code: int
    tag: str
    timezone: str

class ClientCreate(ClientBase):
    
    @validator('timezone')
    def is_valid(cls, v):
        compare_v = re.match('^[+-]+(?:2[0-3]|[01][0-9]):[0-5][0-9]$', v)
        if compare_v is None:
            raise ValueError('Timezone is not correct')
        return v

class Client(ClientBase):
    id: int

    class Config:
        orm_mode = True

class ClientDelete(BaseModel):
    phone_number: int

class ClientUpdate(ClientBase):
    @validator('timezone')
    def is_valid(cls, v):
        compare_v = re.match('^[+-]+(?:2[0-3]|[01][0-9]):[0-5][0-9]$', v)
        if compare_v is None:
            raise ValueError('Timezone is not correct')
        return v

class NewsletterBase(BaseModel):
    dt_start: datetime
    msg_text: str
    mobile_code: int
    tag: str
    dt_end: datetime

class NewsletterCreate(NewsletterBase):
    pass

class Newsletter(NewsletterBase):
    id: int

    class Config:
        orm_mode = True

class NewsletterDelete(BaseModel):
    id: int
