from django.contrib.auth.models import User
from django.forms.widgets import DateInput
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from .forms import CreateUserForm


def registerPage(request):
    if not request.user.is_authenticated:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Account created for ' +
                                 form.cleaned_data.get('username'))
                return redirect('/accounts/login')

        context = {'form': form}
        return render(request, 'accounts/register.html', context)
    else:
        return redirect('/movies/movies')


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('/movies/movies')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/movies/')
            else:
                messages.info(request, 'Username OR Password is incorrect!')
        context = {}
        return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('/accounts/login')
