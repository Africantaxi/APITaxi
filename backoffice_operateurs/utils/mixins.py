from flask.ext.login import current_user
from datetime import datetime
from flask import request
from sqlalchemy_defaults import Column
from sqlalchemy.types import Integer, DateTime, Enum, String
from sqlalchemy.schema import ForeignKey
from sqlalchemy.ext.declarative import declared_attr


class AsDictMixin:
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class HistoryMixin:

    @declared_attr
    def added_by(self):
        return Column(Integer, ForeignKey('user.id'))

    added_at = Column(DateTime)
    added_via = Column(Enum('form', 'api', name="sources"))
    source = Column(String(255), default='added_by')
    last_update_at = Column(DateTime, nullable=True)

    @classmethod
    def to_exclude(cls):
        return [attr for attr in cls.__dict__.keys() if\
                attr.startswith('_') and\
                attr in ['added_by', 'to_exclude', 'can_be_listed_by',
                    'can_be_edited_by', 'can_be_deleted_by', 'showable_fields']]

    def __init__(self):
        self.added_by = current_user.id if current_user else None
        self.added_at = datetime.now().isoformat()
        self.added_via = 'form' if 'form' in request.url_rule else 'api'
        self.source = 'added_by'

    def can_be_deleted_by(self, user):
        return user.has_role("admin") or self.added_by == user.id

    def can_be_edited_by(self, user):
        return user.has_role("admin") or self.added_by == user.id

    @classmethod
    def can_be_listed_by(cls, user):
        return user.has_role("admin")

    def showable_fields(self, user):
        if user.has_role("admin") or self.added_by == user.id:
            return set([k for k in self.__dict__.keys() if k not in self.__class__.to_exclude()])
        cls = self.__class__
        return cls.public_fields if hasattr(cls, "public_fields") else set()
