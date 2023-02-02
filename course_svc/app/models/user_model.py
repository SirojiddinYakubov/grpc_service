import sqlalchemy as db
from sqlalchemy.orm import relationship

from .base_model import Base


class Roles(Base):
    role_name = db.Column(db.String, nullable=False, unique=True)
    display_name = db.Column(db.String, nullable=True)


class Permissions(Base):
    permission_name = db.Column(db.String, nullable=False, unique=True)
    display_name = db.Column(db.String, nullable=True)


class RolePermissions(Base):
    role_id = db.Column(db.Integer, db.ForeignKey(Roles.id), primary_key=True)
    # role = relationship('Roles', foreign_keys='RolePermissions.role_id')

    permission_id = db.Column(db.Integer, db.ForeignKey(Permissions.id), primary_key=True)
    # permission = relationship('Permissions', foreign_keys='RolePermissions.role_id')


class Users(Base):
    first_name = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String, nullable=True)
    mobile = db.Column(db.String, nullable=True)
    verified_at = db.Column(db.DateTime, nullable=True)
    email = db.Column(db.String, nullable=False, unique=True)


class UserRoles(Base):
    role_id = db.Column(db.Integer, db.ForeignKey(Roles.id), primary_key=True)
    # role = relationship('Roles', foreign_keys='UserRoles.role_id')

    user_id = db.Column(db.Integer, db.ForeignKey(Users.id), primary_key=True)
    # user = relationship('Users', foreign_keys='UserRoles.role_id')
