from .. import user_datastore, manager, db
from flask.ext.script import prompt_pass
from validate_email import validate_email

def create_user(email, commit=False):
    "Create a user"
    if not validate_email(email):
        print("email is not valid")
        return
    if user_datastore.find_user(email=email):
        print("User has already been created")
        return
    password = prompt_pass("Type a password")
    user = user_datastore.create_user(email=email, password=password)
    if commit:
        db.session.commit()
    return user

def create_user_role(email, role_name):
    user = create_user(email)
    role = user_datastore.find_role(role_name)
    user_datastore.add_role_to_user(user, role)
    db.session.commit()

@manager.command
def create_operateur(email):
    create_user_role(email, 'operateur')

@manager.command
def create_admin(email):
    create_user_role(email, 'admin')

@manager.command
def create_mairie(email):
    create_user_role(email, 'mairie')