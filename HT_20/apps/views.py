from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


def index(request):
    return render(request, "index.html")


@login_required(redirect_field_name="index")
def logout_view(request):
    logout(request)
    return redirect('index')
