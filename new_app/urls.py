from django.urls import path

from new_app import views, views_author, views_admin, views_reader

urlpatterns = [
   
    #admin

    # path("login_page",views.login_page,name="login_page"),

    path("first_demo_page",views.first_demo_page,name="first_demo_page"),

    path("admin_view", views.admin_view, name="admin_view"),

    path("",views.login_view,name="login_view"),

    path("account",views.account,name='account'),

    path('logout_view/', views.logout_view, name='logout_view'),


    #views_admin

    path('admin_dashboard', views_admin.admin_dashboard, name='admin_dashboard'),

    path('approve_author/<int:author_id>/', views_admin.approve_author, name='approve_author'),

    path('reject_author/<int:author_id>/', views_admin.reject_author, name='reject_author'),

        #  ADMIN BORROW MANAGEMENT 

    path('monitor_borrow_record/', views_admin.monitor_borrow_record, name='monitor_borrow_record'),

    path('mark_returned/<int:borrow_id>/', views_admin.mark_as_returned, name='mark_as_returned'),
  
    path('create_borrow/', views_admin.create_borrow_record, name='create_borrow_record'),




     #manage_author
    path("manage_author",views_admin.manage_author,name='manage_author'),

    #manage_reader
    path("manage_reader",views_admin.manage_reader,name='manage_reader'),

    path("approve_reader/<int:reader_id>/", views_admin.approve_reader, name='approve_reader'),

    path("reject_reader/<int:reader_id>/", views_admin.reject_reader, name='reject_reader'),



    #borrow_record
    path("borrow_record",views_admin.monitor_borrow_record,name='borrow_record'),

    path("borrow_return/<int:borrow_id>/", views_admin.mark_as_returned, name='borrow_return'),

    #manage_books
    path("manage_books", views_admin.manage_books, name='manage_books'),

    path('approve_book/<int:book_id>/', views_admin.approve_book, name='approve_book'),

    path('reject_book/<int:book_id>/', views_admin.reject_book, name='reject_book'),

    #3 html page
    
    path('approved-books/', views_admin.approved_books, name='admin_approved_books'),
    path('pending-books/', views_admin.pending_books, name='admin_pending_books'),
    path('rejected-books/', views_admin.rejected_books, name='admin_rejected_books'),


    #home_look
    path("admin_home",views_admin.admin_home,name="admin_home"),

    #search
    # path('search/', views_admin.search_admin, name='search_admin'),

    path('search/',views_admin.unified_search, name='unified_search'),


   






    #reader

    path("reader_reg_1", views.reader_reg_1, name="reader_reg_1"),

    path("reader_view",views.reader_view,name="reader_view"),

    path("reader_home",views_reader.reader_home,name='reader_home'),

    # path('borrow/<int:book_id>/', views_reader.borrow_book, name='borrow_reader'),

    path('borrowed_books/', views_reader.borrowed_books, name='borrowed_books'),


    # path('return/<int:borrow_id>/', views_reader.return_book, name='return_book'),

    # path('borrow_history/', views_reader.borrow_history, name='view_borrow_history'),



    path('update_reader_profile/', views_reader.update_reader_profile, name='update_reader_profile'),

    path('books/',views_reader.book_list, name='book-list'),

    path('reader_books_list/',views_reader.reader_book_list, name='reader_book_list'),

    path("borrow/<int:book_id>/", views_reader.borrow_book, name="borrow_book"),

    path("reader/search_book", views_reader.reader_search_book, name="reader_search_book"),
     
    path('add-review/<int:book_id>/', views_reader.add_review, name='add_review'),

    path('my-reviews/', views_reader.reader_reviews, name='reader_reviews'),


    # urls.py (reader section)

path('cart/add/<int:book_id>/', views_reader.add_to_cart, name='add_to_cart'),
path('cart/', views_reader.view_cart, name='view_cart'),
path('cart/remove/<int:cart_id>/', views_reader.remove_from_cart, name='remove_from_cart'),



 




    #author

    path("author_reg_1", views.author_reg_1, name="author_reg_1"),
      #remove or update  author_view
    path("author_view",views.author_view,name="author_view"),

    path("home_outlook",views_author.home_outlook,name='home_outlook'),

    path('add_book', views_author.add_book, name='add_book'),

   # list of book by author
    path("book_list",views_author.book_list,name="book_list"),

    path("delete_book/<int:book_id>/", views_author.delete_book, name="delete_book"),


    #my profile
    path("My_profile",views_author.My_profile,name='My_profile'),

    path("author/view/", views_author.author_view, name='author_view'),


    #approve book and rejected book
    path("author_approve",views_author.author_approve,name='author_approve'),

    path("author_approved_books/",views_author.approved_books_view, name="approved_books"),
    path("author_pending_books/",views_author.pending_books_view, name="pending_books"),
    path("author_rejected_books/",views_author.rejected_books_view, name="rejected_books"),

    # path("author_account_view",views_author.author_account_view, name="author_account_view"),

    #search of books on author
    path("search_book", views_author.author_search_book, name="search_book"),



    path('author/reviews/', views_author.author_reviews, name='author_reviews'),

    path('author/reply-review/<int:review_id>/', views_author.reply_review, name='reply_review'),


]
