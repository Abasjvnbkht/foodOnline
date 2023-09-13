from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import VendorForm
from . models import Vendor
from accounts.forms import UserForm
from accounts.models import User, UserProfile


def registerVendor(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        # age az karbar fili bekhaym dar post bayad in ro ham benevisim
        # request.post esme vendor ro mikhad
        # request.files licence
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(
                first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            #  bade inke user.save() shod az tarige signal user profile zakhire mishe va az tarige user
            # mishe b user profile dastrasi dash
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(
                request, 'Your account has been registered successfully! please wait for approval.')
            return redirect('registerVendor')

        else:
            print('invalid form')
            print(form.errors)
    else:
        # age method POST nabud pas hatman method GET hasesh v form ha ro b surate kham neshune karbar midim
        form = UserForm()
        v_form = VendorForm()

    context = {
        'form': form,
        'v_form': v_form,
    }
    return render(request, 'vendor/registerVendor.html', context)
