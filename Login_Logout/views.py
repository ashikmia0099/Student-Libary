from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from .forms import RegisterForm,User_Update_Form
from .models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy,reverse

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings





def Register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            instance = form.save()
                        
            messages.success(request, 'Account registered successfully')
            return redirect('Registerpage')
        else:
            messages.error(request, 'Registration failed. Please correct the errors.')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})






# simple user Login



def simple_user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(email=email, password=password)
            
            if user is not None:
                
                login(request, user)
                messages.success(request, f'Welcome {user.first_name} {user.last_name}!')
                return redirect('Favorite_book_views')
                
            else:
                messages.error(request, 'Login information is incorrect.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AuthenticationForm()
        
    return render(request, 'user_login.html', {'form': form})





def Custom_admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(email=email, password=password)
            
            if user is not None:
                if user.is_author:
                    login(request, user)
                    messages.success(request, f'Welcome {user.first_name} {user.last_name}!')
                    return redirect('Add_book')
                else:
                    messages.error(request, 'You do not have the required permissions to log in.')
            else:
                messages.error(request, 'Login information is incorrect.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AuthenticationForm()
        
    return render(request, 'login.html', {'form': form})




# user logout

@login_required
def LogoutView(request):
    user = request.user
    logout(request)
    messages.success(request, f'{user.first_name} {user.last_name} is successfully logged out.')
    return redirect('Custom_admin_login')



# edit user data
 

@login_required
def Edit_user_data(request):
    
    if request.method == 'POST':
        form = User_Update_Form(request.POST, instance=request.user)
        
        if form.is_valid():
            form.save()
            return redirect('Edit_user_data')
    else:
        form = User_Update_Form(instance=request.user)
    
    
    return render(request, 'edit_user_data.html', {'form': form})

 
 


