from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Login(AbstractUser):
    is_reader = models.BooleanField(default=False)
    is_author = models.BooleanField(default=False)


class reader(models.Model):
    user_reader = models.ForeignKey(Login, on_delete=models.CASCADE, related_name='reader')
    reader_name = models.CharField(max_length=50)
    reader_phone_no = models.CharField(max_length=12)
    reader_email = models.EmailField(default='default_email@example.com')
    reader_address = models.CharField(max_length=100)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    

    def __str__(self):
        return self.reader_name


class author(models.Model):
    user_author = models.ForeignKey(Login, on_delete=models.CASCADE, related_name='author')
    author_name = models.CharField(max_length=100)
    author_phone_no = models.CharField(max_length=12)
    author_email = models.CharField(max_length=100)
    author_address = models.CharField(max_length=100)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

    def __str__(self):
        return self.author_name


class book(models.Model):
    book_name = models.CharField(max_length=100)
    book_author_name = models.ForeignKey(author, on_delete=models.CASCADE, related_name='books')

    book_type = [
        ('education', 'Education'),
        ('entertainment', 'Entertainment'),
        ('comics', 'Comics'),
        ('biography', 'Biography'),
        ('history', 'History'),
        ('novel', 'Novel'),
        ('fantasy', 'Fantasy'),
        ('thriller', 'Thriller'),
        ('romance', 'Romance'),
        ('scifi', 'Sci-Fi')
    ]
    category = models.CharField(max_length=50, choices=book_type)

    book_cover = models.FileField(upload_to='book_covers/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

    def __str__(self):
        return self.book_name


class Borrow(models.Model):
    STATUS_CHOICES = (
        ('requested', 'requested'),
        ('borrowed', 'borrowed'),
        ('returned', 'returned'),
    )

    user_borrow = models.ForeignKey(reader, on_delete=models.CASCADE)
    book_borrow = models.ForeignKey(book, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(default=timezone.now)
    return_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='borrowed')

    def __str__(self):
        return f"{self.user_borrow.reader_name} - {self.book_borrow.book_name}"



class Review(models.Model):
    book = models.ForeignKey(book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(reader, on_delete=models.CASCADE)  
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    reply = models.TextField(blank=True, null=True)  

    def __str__(self):
        return f"{self.user.reader_name} - {self.book.book_name}"
    

# models.py

class Cart(models.Model):
    user_cart = models.ForeignKey(reader, on_delete=models.CASCADE, related_name='cart_items')
    book_cart = models.ForeignKey(book, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_cart.reader_name} - {self.book_cart.book_name}"

