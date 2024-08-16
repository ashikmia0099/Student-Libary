from django.contrib import messages
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User





class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name', 'email', 'password1', 'password2']
        
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])  # Use password1 here
        if commit:
            user.save()
        return user
    
    
    
    
    

class User_Update_Form(forms.ModelForm):
    
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        

    def save(self, commit = True):
        user = super().save(commit=False)
        
        if commit:
            user.save()              
            
            
            
        return user
    
    
 

    
    