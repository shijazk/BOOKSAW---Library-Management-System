from django.shortcuts import redirect, render, get_object_or_404

from new_app.filter import BookFilter
from new_app.form import AuthorProfileForm, BookForm, AuthorUpdateForm
from new_app.models import Review, author, book
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='login_view')
def add_book(request):

    try:
        author_instance = author.objects.get(user_author=request.user)  
    except author.DoesNotExist:
        return render(request, 'author/add_book.html', {'error': "You must be a registered author to add books."})

    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book_instance = form.save(commit=False)
            book_instance.book_author_name = author_instance  
            book_instance.save()
            return redirect('author_view') 

    else:
        form = BookForm()

    return render(request, 'author/add_book.html', {'form': form})



#new author view
# def author_view(request):
#     return render(request,'author/author_view.html')

# def author_view(request):
#     return render(request,'author/author_view_1.html')

@login_required(login_url='login_view')
def author_view(request):
    return render(request, 'author/author_view.html')


#just sample home look
# if want remove
@login_required(login_url='login_view')
def home_outlook(request):
    return render(request,'author/home_outlook.html')



# list of book by author
@login_required(login_url='login_view')
def book_list(request):
    try:
        author_instance = author.objects.get(user_author=request.user)  
        books = book.objects.filter(book_author_name=author_instance)  
    except author.DoesNotExist:
        books = None  

    return render(request, 'author/book_list.html', {'books': books})

@login_required(login_url='login_view')
def delete_book(request, book_id):
    book_instance = get_object_or_404(book, id=book_id, book_author_name__user_author=request.user)
    if request.method == "POST":
        book_instance.delete()
        messages.success(request, "Book deleted successfully!")
        return redirect('book_list')  # back to book list page
    return redirect('book_list')

# list of book by author
#simplified version of book_list
# def book_list(request):
#     books = book.objects.filter(book_author_name__user_author=request.user)
#     return render(request, 'author/book_list.html', {'books': books})


@login_required(login_url='login_view')
def My_profile(request):
    author_instance = author.objects.filter(user_author=request.user).first()
    if not author_instance:
        messages.error(request, "No profile found.")
        return redirect('some_error_page')

    if request.method == "POST":
        form = AuthorUpdateForm(request.POST, instance=author_instance)
        if form.is_valid():
            form.save()
            # messages.success(request, "Profile updated successfully!")
            return redirect('My_profile')  
    else:
        form = AuthorUpdateForm(instance=author_instance)

    return render(request, 'author/author_My_profile.html', {'form': form})








@login_required(login_url='login_view')
def author_approve(request):
    try:
        author_instance = author.objects.get(user_author=request.user)  
        approved_books = book.objects.filter(book_author_name=author_instance, is_approved=True)
        rejected_books = book.objects.filter(book_author_name=author_instance, is_rejected=True)
        pending_books = book.objects.filter(book_author_name=author_instance, is_approved=False, is_rejected=False)
    except author.DoesNotExist:
        approved_books = rejected_books = pending_books = []

    return render(request, 'author/author_approve.html', {
        'approved_books': approved_books,
        'rejected_books': rejected_books,
        'pending_books': pending_books
    })

@login_required(login_url='login_view')
def approved_books_view(request):
    try:
        author_instance = author.objects.get(user_author=request.user)
        approved_books = book.objects.filter(book_author_name=author_instance, is_approved=True)
    except author.DoesNotExist:
        approved_books = []

    return render(request, 'author/author_approved_books.html', {'approved_books': approved_books})

@login_required(login_url='login_view')
def pending_books_view(request):
    try:
        author_instance = author.objects.get(user_author=request.user)
        pending_books = book.objects.filter(book_author_name=author_instance, is_approved=False, is_rejected=False)
    except author.DoesNotExist:
        pending_books = []

    return render(request, 'author/author_pending_books.html', {'pending_books': pending_books})

@login_required(login_url='login_view')
def rejected_books_view(request):
    try:
        author_instance = author.objects.get(user_author=request.user)
        rejected_books = book.objects.filter(book_author_name=author_instance, is_rejected=True)
    except author.DoesNotExist:
        rejected_books = []

    return render(request, 'author/author_rejected_books.html', {'rejected_books': rejected_books})


# def author_account_view(request):
#
#
#     print(f"Logged-in user: {request.user}")  # Print username
#     print(f"User ID: {request.user.id}")  # Print User ID
#
#     author_instance = None
#
#     if request.user.is_authenticated:
#         try:
#             author_instance = author.objects.get(user_author=request.user)
#         except author.DoesNotExist:
#             author_instance = None  # If the logged-in user is not an author
#
#     return render(request, 'author/author_view.html', {'author_instance': author_instance})



@login_required(login_url='login_view')
def author_search_book(request):
    query = request.GET.get('q', '')  
    books = book.objects.filter(book_name__icontains=query) if query else None 

    return render(request, 'author/author_search_book.html', {'books': books})


@login_required(login_url='login_view')
def author_reviews(request):
    
    author_instance = author.objects.get(user_author=request.user)
    
    author_books = book.objects.filter(book_author_name=author_instance)
        
    reviews = Review.objects.filter(book__in=author_books)
    
    return render(request, 'author/author_reviews.html', {'reviews': reviews})


@login_required(login_url='login_view')
def reply_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if request.method == "POST":
        reply_text = request.POST.get("reply")
        review.reply = reply_text
        review.save()
        return redirect('author_reviews')

    return render(request, 'author/reply_review.html', {'review': review})