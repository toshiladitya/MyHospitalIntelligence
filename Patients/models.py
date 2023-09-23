from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

from datetime import date
# from address.models import AddressField
import uuid
class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name,last_name,gender,username,mobile_number, password=None,confirm_password=None,):
      
        if not email:
            raise ValueError("Users must have an email address")
        

        

        user = self.model(
             email=self.normalize_email(email),
            username=username,
            mobile_number=mobile_number,
            first_name=first_name,
            last_name =last_name,
            
            gender=gender,
           
        )
        print("jijij")
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email, first_name,last_name,gender, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name =last_name,
            gender=gender
        
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# mobile_number_regex=RegexValidator(
#     regex=r"^/d{12}",message="Phone Number Must be 10 digit only"
# )
class Patient(AbstractBaseUser):
    id = models.AutoField(_("Id"),primary_key=True)
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    otp = models.CharField(max_length=6, null=True, blank=True)
    username=models.CharField(_("Username"), max_length=50,unique=True)
    first_name=models.CharField(_("first name"), max_length=50)
    last_name=models.CharField(_("last name"), max_length=50)
    image=models.ImageField(_(""), upload_to='patient_images',default=None)
    dob = models.DateField(max_length=8,null=True)

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    Gender=(
        ('Male','Male'),
        ('Female','Female'),
        ('Others','Others'),
    )
    gender=models.CharField(_("gender"), max_length=50,choices=Gender)
    mobile_number=models.CharField(_("Mobile Number"), max_length=10,unique=True)
    is_verified=models.BooleanField(default=False) 
    created_at=models.DateField(auto_now_add=True)


    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name','last_name','gender']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        if self.dob:
            today = date.today()
            age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
            return age
        else:
            return None
        
    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return None


    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    

    
