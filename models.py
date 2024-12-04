from datetime import datetime
import pytz
from marshmallow import fields
from config import db, ma

# SQLAlchemy Model for Note Table
class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.person_id'))
    content = db.Column(db.String, nullable=False)
    timestamp = db.Column(
        db.DateTime, default=lambda: datetime.now(pytz.timezone('Europe/London')),
        onupdate=lambda: datetime.now(pytz.timezone('Europe/London'))
    )

# Marshmallow Schema for Note Table
class NoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Note
        load_instance = True
        sqla_session = db.session

# SQLAlchemy Model for Person Table
class Person(db.Model):
    __tablename__ = "person"
    person_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lname = db.Column(db.String(32), unique=True)
    fname = db.Column(db.String(32))
    timestamp = db.Column(
        db.DateTime, default=lambda: datetime.now(pytz.timezone('Europe/London')),
        onupdate=lambda: datetime.now(pytz.timezone('Europe/London'))
    )
    notes = db.relationship(
        Note,
        backref="person",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="desc(Note.timestamp)"
    )

# Marshmallow Schema for Person Table
class PersonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Person
        load_instance = True
        sqla_session = db.session
        include_relationships = True

    notes = fields.Nested(NoteSchema, many=True)  # Correct Nested reference

class Account(db.Model):
    __tablename__ = "Account"
    AccountID = db.Column(db.Integer, primary_key=True)
    Email_address = db.Column(db.String(255), nullable=False, unique=True)
    Role = db.Column(db.String(255), nullable=False)

# Create schema instances
note_schema = NoteSchema()
person_schema = PersonSchema()
people_schema = PersonSchema(many=True)
