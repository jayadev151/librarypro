from django.shortcuts import render,HttpResponseRedirect
from .models import User,Books
from .forms import SignUpForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout


# Create your views here.
def signup(request):
    if  not request.user.is_authenticated:
        if request.method =='POST':
            form=SignUpForm(request.POST)
            if form.is_valid():
                messages.success(request,'Account Created Succesfully')
                form.save()

            return render(request,'signup.html',{'form':form})
        else:
            form=SignUpForm()
            return render(request,'signup.html',{'form':form})
    else:
        return HttpResponseRedirect('/profile/')
def user_login(request):
    if  not request.user.is_authenticated:
        if request.method =='POST':
            form=AuthenticationForm(request=request,data=request.POST)
            if form.is_valid():
                uname=form.cleaned_data['username']
                upass=form.cleaned_data['password']
                user=authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    return HttpResponseRedirect('/profile/')

            return render(request,'userlogin.html',{'form':form})
        else:
            form=AuthenticationForm()
        return render(request,'userlogin.html',{'form':form})
    else:
        return HttpResponseRedirect('/profile/')

def profile(request):
    if request.user.is_authenticated:

        book=Books.objects.all()
        return render(request,'profile.html',{'book':book})
def add(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method =='POST':
            Books(
            name=request.POST.get('name'),
            author_name=request.POST.get('author')

            ).save()
            return render(request,'add.html')
        else:
            return render(request,'add.html')
    else:
        return HttpResponseRedirect('/user_login/')
def edit(request,id):
    if request.user.is_authenticated  and request.user.is_superuser:
        book=Books.objects.get(id=id)
        if request.method =='POST':
            book.name=request.POST.get('name')
            book.author_name=request.POST.get('author')
            book.save()
            return HttpResponseRedirect('/profile/')
        else:
            return render(request,'edit.html',{'book':book})
    else:
        return HttpResponseRedirect('/user_login/')
def delete(request,id):
    if request.user.is_authenticated  and request.user.is_superuser:
        book=Books.objects.get(id=id)
        book.delete()
        return HttpResponseRedirect('/profile/')
    else:
        return HttpResponseRedirect('/user_login/')
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/user_login/')
    else:
        return HttpResponseRedirect('/user_login/')
