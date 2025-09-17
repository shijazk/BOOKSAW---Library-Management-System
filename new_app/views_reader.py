from _ast import Return

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from datetime import timedelta

from new_app.form import ReaderProfileForm
from .models import Borrow, Review, book, reader ,Cart
from django.contrib.auth.decorators import login_required

@login_required(login_url='login_view')
def reader_home(request):
    return render(request,'reader/reader_home.html')



@login_required(login_url='login_view')
def update_reader_profile(request):
    try:
        user_reader = reader.objects.get(user_reader=request.user)
    except reader.DoesNotExist:
        messages.error(request, "Profile not found. Please contact support or register.", extra_tags="profile")
        return redirect('reader_home')  

    if request.method == 'POST':
        form = ReaderProfileForm(request.POST, instance=user_reader)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!", extra_tags="profile")
            return redirect('update_reader_profile')  
        else:
            messages.error(request, "Please correct the errors below.", extra_tags="profile")
    else:
        form = ReaderProfileForm(instance=user_reader)

    return render(request, 'reader/update_profile.html', {'form': form, 'user_reader': user_reader})

@login_required(login_url='login_view')
def book_list(request):
    books = book.objects.all()  # Fetch all books (added by admin and authors)
    return render(request, 'reader/book_list.html', {'books': books})

@login_required(login_url='login_view')
def reader_book_list(request):
    books = book.objects.filter(is_approved=True)  # Fetch only admin-approved books
    print(books)
    return render(request, 'reader/book_list.html', {'books': books})



@login_required(login_url='login_view')
def reader_search_book(request):
    query = request.GET.get('q', '')

    if query:
        books = book.objects.filter(
            Q(book_name__icontains=query) | Q(book_author_name__author_name__icontains=query),
            is_approved=True
        )
    else:
        books = None

    return render(request, 'reader/reader_search_book.html', {'books': books, 'query': query})



#woring one
# def add_review(request, book_id):
#     book_instance = get_object_or_404(book, id=book_id)

#     if request.method == "POST":
#         review_text = request.POST.get("review")
#         if review_text:
#             
#             reader_instance = get_object_or_404(reader, user_reader=request.user)

#             Review.objects.create(
#                 book=book_instance,
#                 user=reader_instance,     
#                 review_text=review_text
#             )
#         return redirect('reader_book_list')

#     return render(request, 'author/add_review.html', {'book': book_instance})

@login_required(login_url='login_view')
def add_review(request, book_id):
    book_instance = get_object_or_404(book, id=book_id)

    if request.method == "POST":
        review_text = request.POST.get("review")
        if review_text:
            reader_instance = get_object_or_404(reader, user_reader=request.user)
            Review.objects.create(
                book=book_instance,
                user=reader_instance,
                review_text=review_text
            )
        return redirect('reader_book_list')

    return render(request, 'reader/add_review.html', {'book': book_instance})

@login_required(login_url='login_view')
def reader_reviews(request):
    
    reader_instance = request.user.reader.first()
    
    reviews = Review.objects.filter(user=reader_instance)
    return render(request, 'reader/reader_reviews.html', {'reviews': reviews})

@login_required(login_url='login_view')
def borrow_book(request, book_id):
    
    book_instance = get_object_or_404(book, id=book_id)
    
    reader_instance = request.user.reader.first()
    
    if not reader_instance:
        
        return redirect('some_error_page')

    if request.method == "POST":
        days = int(request.POST.get("days", 7))
        return_date = timezone.now() + timedelta(days=days)
        
        
        Borrow.objects.create(
            book_borrow=book_instance,    
            user_borrow=reader_instance, 
            return_date=return_date,
            status='borrowed'
        )
        
        return redirect('reader_book_list')

    
    return render(request, 'reader/borrow_book.html', {'book': book_instance})

@login_required(login_url='login_view')
def borrowed_books(request):
    reader_instance = request.user.reader.first()
    borrowed = Borrow.objects.filter(user_borrow=reader_instance)
    return render(request, 'reader/borrow_book_list.html', {'borrowed': borrowed})



@login_required(login_url='login_view')
def add_to_cart(request, book_id):
    book_instance = get_object_or_404(book, id=book_id)
    reader_instance = request.user.reader.first()

    if not reader_instance:
        messages.error(request, "Reader profile not found.")
        return redirect('reader_home')

    # Prevent duplicate cart entries
    existing = Cart.objects.filter(user_cart=reader_instance, book_cart=book_instance).first()
    if existing:
        messages.info(request, "This book is already in your cart.")
    else:
        Cart.objects.create(user_cart=reader_instance, book_cart=book_instance)
        messages.success(request, f"{book_instance.book_name} added to cart.")

    return redirect('reader_book_list')

@login_required(login_url='login_view')
def view_cart(request):
    reader_instance = request.user.reader.first()
    if not reader_instance:
        messages.error(request, "Reader profile not found.")
        return redirect('reader_home')

    cart_items = Cart.objects.filter(user_cart=reader_instance)
    return render(request, 'reader/view_cart.html', {'cart_items': cart_items})

@login_required(login_url='login_view')
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id)
    cart_item.delete()
    messages.success(request, "Book removed from cart.")
    return redirect('view_cart')