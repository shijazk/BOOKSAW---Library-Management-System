from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from new_app.filter import BookFilter, AuthorFilter, ReaderFilter
from new_app.models import author, book, Login, Borrow, reader
from django.contrib.auth.decorators import login_required

@login_required(login_url='login_view')
def admin_dashboard(request):
    authors = author.objects.filter(is_approved=False)  
    books = book.objects.filter(is_approved=False)  
    users = Login.objects.filter(is_reader=True)  
    borrow_records = Borrow.objects.all() 

    return render(request, 'admin/admin_dashboard.html', {
        'authors': authors,
        'books': books,
        'users': users,
        'borrow_records': borrow_records
    })

# def manage_author(request):
#     authors = author.objects.all()
#     return render(request,'admin/manage_author.html', {'authors': authors})



@login_required(login_url='login_view')
def manage_author(request):
    approved_authors = author.objects.filter(is_approved=True, is_rejected=False)  
    pending_authors = author.objects.filter(is_approved=False, is_rejected=False)  
    rejected_authors = author.objects.filter(is_rejected=True)

    return render(request, 'admin/manage_author.html', {
        'approved_authors': approved_authors,
        'pending_authors': pending_authors,
        'rejected_authors': rejected_authors
    })


@login_required(login_url='login_view')
def approve_author(request, author_id):
    authors = get_object_or_404(author, id=author_id)
    authors.is_approved = True
    authors.is_rejected = False
    authors.save()
    messages.success(request, "Author approved successfully!")
    return redirect('manage_author')



@login_required(login_url='login_view')
def reject_author(request, author_id):
    authors = get_object_or_404(author, id=author_id)
    authors.is_rejected = True
    authors.is_approved = False  
    authors.save()
    messages.error(request, "Author rejected successfully!")
    return redirect('manage_author')

@login_required(login_url='login_view')
def rejected_authors(request):
    rejected_authors = author.objects.filter(is_rejected=True)
    return render(request, 'admin/rejected_authors.html', {'rejected_authors': rejected_authors})



@login_required(login_url='login_view')
def manage_books(request):
    """View books with pending, approved, and rejected status"""
    approved_books = book.objects.filter(is_approved=True, is_rejected=False)
    pending_books = book.objects.filter(is_approved=False, is_rejected=False)
    rejected_books = book.objects.filter(is_rejected=True)

    return render(request, 'admin/manage_books.html', {
        'approved_books': approved_books,
        'pending_books': pending_books,
        'rejected_books': rejected_books
    })

@login_required(login_url='login_view')
def approve_book(request, book_id):
    
    books = get_object_or_404(book, id=book_id)
    books.is_approved = True
    books.save()
    messages.success(request, "Book approved successfully!")
    return redirect('manage_books')

@login_required(login_url='login_view')
def reject_book(request, book_id):
    
    books = get_object_or_404(book, id=book_id)
    books.delete()
    messages.error(request, "Book rejected and deleted!")
    return redirect('manage_books')


#3 seperate html page
@login_required(login_url='login_view')
def approved_books(request):
    approved_books = book.objects.filter(is_approved=True, is_rejected=False)
    return render(request, 'admin/manage_bk_approved_books.html', {'approved_books': approved_books})

@login_required(login_url='login_view')
def pending_books(request):
    pending_books = book.objects.filter(is_approved=False, is_rejected=False)
    return render(request, 'admin/manage_bk_pending_books.html', {'pending_books': pending_books})

@login_required(login_url='login_view')
def rejected_books(request):
    rejected_books = book.objects.filter(is_rejected=True)
    return render(request, 'admin/manage_bk_rejected_books.html', {'rejected_books': rejected_books})


# def manage_reader(request):
#     readers = reader.objects.all()
#     return render(request,'admin/manage_reader.html', {'readers': readers})

@login_required(login_url='login_view')
def borrow_record(request):
    borrow_records = Borrow.objects.all()
    return render(request,'admin/borrow_record.html', {'borrow_records': borrow_records})

@login_required(login_url='login_view')
def mark_as_returned(request, borrow_id):
    """Mark a book as returned"""
    borrow = get_object_or_404(Borrow, id=borrow_id)
    borrow.mark_as_returned()
    messages.success(request, f"Book '{borrow.book_borrow.book_name}' returned by {borrow.user_borrow.reader_name}")
    return redirect('borrow_record')



