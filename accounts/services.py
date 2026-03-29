from .models import User
from core.utils import hash_password, check_password

def create_user(email, password, role):
    return User(
        email=email,
        password=hash_password(password),
        role=role
    ).save()

def authenticate_user(email, password):
    user = User.objects(email=email).first()
    if user and check_password(password, user.password):
        return user
    return None