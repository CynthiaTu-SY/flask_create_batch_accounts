from . import db
from sqlalchemy.sql import func

accountmaps = db.Table('accountmaps',
    db.Column('group_id', db.String, db.ForeignKey('group.id')),
    db.Column('account_id', db.String, db.ForeignKey('account.id'))
)
class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    groupname = db.Column(db.String(10000), unique=True)
    users = db.relationship('Account', secondary=accountmaps, lazy='subquery',
    backref=db.backref('groups', lazy=True))   

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10000), unique=True)
    password = db.Column(db.String)