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
                        default=datetime.datetime.utcnow)
    user_id = reference_col('users', nullable=True)
    user = relationship('User', backref='notes')

    def __init__(self, title="", content="", **kwargs):
        """Create instance."""
        db.Model.__init__(self, title=title, content=content, **kwargs)

    def __str__(self):
        """String representation of the note. Shows the notes title."""
        return self.title


class Calendar_entry(SurrogatePK, Model):
    """A google calendar entry."""

    __tablename__ = 'calendar_entries'

    google_cal_id = Column(db.Integer, nullable=False)
    google_cal_entry_link = Column(db.String(200), nullable=False, unique=True)
    note_id = reference_col('notes', nullable=True)
    note = relationship('Note', backref='calendar_entries')

    def __init__(self, google_cal_id=None,
                 google_cal_entry_link=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self,
                          google_cal_id=google_cal_id,
                          google_cal_entry_id=google_cal_entry_link,
                          **kwargs)

    def __str__(self):
        return 'Note: {0}, Google Calendar Entry: {1}'
