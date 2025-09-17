from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


from django.http import HttpResponse
from django.shortcuts import render, redirect

from new_app.form import reader_reg, author_reg, Login_reg

from django.contrib.auth.decorators import login_required



# def login_page(request):
#     return render(request,'login_view.html')

def first_demo_page(request):
    return render(request,'index.html')


def reader_reg_1(request):
    form1 = Login_reg()
    form2=reader_reg()
    if request.method=='POST':
        form1 = Login_reg(request.POST)

        form2 =reader_reg(request.POST)
        if form1.is_valid() and form2.is_valid():
            user1 = form1.save(commit=False)
            user1.is_reader = True
            user1.save()

            user2 = form2.save(commit=False)
            user2.user_reader = user1
            user2.save()

            return redirect('login_view')
    return render(request,'reader_reg_1.html',{'form1':form1,'form2':form2})




def author_reg_1(request):
    form3 = Login_reg()
    form4=author_reg()

    if request.method=='POST':
        form3 = Login_reg(request.POST)

        form4 = author_reg(request.POST)

        if form3.is_valid() and form4.is_valid():
            user1 = form3.save(commit=False)
            user1.is_author = True
            user1.save()

            user2 = form4.save(commit=False)
            user2.user_author = user1
            user2.save()

            return redirect("login_view")
    return render(request,'author_reg_1.html',{"form3":form3,'form4':form4})


def login_view(request):

    if request.method == 'POST':

        username =request.POST.get('uname')
        password =request.POST.get('password')
        user= authenticate(request,username=username, password=password)

        if user is not None:
            login(request,user)
            if user.is_staff:
                return redirect('admin_view')
            elif user.is_reader:
                 return redirect('reader_view')
            elif user.is_author:
                 return redirect('author_view')
        else:
            messages.info(request,'invalid credentials')


    return render(request,'login_view.html')



@login_required(login_url='login_view')
def admin_view(request):
    return render(request,'admin/admin_view.html')

@login_required(login_url='login_view')
def reader_view(request):
    return render(request,'reader/reader_view.html')

@login_required(login_url='login_view')
def author_view(request):
    return render(request,'author/author_view.html')

#for top side account section
@login_required(login_url='login_view')
def account(request):
    return render(request,'account.html')




def logout_view(request):
    logout(request)
    return redirect('login_view')
