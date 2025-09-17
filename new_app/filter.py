# 🔹 Search for Books
import django_filters
from django import forms
from django_filters import CharFilter

from new_app.models import book, author, reader


# class BookFilter(django_filters.FilterSet):
#     book_name = CharFilter(label="", lookup_expr='icontains',
#                            widget=forms.TextInput(attrs={'placeholder': 'Search Book', 'class': 'form-control'}))
#
#     class Meta:
#         model = book
#         fields = ['book_name']

# 🔹 Search for Authors
class AuthorFilter(django_filters.FilterSet):
    author_name = CharFilter(label="", lookup_expr='icontains',
                             widget=forms.TextInput(attrs={'placeholder': 'Search Author', 'class': 'form-control'}))

    class Meta:
        model = author
        fields = ['author_name']

# 🔹 Search for Readers
class ReaderFilter(django_filters.FilterSet):
    reader_name = CharFilter(label="", lookup_expr='icontains',
                             widget=forms.TextInput(attrs={'placeholder': 'Search Reader', 'class': 'form-control'}))

    class Meta:
        model = reader
        fields = ['reader_name']


#search books in author_view
class BookFilter(django_filters.FilterSet):
    book_name = django_filters.CharFilter(field_name='book_name', lookup_expr='icontains', label="Book Name")

    class Meta:
        model = book
        fields = ['book_name']