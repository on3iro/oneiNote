# -*- coding: utf-8 -*-
"""Notes models."""
import datetime

from oneiNote.database import Column, Model, SurrogatePK, db, \
    reference_col, relationship


class Note(SurrogatePK, Model):
    """A single note of a user."""

    __tablename__ = 'notes'

    title = Column(db.String(160), unique=True, nullable=False)
    content = Column(db.Text, nullable=True)
    created_at = Column(db.DateTime, nullable=False,
                        default=datetime.datetime.now)
    user_id = reference_col('users', nullable=True)
    user = relationship('User', backref='notes')

    def __init__(self, title="", content="", **kwargs):
        """Create instance."""
        db.Model.__init__(self, title=title, content=content, **kwargs)

    def __str__(self):
        """String representation of the note. Shows the notes title."""
        return self.title
