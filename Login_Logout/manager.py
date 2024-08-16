from django.contrib.auth.base_user import BaseUserManager

class CustomManager(BaseUserManager):
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_author', True)
        
        if not password:
            raise ValueError('Superuser must have a password')

        return self.create_user(email, password, **extra_fields)

    def staff_count(self):
        return self.filter(is_staff=True).count()