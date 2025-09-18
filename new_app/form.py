from django.contrib.auth.forms import UserCreationForm
from django import forms

from new_app.models import Login, reader, author, book


class Login_reg(UserCreationForm):
    username=forms.CharField()
    password1 = forms.CharField(label="password",widget=forms.PasswordInput)
    password2 = forms.CharField(label="conform password", widget=forms.PasswordInput)

    class Meta:
        model = Login
        fields =('username','password1','password2')



class reader_reg(forms.ModelForm):
    class Meta:
        model=reader
        fields="__all__"
        exclude=('user_reader', 'is_approved',)




class author_reg(forms.ModelForm):
    class Meta:
        model=author
        fields="__all__"
        exclude=('user_author', 'is_approved', 'is_rejected')



#
# class bookform(forms.ModelForm):
#     class Meta:
#         model = book
#         fields = ['book_name', 'book_author_name', 'category','book_cover']
#         widgets = {
#             'book_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter book name'}),
#             'book_author_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter author name'}),
#             'category': forms.Select(attrs={'class': 'form-control'}),
#             'book_cover': forms.ClearableFileInput(attrs={'class': 'form-control'}),
#         }

# class BookForm(forms.ModelForm):
#     class Meta:
#         model = book
#         fields = ['book_name', 'category', 'book_cover', 'price']
#         exclude = ['book_author_name', 'is_approved']

class BookForm(forms.ModelForm):
    class Meta:
        model = book
        fields = ['book_name', 'category', 'book_cover', 'price']
        widgets = {
            'book_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter book name'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'book_cover': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
        }


class AuthorProfileForm(forms.ModelForm):
    class Meta:
        model = author
        fields = ['author_name', 'author_phone_no', 'author_email', 'author_address']




class AuthorUpdateForm(forms.ModelForm):
    class Meta:
        model = author
        fields = ['author_name', 'author_phone_no', 'author_email', 'author_address']
        widgets = {
            'author_name': forms.TextInput(attrs={'class': 'form-control'}),
            'author_phone_no': forms.TextInput(attrs={'class': 'form-control'}),
            'author_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'author_address': forms.TextInput(attrs={'class': 'form-control'}),
        }




class ReaderProfileForm(forms.ModelForm):
    class Meta:
        model = reader
        fields = ['reader_name', 'reader_phone_no', 'reader_email', 'reader_address']
        widgets = {
            'reader_name': forms.TextInput(attrs={'class': 'form-control'}),
            'reader_phone_no': forms.TextInput(attrs={'class': 'form-control'}),
            'reader_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'reader_address': forms.TextInput(attrs={'class': 'form-control'}),
        }