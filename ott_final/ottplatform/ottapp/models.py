from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class Customer(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)  # You should use a more secure way to store passwords
    DoB = models.DateField()
    phonenumber = models.CharField(max_length=15)
    joining_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.joining_date:
            from datetime import datetime
            today = datetime.now().date()
            self.joining_date = today

        if not self.expiry_date:
            from datetime import timedelta
            duration_months = 1  # Set the default subscription duration
            self.expiry_date = self.joining_date + timedelta(days=30 * duration_months)

        super(Customer, self).save(*args, **kwargs)

    def __str__(self):
        return self.username


MOVIE_CHOICES = (
    ('seasonal', 'Seasonal'),
    ('single', 'Single')
)
AGE_CHOICES = (
    ('ALL', 'ALL'),
    ('Kids', 'Kids')
)
GENRE_CHOICES = [
    ('action', 'Action'),
    ('comedy', 'Comedy'),
    ('drama', 'Drama'),
    ('horror', 'Horror'),
    ('romance', 'Romance'),
    ('science_fiction', 'Science Fiction'),
    ('fantasy', 'Fantasy'),
]
LANGUAGE_CHOICES = [
    ('english', 'English'),
    ('hindi', 'Hindi'),
    ('malayalam', 'Malayalam'),
    ('tamil', 'Tamil'),
    ('kannada', 'Kannada'),
    ('telugu', 'Telugu'),
    ('bengali', 'Bengali'),
]


class CustomerProfile(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='profile')

    name = models.CharField(max_length=100)
    pin = models.CharField(max_length=4)
    avatar = models.ImageField(upload_to='media/')


class KidProfile(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='kid_profiles')
    name = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='media/')



class Movie(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(choices=MOVIE_CHOICES, max_length=10)
    languages = models.CharField(choices=LANGUAGE_CHOICES, max_length=20)
    age_limit = models.CharField(choices=AGE_CHOICES, max_length=10)
    release_date = models.DateField()
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES)
    length = models.PositiveIntegerField()
    image_card = models.ImageField(upload_to='movie_images/')
    image_cover = models.ImageField(upload_to='movie_images/')
    video = models.FileField(upload_to='movie_videos/')
    movie_views = models.IntegerField(default=0)
    for_kids = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class MovieList(models.Model):
    owner_user = models.ForeignKey(
        Customer,  # Use the Register model instead of settings.AUTH_USER_MODEL
        on_delete=models.CASCADE,
    )
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
