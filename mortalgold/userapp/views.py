from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from . import forms

User = get_user_model()

@csrf_protect
def singup(request):
    if request.user.is_authenticated:
        messages.info(request, _('Looks like your already sign up'))
    if request.method == "POST":
        error = False
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.qet('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        if not username or len(username) < 4 or User.objects.filter(username=username).exists():
            error = True
            messages.error(request, _('Username is too short or already taken.'))
        if not email or len(email) < 6 or User.objects.filter(email=email).exists():
            error = True
            messages.error(request, _('Email is invalid or already taken.'))
        if not password or not password_confirm or password != password_confirm or len(password) < 7:
            error = True
            messages.error(request, _('Password must be at least 7 characters long and match.'))
        if not error:
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
            )
            user.set_password(password)
            user.save()
            messages.success(request, _('Resgistration was successful!'))
            return redirect('login')
    return render(request, 'userapp/signup.html')

def profile(request, user_id=None):
    if user_id == None:
        user = request.user
    else:
        user = get_object_or_404(get_user_model(), id=user_id)
    return render(request, 'userapp/profile.html', {'user_': user})

@login_required
@csrf_protect
def profile_update(request):
    if request.method == "POST":
        user_form = forms.UserUpdateForm(request.POST, instance=request.user)
        profile_form = forms.ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _("Profile updated."))
            return redirect('profile')
    else:
        user_form = forms.UserUpdateForm(instance=request.user)
        profile_form = forms.ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'userapp/profile_update.html', {'user_form': user_form, 'profile_form': profile_form})
