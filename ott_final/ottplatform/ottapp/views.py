from urllib import request
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PINVerificationForm, CustomerRegistrationForm, CustomerProfileForm, KidProfileForm, SearchForm
from django.contrib.auth.hashers import check_password, make_password
# ottapp/views.py
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from .models import  Customer, CustomerProfile, KidProfile, Movie
from .forms import LoginForm
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string

import asyncio
from django.views import View
from django.utils.decorators import method_decorator

from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.hashers import check_password

def login_view(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                customer = Customer.objects.get(username=username)
                if customer.password == password:
                    # Get the customer ID and redirect to the profile detail page
                    customer_id = customer.id
                    return redirect('profile_detail', customer_id=customer_id)
                else:
                    form.add_error(None, 'Invalid credentials')
            except Customer.DoesNotExist:
                form.add_error(None, 'User not found')

    return render(request, 'useraccount/login.html', {'form': form})

async def send_welcome_email_async(email, firstname):
    try:
        subject = 'Welcome to Our App'
        message = render_to_string('useraccount/welcome_email.txt', {'firstname': firstname})
        from_email = 'D-flix <ajithhunting900@gmail.com>'  # Replace with your email
        recipient_list = [email]

        await asyncio.sleep(0)  # Allow other tasks to run

        send_mail(subject, message, from_email, recipient_list)

    except Exception as e:
        # Log the error details
        print(f"Error sending welcome email: {e}")

def help_view(request):
    return render(request, 'help.html')
def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            asyncio.run(send_welcome_email_async(user.email, user.firstname))
            return redirect('home')  # Redirect to a success page
    else:
        form = CustomerRegistrationForm()

    return render(request, 'useraccount/signup.html', {'form': form})

def home_view(request):
    return render(request, 'home.html')
class ProfileDetailView(View):
    template_name = 'profile_detail.html'

    def get(self, request, customer_id):
        customer = Customer.objects.get(id=customer_id)
        profile = customer.profile.all()  # Assuming there's only one profile per customer
        kid_profiles = customer.kid_profiles.all()
        return render(request, self.template_name,
                      {'customer': customer, 'profile': profile, 'kid_profiles': kid_profiles})

def profile_registration_view(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    template_name = 'profile_registration.html'

    # Check the existing number of profiles for the customer
    total_profiles = CustomerProfile.objects.filter(customer=customer).count()

    if total_profiles >= 2:
        # Return an error message or handle the limit reached scenario
        return render(request,'error.html')

    if request.method == 'POST':
        profile_form = CustomerProfileForm(request.POST, request.FILES)

        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.customer = customer
            profile.save()

            return redirect('profile_detail', customer_id=customer.id)

    else:
        profile_form = CustomerProfileForm()

    return render(request, template_name, {'customer': customer, 'profile_form': profile_form})


def kid_profile_registration_view(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    template_name = 'kid_registration.html'

    # Check the existing number of profiles for the customer
    total_profiles = KidProfile.objects.filter(customer=customer).count()

    if total_profiles >= 2:
        # Return a JSON response with the error message
        return render(request,'error.html')

    if request.method == 'POST':
        profile_form = KidProfileForm(request.POST, request.FILES)

        if profile_form.is_valid():
            kid_profile = profile_form.save(commit=False)
            kid_profile.customer = customer
            kid_profile.save()
            return redirect('profile_detail', customer_id=customer.id)

            # Optionally, return a success message or an empty JSON response


    else:
        profile_form = KidProfileForm()

    return render(request, template_name, {'customer': customer, 'profile_form': profile_form})



def profile_details(request, customer_id, profile_id):
    customer = get_object_or_404(Customer, id=customer_id)
    profile = get_object_or_404(CustomerProfile, id=profile_id, customer=customer)

    if request.method == 'POST':
        pin_form = PINVerificationForm(request.POST)

        if pin_form.is_valid():
            entered_pin = pin_form.cleaned_data['pin']

            if entered_pin == profile.pin:
                # PIN is correct, redirect to the movie_list function
                return redirect('movie_card')
            else:
                # PIN is incorrect, show an error message
                pin_form.add_error('pin', 'Incorrect PIN. Please try again.')

    else:
        # If the request is not a POST, initialize an empty form
        pin_form = PINVerificationForm()

    return render(request, 'pin_verification.html', {'customer': customer, 'profile': profile, 'pin_form': pin_form})

def kidprofile_details(request, customer_id, profile_id):
    customer = get_object_or_404(Customer, id=customer_id)
    profile = get_object_or_404(KidProfile, id=profile_id, customer=customer)

    return render(request, 'kids_profile.html', {'customer': customer, 'profile': profile})



#more changes

# views.py


def update_profile(request, customer_id, profile_id):
    customer = get_object_or_404(Customer, id=customer_id)
    profile = get_object_or_404(CustomerProfile, id=profile_id)

    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_detail', customer_id=customer.id)
    else:
        form = CustomerProfileForm(instance=profile)

    return render(request, 'update_profile.html', {'customer': customer, 'profile': profile, 'form': form})


# views.py


def delete_profile(request, customer_id, profile_id):
    customer = get_object_or_404(Customer, id=customer_id)
    profile = get_object_or_404(CustomerProfile, id=profile_id)

    if request.method == 'POST':
        profile.delete()
        return redirect('profile_detail', customer_id=customer.id)

    return render(request, 'delete_profile.html', {'customer': customer, 'profile': profile})

# views.py
from django.shortcuts import get_object_or_404, redirect
from .models import KidProfile

def delete_kid_profile(request, customer_id, kid_profile_id):
    customer = get_object_or_404(Customer, id=customer_id)
    kid_profile = get_object_or_404(KidProfile, id=kid_profile_id)

    if request.method == 'POST':
        kid_profile.delete()
        return redirect('profile_detail', customer_id=customer.id)

    return render(request, 'delete_kid_profile.html', {'customer': customer, 'kid_profile': kid_profile})



def update_kid_profile(request, customer_id, kid_profile_id):
    customer = get_object_or_404(Customer, id=customer_id)
    kid_profile = get_object_or_404(KidProfile, id=kid_profile_id)

    if request.method == 'POST':
        form = KidProfileForm(request.POST, request.FILES, instance=kid_profile)
        if form.is_valid():
            form.save()
            return redirect('profile_detail', customer_id=customer.id)
    else:
        form = KidProfileForm(instance=kid_profile)

    return render(request, 'update_kid_profile.html', {'customer': customer, 'kid_profile': kid_profile, 'form': form})

def movie_card(request):
    # Get movies added in the last 3 days
    recent_movies = Movie.objects.filter(release_date__gte=(timezone.now() - timedelta(days=3))).order_by(
        '-release_date')

    # Get all movies for the general display
    all_movies = Movie.objects.filter(type='single').order_by('-release_date')

    # Get all series for the series display
    all_series = Movie.objects.filter(type='seasonal')

    return render(request, 'movie_card.html',
                  {'recent_movies': recent_movies, 'all_movies': all_movies, 'all_series': all_series})


def movie_detail(request, uuid):
    movie = get_object_or_404(Movie, uuid=uuid)
    related_movies = Movie.objects.filter(languages=movie.languages).order_by('-release_date')[:5]
    return render(request, 'movie_detail.html', {'movie': movie, 'related_movies': related_movies})


def language_movies(request, language):
    movies = Movie.objects.filter(languages=language)
    return render(request, 'language_movies.html', {'movies': movies, 'language': language})


def going_to_search(request):
    # Handle search form submission
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['search_query']
            # Add your search logic here if needed
            # For example, you can filter movies based on the search query
            search_results = Movie.objects.filter(title__icontains=query)
            # Add search results to the context
            context = {'search_results': search_results, 'form': form}
            return render(request, 'search_page.html', context)

    # If it's not a search submission or the form is not valid, display the page with placeholder data
    random_movies = Movie.objects.annotate(num_views=Count('movie_views')).order_by('?')[:6]
    recent_movies = Movie.objects.order_by('-release_date')[:6]
    all_movies = Movie.objects.all()[:10]
    all_series = Movie.objects.filter(type='series')[:6]
    form = SearchForm()

    context = {
        'recent_movies': recent_movies,
        'all_movies': all_movies,
        'all_series': all_series,
        'random_movies': random_movies,
        'form': form,
        # Add other data to the context as needed
    }

    return render(request, 'search_page.html', context)


def movie_detail(request, uuid):
    movie = get_object_or_404(Movie, uuid=uuid)
    return render(request, 'movie_detail.html', {'movie': movie})


# def external_video_player(request, uuid):
#     # Retrieve the Movie object based on the UUID
#     movie = get_object_or_404(Movie, uuid=uuid)
#
#     # Pass the video URL to the template
#     context = {'video_url': movie.video.url}
#     return render(request, 'video_detail.html', context)
from django.shortcuts import render, get_object_or_404
from .models import Movie


def video_detail(request, uuid):
    movie = get_object_or_404(Movie, uuid=uuid)
    return render(request, 'video_detail.html', {'movie': movie})

def kids_profile(request):
    # Get movies added in the last 3 days marked for kids
    recent_kids_movies = Movie.objects.filter(for_kids=True, release_date__gte=(timezone.now() - timedelta(days=3))).order_by(
        '-release_date')

    # Get all movies marked for kids
    all_movies_for_kids = Movie.objects.filter(type='single', for_kids=True).order_by('-release_date')

    # Get all series marked for kids
    all_series_for_kids = Movie.objects.filter(type='seasonal', for_kids=True).order_by('-release_date')

    kids_movies = Movie.objects.filter(for_kids=True)
    # ... other context data for kids_profile view
    fantasy_movies_for_kids = Movie.objects.filter(for_kids=True, genre='fantasy').order_by('-release_date')
    action_movies_for_kids = Movie.objects.filter(for_kids=True, genre='action').order_by('-release_date')
    comedy_movies_for_kids = Movie.objects.filter(for_kids=True, genre='comedy').order_by('-release_date')
    drama_movies_for_kids = Movie.objects.filter(for_kids=True, genre='drama').order_by('-release_date')
    sci_fi_movies_for_kids = Movie.objects.filter(for_kids=True, genre='science_fiction').order_by('-release_date')
    fantasy_movies_for_kids = Movie.objects.filter(for_kids=True, genre='fantasy').order_by('-release_date')
    return render(request, 'kids_profile.html', {
        'kids_movies': kids_movies,
        'recent_kids_movies': recent_kids_movies,
        'all_movies': all_movies_for_kids,
        'all_series': all_series_for_kids,
        'fantasy_movies_for_kids': fantasy_movies_for_kids,
        'action_movies_for_kids': action_movies_for_kids,
        'comedy_movies_for_kids': comedy_movies_for_kids,
        'drama_movies_for_kids': drama_movies_for_kids,
        'sci_fi_movies_for_kids': sci_fi_movies_for_kids,
    })


def going_to_search_kids(request,profile_type='kids'):
    # Handle search form submission
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['search_query']

            # Use a single filter condition based on the profile type
            if profile_type == 'kids':
                search_results = Movie.objects.filter(for_kids=True, title__icontains=query)
            else:
                search_results = Movie.objects.filter(title__icontains=query, for_kids=False)

            # Add search results to the context
            context = {'search_results': search_results, 'form': form, 'profile_type': profile_type}
            return render(request, 'search_page_kids.html', context)

    # If it's not a search submission or the form is not valid, display the page with placeholder data
    random_movies = Movie.objects.filter(for_kids=True)

    recent_movies = Movie.objects.order_by('-release_date')[:6]
    all_movies = Movie.objects.all()[:10]
    all_series = Movie.objects.filter(type='series')[:6]
    form = SearchForm()

    context = {
        'recent_movies': recent_movies,
        'all_movies': all_movies,
        'all_series': all_series,
        'random_movies': random_movies,
        'form': form,
        'profile_type':profile_type

        # Add other data to the context as needed
    }

    return render(request, 'search_page_kids.html', context)