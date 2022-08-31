import enum

import sqlalchemy as sqla
from sqlalchemy.orm import relationship

from db import Base


class Client(Base):
    __tablename__ = 'client'
    id = sqla.Column(sqla.Integer, primary_key = True, index = True)
    phone_number = sqla.Column(sqla.BigInteger, unique = True)
    mobile_code = sqla.Column(sqla.Integer, index = True)
    tag = sqla.Column(sqla.String)
    timezone_time = sqla.Column(sqla.Time)
    timezone_sign = sqla.Column(sqla.Boolean)

class Newsletter(Base):
    __tablename__ = 'newsletter'
    id = sqla.Column(sqla.Integer, primary_key = True, index = True)
    dt_start = sqla.Column(sqla.DateTime)
    msg_text = sqla.Column(sqla.String)
    mobile_code = sqla.Column(sqla.Integer, index = True)
    tag = sqla.Column(sqla.String)
    dt_end = sqla.Column(sqla.DateTime)

class Status(enum.Enum):
    sent = 'Отправелно'
    not_sent = 'Не отправлено'

class Mail(Base):
    __tablename__ = 'mail'
    id = sqla.Column(sqla.Integer, primary_key = True, index = True)
    dt_sending = sqla.Column(sqla.DateTime)
    status_sending = sqla.Column(sqla.Enum(Status))
    client_id = sqla.Column(sqla.ForeignKey('client.id'))
    nemwletter_id = sqla.Column(sqla.ForeignKey('newsletter.id'))