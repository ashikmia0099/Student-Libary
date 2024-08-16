from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from Login_Logout.models import User
from .models import FabaritBook,AddNewBook
from django.contrib import messages
from .forms import  Add_book_forms
from django.utils.decorators import method_decorator
from django.views.generic import CreateView,UpdateView,DeleteView,DetailView
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import HttpResponse
from django.db.models import Count
from django.core.paginator import Paginator



from django.db.models import Q, Value
from django.db.models.functions import Concat

# right seacrh finction



def Home_page(request, book_id=None):
    
    if book_id:
        id_wise_books = AddNewBook.objects.filter(user__id=book_id)
    else:
        id_wise_books = AddNewBook.objects.all()
    
    # Fetch authors
    authors = User.objects.filter(is_author=True)
 
    author_paginator = Paginator(authors, 12)
    author_page_number = request.GET.get('page')
    author_page_obj = author_paginator.get_page(author_page_number)
    
    # Search functionality
    q = request.GET.get('question', '')

    if q:
        # Concatenate first_name and last_name for the search
        id_wise_books = id_wise_books.annotate(
            full_name=Concat('user__first_name', Value(' '), 'user__last_name')
        ).filter(
            Q(Book_Title__icontains=q) |  
            Q(full_name__icontains=q)    
        )
        
    paginator = Paginator(id_wise_books, 15)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'home.html', {
        'author_page_obj': author_page_obj,
        'books': page_obj,  
        'query': q,
        'page_obj': page_obj  
    })

# add book

@login_required
def  Add_books(request):
    
    
    return render(request, 'Add_book.html')


@login_required
def Add_book_New_forms(request):
    if request.method == 'POST':
        Book_Title = request.POST.get('Book_Title')
        
        BookImage = request.FILES.get('BookImage')
        
        if not Book_Title:
            messages.error(request, 'Please fill in all required fields.')
            return redirect('Add_book')
        
        try:
            AddNewBook.objects.create( 
                user=request.user,
                Book_Title=Book_Title,
                BookImage=BookImage,
            )
            messages.success(request, 'Book added successfully!')
            return redirect('Add_book')
        
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('Add_book')
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('Add_book')
    
    
    
    

@login_required
def Author_wise_book_show(request):
    books = AddNewBook.objects.filter(user=request.user)
    return render(request, 'your_all_book.html', {'books': books})




@login_required
def Delete_book(request, id):

    book = AddNewBook.objects.get(pk=id)
    book.delete()
    
    return redirect('Author_wise_book_show')


#  edit book data



def Edit_book_data(request, id):
    book = AddNewBook.objects.get(pk=id)
    book_model = Add_book_forms()
    
    if request.method == 'POST':
        
        book_model = Add_book_forms(request.POST,request.FILES, instance=book)
        if book_model.is_valid():
            book_model.instance.user = request.user
            book_model.save()
            return redirect('Home_page')  # Assuming you have a redirect URL for successful edit
    else:
        book_model = Add_book_forms(instance=book)
    
    return render(request, 'Edit_book.html',{'book':book_model})





@login_required
def Favorite_book_views(request, book_id=None):
    user = request.user

    if book_id:
        book = get_object_or_404(AddNewBook, id=book_id)

        
        if FabaritBook.objects.filter(user=user, book=book).exists():
            
            FabaritBook.objects.filter(user=user, book=book).delete()
        else:
            
            if FabaritBook.objects.filter(user=user).count() >= 20:
                messages.error(request, "Cannot have more than 20 favorite books.")
                return redirect('Favorite_book_views')
            FabaritBook.objects.create(user=user, book=book)

    
    recommended_books = get_recommended_books(user)
    
    
   

    # Render a template to show the favorite book and recommendations
    return render(request, 'fabarite_book_list.html', {
        'favorite_books': FabaritBook.objects.filter(user=user),
        'recommended_books': recommended_books,
        
    })



def get_recommended_books(user):
    favorite_books = FabaritBook.objects.filter(user=user).values_list('book', flat=True)

    if not favorite_books:
        return []

    recommended_books = AddNewBook.objects.exclude(id__in=favorite_books).order_by('-created_on')[:5]


    return recommended_books




@login_required
def add_to_favorites(request, book_id):
    book = get_object_or_404(AddNewBook, id=book_id)
    user = request.user

    # Check if the book is already a favorite
    if FabaritBook.objects.filter(user=user, book=book).exists():
        messages.info(request, 'This book is already in your favorites.')
    else:
        # Check if the user has reached the maximum number of favorite books
        if FabaritBook.objects.filter(user=user).count() >= 20:
            messages.error(request, 'You cannot add more than 20 favorite books.')
        else:
            FabaritBook.objects.create(user=user, book=book)
            messages.success(request, 'Book added to your favorites.')

    return redirect('Home_page')




# remove book


@login_required
def Remove_book(request, id):

    book = FabaritBook.objects.get(pk=id)
    book.delete()
    
    return redirect('Favorite_book_views')




