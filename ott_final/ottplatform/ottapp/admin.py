from django.contrib import admin

from .models import Customer, CustomerProfile, KidProfile, MovieList
from django.contrib import admin
from .models import Movie


# Register your models here.
admin.site.register(Customer)
admin.site.register(Movie)
admin.site.register(CustomerProfile)
admin.site.register(KidProfile)
admin.site.register(MovieList)


