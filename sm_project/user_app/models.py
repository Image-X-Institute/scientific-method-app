from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


"""A custom user manager class for the new user class.

Methods
-------
create_user(self, email, password=None)
    Creates a new user in the database using the given email and password.
create_superuser(self, email, password)
    Creates a new admin user in the database using the given email and password.
"""
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.admin = True
        user.save(using=self._db)
        return user

"""A class that will be used as a replacement for the base user class.

Attributes
-------
username: None
    Sets the default username of the user class as none.
email: EmailField
    The email of the user. This attribute has a limit of 255 characters and must be unique.
admin: BooleanField
    Defines whether the user is an admin user or not.
objects: class
    The user manager class that the user class uses

Methods
-------
__str__(self)
    Returns the email of the user.
is_staff(self)
    Returns whether the user is considered an staff member
is_admin(self)
    Returns whether the user is considered an admin
"""
class User(AbstractBaseUser):
    username = None
    email = models.EmailField(max_length=255, unique=True)
    admin = models.BooleanField(default=False)
    objects = UserManager()

    # Sets the attribute used as the username to the email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
        
    @property
    def is_staff(self):
        return self.admin
    
    @property
    def is_admin(self):
        return self.admin