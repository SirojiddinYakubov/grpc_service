import re
import datetime

import sqlalchemy as db
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.orm.query
import sqlalchemy.event
from typing import Set, Optional


def camelcase_to_snakecase(name: str) -> str:
    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    return pattern.sub('_', name).lower()


class Base(object):
    @declared_attr
    def __tablename__(cls):
        return camelcase_to_snakecase(cls.__name__)

    # __table_args__ = {'mysql_engine': 'InnoDB'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column('created_at', db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column('updated_at', db.DateTime, onupdate=datetime.datetime.now)
    deleted_at = db.Column(db.DateTime, default=None)


Base = declarative_base(cls=Base)

# @db.event.listens_for(db.orm.Mapper, 'refresh', named=True)
# def on_instance_refresh(target: type,
#                         context: db.orm.query.QueryContext,
#                         attrs: Optional[Set[str]]):
#     ssn: sqlalchemy.orm.Session = context.session
#     # target.deleted_at = datetime.datetime.now
#     print(38, target.id, attrs)
#     return target
