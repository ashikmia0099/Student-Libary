from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
  
   path('', views.Home_page, name = 'Home_page'),
   path('Add-book/', views.Add_books, name = 'Add_book'),
   path('Author-wise-book/', views.Author_wise_book_show, name = 'Author_wise_book_show'),
   path('Add-book-forms/', views.Add_book_New_forms, name = 'Add_bookforms'),
   path('Filter-book/<int:book_id>/', views.Home_page, name='bookid'),
   path('delete/<int:id>/', views.Delete_book, name='Delete_book'),
   path('Edit-book/<int:id>/', views.Edit_book_data, name='Edit_book'),
   
   # # path('edit/<int:id>',views.EditPostView.as_view(),name='Edit_book'),
   
   path('favorite-book/', views.Favorite_book_views, name='Favorite_book_views'),
   path('favorite-book/<int:book_id>/', views.Favorite_book_views, name='add_favorite'),
   path('add-to-favorites/<int:book_id>/', views.add_to_favorites, name='add_to_favorites'),
   path('Remove/<int:id>/', views.Remove_book, name='Remove_book'),
   
]
