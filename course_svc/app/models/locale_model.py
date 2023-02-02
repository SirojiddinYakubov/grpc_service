import sqlalchemy as db

from .base_model import Base


class Locales(Base):
    name = db.Column(db.String, nullable=False)
    code = db.Column(db.String, nullable=False, unique=True)
    is_main = db.Column(db.Boolean, default=False)
