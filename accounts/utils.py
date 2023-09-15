from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


def detectUser(user):
    if user.role == 1:
        redirectUrl = 'vendorDashboard'
        return redirectUrl
    elif user.role == 2:
        redirectUrl = 'custDashboard'
        return redirectUrl
    elif user.role == 'None' and user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl


def send_verification_email(request, user):
    """
    in function baraye ersale email hasesh
    """
    current_site = get_current_site(request)
    # in site feli ra b man mide
    mail_subject = 'Please Activate Your Accounts'
    message = render_to_string('accounts/emails/account_verification_email.html'), {
        # in body emaile
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        # user.pk ra mostagim nemishe b email ersal konim vase hamin ramz neagri mikonim v bad dakhele email.body mifresim
        'token': default_token_generator.make_token(user),
        # dar inja karbaro migire v token ijad mikone
    }
    to_email = user.email
    mail = EmailMessage(mail_subject, message, to=[to_email])
    # EmailMessage, packagiye k az an baraye ersale payame email estefade mikonim
    mail.send()
