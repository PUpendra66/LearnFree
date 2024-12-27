from django.shortcuts import render,redirect,get_list_or_404,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import models
from.models import Course,Enrollment,UserProfile
from django.http import HttpResponse
from .forms import UserUpdateForm, ProfileUpdateForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import UserProfile, Enrollment
# Create your views here.


def index(request):
    courses = Course.objects.all()
    return render(request, 'index.html', {'courses': courses})

@login_required(login_url='/login/')
def course_list(request):
    courses = Course.objects.all()
    enrolled_courses = Enrollment.objects.filter(user=request.user).values_list('course_id', flat=True)
    return render(request, 'courses.html', {'courses': courses, 'enrolled_courses': enrolled_courses})
@login_required(login_url='/login/')
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'course_detail.html', {'course': course})



def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        image = request.FILES.get('image')  # Use request.FILES for the uploaded image

        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already exists")

        # Create the User
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Update the UserProfile if it doesn't already exist
        profile, created = UserProfile.objects.get_or_create(user=user)
        if image:
            profile.avatar = image  # Set the avatar if provided
            profile.save()

        return redirect('login')

    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse("Invalid credentials")
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('index')


@login_required(login_url='/login/')
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)
   
    
    return redirect('courses')


@login_required(login_url='/login/')
def enrolled_courses(request):
    enrollments = Enrollment.objects.filter(user=request.user).select_related('course')
    return render(request, 'enrolled_courses.html', {'enrollments': enrollments})


def about(request):
    return render(request, 'about.html')
@login_required(login_url='/login/')
def profile(request):
    user = request.user

    # Ensure the UserProfile exists
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileUpdateForm(instance=profile)

    # Fetch the user's enrolled courses
    enrollments = Enrollment.objects.filter(user=user)

    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,

        'profile': profile,
        'enrollments': enrollments,
    })


@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')  # Redirect to the profile page after updating
    else:
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
    return render(request, 'register.html', {'profile_form': profile_form})

from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

class CustomPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('profile')  # Redirect to the profile page after success




