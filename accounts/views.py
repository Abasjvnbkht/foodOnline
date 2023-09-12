from django.shortcuts import render, redirect
from .forms import UserForm
from . models import User
from django.contrib import messages


def registerUser(request):
    if request.method == 'POST':
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