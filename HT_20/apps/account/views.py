from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views import generic

from .forms import LoginForm


class AccountLoginView(generic.FormView):
    template_name = 'registration/login.html'
    form_class = LoginForm

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = authenticate(request, username=username, password=password)
            except Exception:
                messages.error(request, f'Username {username} does not exist')
                return redirect("account:login")

            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                messages.error(request, "Username or Password does not match...")
                return redirect("account:login")


@login_required(login_url="account:login")
def logout_view(request):
    logout(request)
    return redirect('index')
