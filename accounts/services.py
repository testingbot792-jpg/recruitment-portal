from .models import User
import bcrypt

def create_user(email, password, role):
    # check duplicate
    if User.objects(email=email).first():
        raise ValueError("User already exists")

    # hash password
    hashed_pw = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    return User(
        email=email,
        password=hashed_pw,
        role=role
    ).save()


def authenticate_user(email, password):
    user = User.objects(email=email).first()

    if user and bcrypt.checkpw(
        password.encode('utf-8'),
        user.password.encode('utf-8')
    ):
        return user

    return None