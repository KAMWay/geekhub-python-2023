from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


# Create your views here.
@login_required(redirect_field_name="index", login_url="account:login")
def logout_view(request):
    logout(request)
    return redirect('index')
