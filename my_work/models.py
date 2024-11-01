from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin,User
from django.core.validators import RegexValidator
from django.core.validators import FileExtensionValidator



class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=150,
        unique=True,null=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Username must contain only letters, numbers, and @/./+/-/_ characters.'
        )]
    )
    mobile = models.CharField(
        max_length=14,
        validators=[RegexValidator(
            regex=r'^\+91\d{10}$',
            message="Phone number must be entered in the format: '+91XXXXXXXXXX' and must be exactly 14 characters long."
        )],
        blank=True,
        null=True,unique=True
    )
    full_name = models.CharField(max_length=200,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    is_active = models.BooleanField(default=True)
    ROLL_CHOICES = [
        ('teacher', 'teacher'),
        ('student', 'student'),
        
    ]
    user_type=models.CharField(max_length=20, choices=ROLL_CHOICES, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)


    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

   
    

    def __str__(self):
        return self.username




class Profile(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    qualification = models.CharField(max_length=200,null=True,blank=True)
    mobile = models.CharField(
        max_length=14,
        validators=[RegexValidator(
            regex=r'^\+91\d{10}$',
            message="Phone number must be entered in the format: '+91XXXXXXXXXX' and must be exactly 14 characters long."
        )],
        blank=True,
        null=True,
    )
    mail = models.EmailField(null=True,blank=True)
    course = models.CharField(max_length=200,null=True,blank=True)
    subject = models.CharField(max_length=200,null=True,blank=True)
    training_sub = models.CharField(max_length=200)
    current_job = models.CharField(max_length=200,null=True,blank=True)
    adhar = models.FileField(upload_to='poster/', validators=[FileExtensionValidator(['pdf', 'jpg', 'png','jpeg'])],null=True,blank=True)


class ClassModel(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    subject = models.CharField(max_length=200,null=True,blank=True)
    classes = models.CharField(max_length=200,null=True,blank=True)
    time_slot = models.CharField(max_length=200,null=True,blank=True)
    price = models.CharField(max_length=200,null=True,blank=True)
    discout = models.CharField(max_length=200,null=True,blank=True)
    offer = models.CharField(max_length=200,null=True,blank=True)
    emi = models.CharField(max_length=200,null=True,blank=True)
    status = models.BooleanField(default=False) 