# accounts/views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin

from .models import CustomUser

# Custom Signup View
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        image = request.FILES.get('image')
        job = request.POST.get('job')
        about_you = request.POST.get('about_you')

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            image=image,
            job=job,
            about_you=about_you,
            first_name=request.POST['firstname'],  # Automatically sets first name
            last_name=request.POST['lastname']  # Automatically sets last name
        )

        login(request, user)
        return redirect('dashboard')

    return render(request, 'registration/signup.html')

def custom_login_view(request):
    if request.method == 'POST':
        # Retrieve data from the form manually
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log in the user
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect('dashboard')
        else:
            # If authentication fails, add an error message
            messages.error(request, "Invalid username or password.")

    # Render the signin template
    return render(request, 'registration/signin.html')


# Custom Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# Profile View
@login_required
def profile_view(request):
    user_data = CustomUser.objects.get(username=request.user.username)
    return render(request, 'registration/profile.html', {'user_data': user_data})

# Change Password View
@login_required
def change_password_view(request):
    if request.method == 'POST':
        user = request.user
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # To keep the user logged in
            messages.success(request, 'Password changed successfully.')
        else:
            messages.error(request, 'Incorrect old password.')

    return render(request, 'registration/change_password.html')

# Lock Screen View
@login_required
def lock_screen_view(request):
    if request.method == 'POST':
        password = request.POST['password']
        user = authenticate(username=request.user.username, password=password)

        if user:
            # Unlock the screen and redirect to the profile
            request.session['lock_screen'] = False
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Invalid password. Please try again.')

    # Set the lock screen session variable
    request.session['lock_screen'] = True

    return render(request, 'registration/lock_screen.html')
