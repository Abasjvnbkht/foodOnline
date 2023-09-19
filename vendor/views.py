from django.shortcuts import render, get_object_or_404
from accounts.forms import UserProfileForm, VendorForm
from accounts.models import UserProfile, Vendor
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vprofile(request):

    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    profile_form = UserProfileForm(instance=profile)
    vendor_form = VendorForm(instance=vendor)
    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor,
    }

    return render(request, 'vendor/vprofile.html', context)
