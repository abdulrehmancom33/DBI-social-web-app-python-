from django.db import models
from django.conf import settings
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)

# Your models here.
class UserManager(BaseUserManager):
    
    #creates user with given email and password
    def create_user(self, email, resetkey = None, full_name = None, city = None, country = None, password=None):
            
        if email is None:
            raise ValueError('Email is required.')
            # resetkey = "default@dbisystems.com"
            print("NO OK")
        elif resetkey is None: 
            print("Alt No Ok")
            raise ValueError('Reset Key is required.')
        else:
            print("All OK")
            
        user = self.model(
            email=self.normalize_email(email),
            resetkey = resetkey,
            full_name = full_name,
            city = city,
            country = country,
            password = password,
        )
        
        user.save(using=self._db)
    
        return user

    #creates staffuser with given email and password
    def create_staffuser(self, email, password):
        user = self.create_user(
            email,
            resetkey = "staff@dbisystems.com",
            password=password,
            full_name="staff",
            city = None,
            country = None
        )
        user.staff = True
        user.save(using=self._db)
        return user

    #creates superuser with given email and password
    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            resetkey = "defaultadmin@dbisystems.com",
            password=password,
            full_name="admin",
            city = None,
            country = None
        )
        user.set_password(password)
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        
        return user
    
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name    =   'email address',
        max_length      =   255,
        unique          =   True
    )

    resetkey = models.CharField(
        verbose_name    =   'Reset Key',
        max_length      =   255,
        unique          =   False
    )

    active  =   models.BooleanField(default = True)  #false when user deletes his account
    staff   =   models.BooleanField(default = False) #an admin user; non super-user
    admin   =   models.BooleanField(default = False) #a superuser
    
    # extended
    full_name = models.CharField(
        max_length = 100,
        blank = True,
        null = False
    )

    city = models.CharField(
        max_length = 100,
        blank = True,
        null = True
    )
    
    country = models.CharField(
        max_length = 100,
        blank = True,
        null = True
    )
    
    #password field is not requited as it's built in

    USERNAME_FIELD = 'email' #makes email the default username fielf
    REQUIRED_FIELDS = [] #email & password are required by default.

    objects = UserManager() #setting up user manager

    def _int_(self):
        return str(self.id)

    def get_full_name(self):
        return self.full_name
    

    def get_short_name(self):
        return self.full_name

    def __str__(self):
        if self.email:
            return self.email
        else:
            return self.contact_details
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active

def upload_location(instance,filename):
        return "%s/%s" %('ImageRepository',filename)

class Image(models.Model):

    #media_url = models.TextField()
    fileToUpload = models.ImageField(upload_to=upload_location)
   # This field should be string or text...
    STATUS_CHOICES = (
        ("JPEG", "JPEG"),
        ("PNG", "PNG"),
        ("JPG", "JPG")
    )
    media_type =  models.CharField(choices=STATUS_CHOICES,max_length=10, default="JPEG")
    #uploaded_on = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return str(self.fileToUpload)
        return str(self.id)
#return str doesn't mean that the field becomes string... it just return its value in string...
class Breed(models.Model):
    breed_name = models.CharField(max_length = 255, blank=True)
    breed_life_expectancy = models.TextField(blank=True)
    breed_avg_weight = models.TextField(blank=True)
    breed_group = models.CharField(max_length = 255,blank=True)
    breed_fav_food = models.TextField(blank=True)  # breed favourite food
    breed_com_food = models.TextField(blank=True) # breed common food
    breed_cautions = models.TextField(blank=True)
    breed_height = models.TextField(blank=True)
    breed_tips = models.TextField(blank=True)
    def __str__(self):
        return '%s , %s' % (self.breed_name, self.breed_group)
        

class Dog(models.Model):
    dog_acc = models.CharField(max_length = 50)
    dog_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='dogusers')
    dog_image = models.TextField()
    dog_breed = models.ForeignKey(Breed, on_delete=models.CASCADE, related_name='dogbreeds')
    Remarks = models.TextField()
    isDog = models.BooleanField()
    def __int__(self):
        return str(self.id)

class Feed_Item(models.Model):
    feed_item_desc = models.TextField()
    feed_item_dog = models.ForeignKey(Dog, on_delete=models.CASCADE,related_name='feeditems')
    Feed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    isSaveFeed = models.BooleanField()
    def __int__(self):
        
        return str(self.id)
        
class Liked_Dog(models.Model):
    liked_user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_feed_item = models.ForeignKey(Feed_Item, on_delete=models.CASCADE)
    # liked_feed_time = models.TextField(default = timezone.now)

    # class Meta:
    #     unique_together = ("liked_user" , "liked_feed_item")
