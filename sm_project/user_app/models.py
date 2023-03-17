from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.shortcuts import get_object_or_404


class UserManager(BaseUserManager):
    """A custom user manager class for the new user class.

    Methods
    -------
    create_user(self, email, name, password=None)
        Creates a new user in the database using the given email, name and password.
    create_superuser(self, email, name, password)
        Creates a new admin user in the database using the given email, name and password.
    """
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    """A class that will be used as a replacement for the base user class.

    Attributes
    -------
    username: None
        Sets the default username of the user class as none.
    email: EmailField
        The email of the user. This attribute has a limit of 255 characters and must be unique.
    name: CharField
        The name of the user. This attribute has a limit of 70 characters.
    admin: BooleanField
        Defines whether the user is an admin user or not.
    objects: class
        The user manager class that the user class uses

    Methods
    -------
    __str__(self)
        Returns the email of the user.
    is_staff(self)
        Returns whether the user is considered an staff member.
    is_admin(self)
        Returns whether the user is considered an admin.
    has_temp_checklist(self)
        Returns whether the checklist that is used to store temporary checklist items as part of checklist creation exists.
        See add_checklist(request) and add_temp_item(request) in cl_app/views.py for more.
    get_temp_checklist(self)
        Returns the checklist that is used to store temporary checklist items as part of checklist creation.
        See add_checklist(request) and add_temp_item(request) in cl_app/views.py for more.
    """
    username = None
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=70)
    admin = models.BooleanField(default=False)
    objects = UserManager()

    # Sets the attribute used as the username to the email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f"{self.name} - {self.email}"

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
    
    def has_temp_checklist(self):
        return self.creator.filter(checklist_title=(f"Temp{self.id}")).exists()
    
    def get_temp_checklist(self):
        return get_object_or_404(self.creator, checklist_title=(f"Temp{self.id}"))
