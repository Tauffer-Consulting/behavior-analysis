from . import db
from datetime import datetime


class Experiment(db.Model):
    """Data model for Experiments"""

    __tablename__ = 'experiment'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.Text,
        unique=True,
        nullable=False
    )
    description = db.Column(
        db.Text,
        unique=True,
        nullable=True
    )
    groups = db.relationship(
        "Group",
        back_populates="experiment"
    )

    def __repr__(self):
        return f'<Experiment: {self.name}>'


class Group(db.Model):
    """Data model for Groups"""

    __tablename__ = 'group'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )
    experiment_id = db.Column(
        db.Integer,
        db.ForeignKey('experiment.id'),
        nullable=False
    )
    experiment = db.relationship(
        "Experiment",
        back_populates="groups"
    )
    subjects = db.relationship(
        "Subject",
        back_populates="group"
    )

    def __repr__(self):
        return '<Group: {}>'.format(self.name)


class Subject(db.Model):
    """Data model for Subjects"""

    __tablename__ = 'subject'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    group_id = db.Column(
        db.Integer,
        db.ForeignKey('group.id'),
        nullable=False
    )
    group = db.relationship(
        "Group",
        back_populates="subjects"
    )
    file = db.Column(
        db.Text,
        nullable=False
    )
    date = db.Column(
        db.DateTime,
        unique=False,
        nullable=False,
        default=datetime.utcnow
    )

    def __repr__(self):
        return '<Subject file: {}>'.format(self.file)
