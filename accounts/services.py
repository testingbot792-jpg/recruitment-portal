from .models import User
import bcrypt

def create_user(email, password, role):
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    user = User(
        email=email,
        password=hashed_pw,
        role=role
    )
    user.save()
    return user


def authenticate_user(email, password):
    user = User.objects(email=email).first()
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return user
    return None