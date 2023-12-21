import datetime
from app import db, ma


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, serial=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Colmun(db.String(200), nullable=False)
    name = db.Colmun(db.String(60), nullable=False)
    email = db.Colmun(db.String(50), unique=True, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, username, password, name, email):
        self.username = username
        self.password = password
        self.name = name
        self.email = email


class UsersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'name', 'email', 'password', 'created_on')


user_schema = UsersSchema()
users_schema = UsersSchema(many=True)