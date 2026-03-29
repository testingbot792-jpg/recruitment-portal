from mongoengine import Document, StringField, EmailField

class User(Document):
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    role = StringField(choices=["admin", "candidate"])