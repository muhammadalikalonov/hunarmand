

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm

from .models import User

from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password





def register(request):
    if request.method == 'POST':        
        username  =  request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 =  request.POST.get("password2")
        status = request.POST.get("status")
        print(f"{username}-{password1}-{password2}-{status}")
        user_name =  User.objects.filter(username=username)
        if user_name:
            users =  User.objects.all()
            message = f"Bu username '{username}' bazada mavjud"
            context = {
            'users':users, 
            'message':message
            }
            return render(request, 'Hunarmand_Admin/register.html', context)
        user  =  User(
            username =  username,
            status = status
        )
   
        user.set_password(password1)
        user.save()
        users =  User.objects.all()
        context = {
            'users':users
        }
        return render(request, 'Hunarmand_Admin/register.html', context)
    else:
        users =  User.objects.all()
        context = {
            'users':users
        }
        return render(request, 'Hunarmand_Admin/register.html', context)




def change_user_password(request, id):
    if request.method == 'POST':
        new_password =  request.POST.get("new_password")
        user =  User.objects.get(id=id)
        user.set_password(new_password)
        user.save()
        users =  User.objects.all()
        context = {
            'users':users
        }
        return render(request, 'Hunarmand_Admin/register.html', context)
    else:
        users =  User.objects.filter(id=id)
        
        context = {
            
            'users':users
        }
        return render(request, 'Hunarmand_Admin/new_pasword.html', context)




def Login_admin(request):
    if request.method == 'POST':
  
        # AuthenticationForm_can_also_be_used__
  
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password, status=None)
        if user is not None:
            login(request, user)
            print(user)
            
            if User.objects.filter(username=user, status=None):

                return redirect('kelgan_ariza')
            elif User.objects.filter(username=user, status="Admin"):

                return redirect('kelgan_ariza')
            else:
                message = "Siz Admin emas siz  !!!"

                context = {
                                "message":message,
                        }
                return render(request, 'Hunarmand_Admin/login_admin.html', context)
        else:
            message = "Login yoki Parol xato !!!"

            context = {
                "message":message,
            }
            return render(request, 'Hunarmand_Admin/login_admin.html', context)
   
    return render(request, 'Hunarmand_Admin/login_admin.html')

def user_delete(request, id):
    user= User.objects.filter(id=id)
    print(user)
    user.delete()
   
    return redirect("Register")



def logout_view(request):
    logout(request)
    return redirect('Login_admin')