from django.db import models
from Login_Logout.models import User
from django.utils import timezone

from django.contrib.auth import get_user_model


# Add_new_book 
 
User = get_user_model()

class AddNewBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Book_Title = models.CharField(max_length=150, blank=True, null=True)
    BookImage = models.ImageField(upload_to='media/HomePage', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Add A New Book'
        verbose_name_plural = 'Add A New Book'
         
    def __str__(self):
        return self.Book_Title if self.Book_Title else "No Book Title"

    

class FabaritBook(models.Model):
    
    
    user = models.ForeignKey(User, related_name='favorite_books', on_delete=models.CASCADE)
    book = models.ForeignKey(AddNewBook, related_name='favorited_by', on_delete= models.CASCADE)
    created_on = models.DateTimeField(auto_now_add= True)
    
    
    class Meta:
        unique_together = ('user', 'book')
        verbose_name = ' Fabarit Book'
        verbose_name_plural = ' Fabarit Book '
         
         
         
    def save(self, *args, **kwargs):
        if FabaritBook.objects.filter(user = self.user).count() >=20:
            raise ValueError('Cannot have more then 20 favorite book')
        
        super().save(*args, **kwargs)
        
        
    
    