@login_required(login_url='login_view')
def manage_reader(request):
    approved_readers = reader.objects.filter(is_approved=True, is_rejected=False)
    pending_readers = reader.objects.filter(is_approved=False, is_rejected=False)
    rejected_readers = reader.objects.filter(is_rejected=True)

    return render(request, 'admin/manage_reader.html', {
        'approved_readers': approved_readers,
        'pending_readers': pending_readers,
        'rejected_readers': rejected_readers,
    })

@login_required(login_url='login_view')
def approve_reader(request, reader_id):
    reader_obj = get_object_or_404(reader, id=reader_id)
    reader_obj.is_approved = True
    reader_obj.is_rejected = False
    reader_obj.save()
    messages.success(request, f"Reader {reader_obj.reader_name} approved!")
    return redirect('manage_reader')


@login_required(login_url='login_view')
def reject_reader(request, reader_id):
    reader_obj = get_object_or_404(reader, id=reader_id)
    reader_obj.is_rejected = True
    reader_obj.is_approved = False
    reader_obj.save()
    messages.success(request, f"Reader {reader_obj.reader_name} rejected!")
    return redirect('manage_reader')

@login_required(login_url='login_view')
def admin_home(request):
    return render(request,'admin/admin_home.html')







@login_required(login_url='login_view')
def unified_search(request):
    query = request.GET.get('q', '').strip()
    books = book.objects.none()
    author_results = author.objects.none()
    reader_results = reader.objects.none()

    if query:
        # Check books first
        books = book.objects.filter(book_name__icontains=query)
        if books.exists():
            # If book found → clear others
            author_results = author.objects.none()
            reader_results = reader.objects.none()

        else:
            # If no book, check authors
            author_results = author.objects.filter(author_name__icontains=query)
            if author_results.exists():
                books = book.objects.none()
                reader_results = reader.objects.none()

            else:
                # If no author, check readers
                reader_results = reader.objects.filter(reader_name__icontains=query)
                if reader_results.exists():
                    books = book.objects.none()
                    author_results = author.objects.none()

    return render(request, 'admin/unified_search.html', {
        'query': query,
        'books': books,
        'authors': author_results,
        'readers': reader_results
    })


# rejected book in author_view
@login_required(login_url='login_view')
def reject_book(request, book_id):
    """Reject a book by marking it as rejected"""
    books = get_object_or_404(book, id=book_id)
    books.is_approved = False
    books.is_rejected = True 
    books.save()
    messages.error(request, "Book rejected!")
    return redirect('manage_books')

#new add
#borrow new
@login_required(login_url='login_view')
def monitor_borrow_record(request):
    """Admin view to monitor all borrow records"""
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', 'all')

    borrow_records = Borrow.objects.all()

    
    if search_query:
        borrow_records = borrow_records.filter(
            Q(user_borrow__reader_name__icontains=search_query) |
            Q(book_borrow__book_name__icontains=search_query)
        )

    
    if status_filter != 'all':
        borrow_records = borrow_records.filter(status=status_filter)

    borrow_records = borrow_records.order_by('-borrow_date').order_by('id')

    
    paginator = Paginator(borrow_records, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

   
    total_borrowed = Borrow.objects.filter(status='borrowed').count()
    total_returned = Borrow.objects.filter(status='returned').count()

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'total_borrowed': total_borrowed,
        'total_returned': total_returned,
    }
    return render(request, 'admin/monitor_borrow_record.html', context)

@login_required(login_url='login_view')
def mark_as_returned(request, borrow_id):
    """Mark a borrow record as returned"""
    borrow = get_object_or_404(Borrow, id=borrow_id)
    if borrow.status == 'borrowed':
        borrow.status = 'returned'
        borrow.return_date = timezone.now()
        borrow.save()
        messages.success(request, f"Book '{borrow.book_borrow.book_name}' marked as returned.")
    else:
        messages.warning(request, "This record is already returned.")
    return redirect('monitor_borrow_record')

@login_required(login_url='login_view')
def create_borrow_record(request):
    """(Optional) Admin can create borrow records manually"""
    if request.method == "POST":
        reader_id = request.POST.get("reader")
        book_id = request.POST.get("book")

        try:
           
            reader_instance = reader.objects.get(id=reader_id)
            book_instance = book.objects.get(id=book_id)
            print(reader_instance)

            Borrow.objects.create(
                user_borrow=reader_instance,
                book_borrow=book_instance,
                status="borrowed"
            )
            messages.success(request, "Borrow record created successfully.")
        except:
            messages.error(request, "Invalid reader or book.")
        return redirect("monitor_borrow_record")

    readers = reader.objects.filter(approved=True)
    books = book.objects.filter(is_approved=True)

    return render(request, "admin/create_borrow_record.html", {
        "readers": readers,
        "books": books
    })


