from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db= SQLAlchemy()

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50),unique= True,nullable=False)
    password = db.Column(db.String(50),unique=True,nullable=False)
    role = db.Column(db.String(50)) #'admin','employer','Applicant'
    created_at = db.Column(db.DateTime,default=datetime.utcnow)

class Job(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(100))
    company = db.Column(db.String(150))
    user_id = db.Column(db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id'))
    job_id = db.Column(db.ForeignKey('job.id'))
    status =  db.Column(db.String(100), default='Applied')



