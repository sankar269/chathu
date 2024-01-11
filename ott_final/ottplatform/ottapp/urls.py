from django.contrib import admin
from django.urls import path
from . import views
from .views import login_view, register_customer, kidprofile_details, profile_details, ProfileDetailView, \
    profile_registration_view, kid_profile_registration_view, home_view, help_view, update_profile, delete_profile, \
    update_kid_profile, delete_kid_profile, movie_detail, going_to_search, video_detail, movie_card, \
    going_to_search_kids

urlpatterns = [
    path('', home_view, name='home'),
    path('help/',help_view,name='help'),
    path('login/',login_view,name='login'),
    path('register/',register_customer,name='register'),

    path('profile/detail/<int:customer_id>/profile/<int:profile_id>/', profile_details, name='profile_details'),
    path('profile/<int:customer_id>/', profile_registration_view, name='profile_registration'),
    path('customer/<int:customer_id>/kid-profile-registration/', kid_profile_registration_view,
         name='kid_profile_registration'),
    path('profile/update/<int:customer_id>/<int:profile_id>/', update_profile, name='update_profile'),
    path('profile/delete/<int:customer_id>/<int:profile_id>/', delete_profile, name='delete_profile'),
    path('kid-profile/update/<int:customer_id>/<int:kid_profile_id>/', update_kid_profile, name='update_kid_profile'),
    path('kid-profile/delete/<int:customer_id>/<int:kid_profile_id>/', delete_kid_profile, name='delete_kid_profile'),
    path('language_movies/<str:language>/', views.language_movies, name='language_movies'),
    path('movie/<uuid:uuid>/', movie_detail, name='movie_detail'),

    path('going_to_search/', going_to_search, name='going_to_search'),
    path('video_detail/<uuid:uuid>/', video_detail, name='video_detail'),
    path('profile/detail/<int:customer_id>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/detail/<int:customer_id>/kidprofile/<int:profile_id>/', kidprofile_details, name='kidprofile_details'),
    path('movie_card/', movie_card, name='movie_card'),
    path('kidsprofile', views.kids_profile, name='kids_profile'),

    path('going_to_search_kids', going_to_search_kids, name='going_to_search_kids')

]