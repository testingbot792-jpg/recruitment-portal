from mongoengine import Document, StringField
from mongoengine import Document
from mongoengine.fields import StringField, FileField
class User(Document):
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    role = StringField(required=True)
    resume = FileField()
    name = StringField()
    phone = StringField()
    address = StringField()