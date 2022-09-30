from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager


class CustomUserManager(BaseUserManager):
    def _create_user(self,email,password,first_name,last_name,mobile,**extra_fields):
        if not email:
            raise ValueError('Email Must Be Provided')
        if not password:
            raise ValueError('Password Must Be Provided')
        user=self.model(
        email=self.normalize_email(email),
        first_name=first_name,
        last_name=last_name,
        mobile=mobile,
        **extra_fields

        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_user(self,email, password,first_name,last_name,mobile, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user( email, password,first_name,last_name,mobile, **extra_fields)

    def create_superuser(self,email, password,first_name,last_name,mobile, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")


        return self._create_user( email, password,first_name,last_name,mobile ,**extra_fields)


# Create your models here.
class User(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(db_index=True,unique=True,max_length=254)
    first_name=models.CharField(max_length=250)
    last_name=models.CharField(max_length=250)
    mobile=models.BigIntegerField()
    is_staff=models.BooleanField(default=True)
    is_active=models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)


    objects=CustomUserManager()
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name','last_name','mobile']



    class Meta:
        verbose_name='User'
        verbose_name_plural='Users'

class Books(models.Model):
    name=models.CharField(max_length=200)
    author_name=models.CharField(max_length=200)
