from django import forms
from .models import AddNewBook



class Add_book_forms(forms.ModelForm):
    class Meta:
        model = AddNewBook
        exclude = ['user']



        
        



