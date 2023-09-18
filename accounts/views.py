from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode


from .forms import UserForm, VendorForm
from . models import User, UserProfile, Vendor
from . utils import detectUser, send_verification_email


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


def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('vendorDashboard')
    elif request.method == 'POST':
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

            # send verification email
            mail_subject = 'Please activate your account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(
                request, user, mail_subject, email_template)

            messages.success(
                request, 'Registered successfully! Please check your E-Mail to confirm.')
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


def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('custDashboard')
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

            # send verification email
            mail_subject = 'Please activate your account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(
                request, user, mail_subject, email_template)

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


def activate(request, uidb64, token):
    # activate user by setting the is_active status to true

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request, 'Congratulation! your account is activated, Login now!')
        return redirect('myAccount')
    else:
        messages.error(request, 'Invalid activition link')
        return redirect('myAccount')


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
    vendor = Vendor.objects.get(user=request.user)
    context = {
        'vendor': vendor,
    }
    return render(request, 'accounts/vendorDashboard.html', context)


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # send reset password email
            mail_subject = 'Reset your password'
            email_template = 'accounts/emails/reset_password_email.html'
            send_verification_email(
                request, user, mail_subject, email_template)

            messages.success(
                request, 'Reset link has been sent to your E-Mail address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgot_password')
    return render(request, 'accounts/forgot_password.html')


def reset_password_validate(request, uidb64, token):
    # validate the user by decoding the token and user.pk
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        # vagti user b link click mikonad uid ro migire
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        # age user none nabashe v token doros bashe
        request.session['uid'] = uid
        messages.info(request, 'Now you can reset your old password')
        return redirect('reset_password')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('myAccount')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        # 'password' hamun name(dakhele field) dakhele html has
        conifirm_password = request.POST['confirm_password']

        if password == conifirm_password:
            pk = request.session.get('uid',)
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_avtive = True
            user.save()
            messages.success(request, 'Password reset successfully!')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match')
            return redirect('reset_password')

    return render(request, 'accounts/reset_password.html')
