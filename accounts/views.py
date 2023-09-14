from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied

from .forms import UserForm
from . models import User
from . utils import detectUser


# Restrict the vendor from accesing the customer page
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


# Restrict the customer from accesing the vendor page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied


def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('dashboard')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():

            #  create the user uding the form
            # password = form.cleaned_data['password']
            # # dar inja miikhaym passworde dakhele admin pannel ro b hash tabdil konim k bade commit
            # # az set_password esttefade mikonim
            # user = form.save(commit=False)
            # user.set_password(password)
            # user.role = User.CUSTOMER
            # # user.save()
            #  fields = ['first_name', 'last_name',
            #       'username', 'email', 'password']

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(
                first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(
                request, 'Your account has been registered successfully')
            return redirect('registerUser')
        else:
            print('invalid form')
            print(form.errors)
    else:
        form = UserForm()
    context = {
        'form': form
    }

    return render(request, 'accounts/registerUser.html', context)


def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('myAccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('myAccount')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    messages.info(request, 'you are logged out.')
    return redirect('login')


@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request, 'accounts/custDashboard.html')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request, 'accounts/vendorDashboard.html')
