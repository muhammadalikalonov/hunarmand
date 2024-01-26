from django.shortcuts import render, redirect

from .models import Anketa, Anketa_File, Anketa_Profile_Image, User, Ball, Customer_Comment
from django.db.models import Q
from django.views import generic
from rest_framework.permissions import AllowAny, IsAuthenticated



def home_admin(request):
    return render(request, 'Hunarmand_Admin/index.html')


class Kelgan_Ariza(generic.CreateView):
    queryset = Anketa.objects.all()
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            cancel = Anketa.objects.filter(status_progress=True,status_cancel=True).count()

            anketa = Anketa.objects.filter(status_new=True, status_progress=False, excel_malumot=False)
            like = Anketa.objects.filter(status_progress=True, excel_malumot=False)
            kelgan_ariza_soni = anketa.count()
            confirm = Anketa.objects.filter(status_confirm=True).count()
            jarayonda = like.count()
            print(request.user.username)
            context = {
                'cancel':cancel,
                'anketa':anketa,
                'kelgan_ariza_soni':kelgan_ariza_soni,
                'jarayonda':jarayonda,
                'confirm':confirm
             
            }
            print(anketa)
            return render(request, 'Hunarmand_Admin/index.html', context)
        else:
            return redirect("Login_admin")
    
    def post(self, request, *args, **kwargs):
        pass


class Jarayonda(generic.CreateView):
    queryset =  Anketa.objects.all()
    permission_classes = [IsAuthenticated]
    template_name = 'Hunarmand_Admin/progress.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            anketa = Anketa.objects.filter(status_new=True, status_progress=False, excel_malumot=False)
            like = Anketa.objects.filter(status_progress=True)

            kelgan_ariza_soni = len(anketa)
            jarayonda = len(like)
            ball_data = Ball.objects.all()
            custom_comment =  Customer_Comment.objects.all()
            cancel = len(Anketa.objects.filter(status_new=True,status_cancel=True))

            confirm = len(Anketa.objects.filter(status_confirm=True))
            print(like)
            if ball_data:
                bal = ball_data.latest('id')
            
            context = {
                'cancel':cancel,
                'like':like,
                'kelgan_ariza_soni':kelgan_ariza_soni,
                'jarayonda':jarayonda,
                'bal':bal,
                'custom_comment':custom_comment, 
                'confirm':confirm

            }
            return render(request, 'Hunarmand_Admin/progress.html', context)
        else:
            return redirect("Login_admin")
    

    def post(self, request, *args, **kwargs):
        pass


class Tasdiqlash(generic.CreateView):
    queryset = Anketa.objects.all()
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            ball = Ball.objects.latest("id")
            anketa1 = Anketa.objects.all().filter(status_progress=True)
            cancel = len(Anketa.objects.filter(status_new=True,status_cancel=True))
            print(anketa1)
            for i in anketa1:
                if i.like_number >= ball.ball:
                    i.status_confirm = True
                    i.status_progress = False
                    i.tasdiqlangan_data = datetime.date.today()
                    print(datetime.date.today())
                    i.save()
                    print("tasdiqlandi")

                
            

            anketa = Anketa.objects.filter(status_confirm=True)
            anketa1 = Anketa.objects.filter(status_new=True, status_progress=False, excel_malumot=False)
            like = Anketa.objects.filter(status_progress=True, status_confirm=False)
            confirm = len(anketa)
            jarayonda = len(like)
            kelgan_ariza_soni = len(anketa1)
            context = {
                'cancel':cancel,
                'anketa':anketa,
                'confirm':confirm,
                'jarayonda':jarayonda,
                'kelgan_ariza_soni': kelgan_ariza_soni,
            }
            
            return render(request, 'Hunarmand_Admin/conf.html', context)
        else:
            return redirect("Login_admin")
    
    def post(self, request, *args, **kwargs):
        pass

class Bekor_qilganlar(generic.CreateView):
    queryset = Anketa.objects.all()
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:

            anketa = Anketa.objects.filter(status_new=True,status_cancel=True)
            cancel = len(Anketa.objects.filter(status_new=True,status_cancel=True))

            like = Anketa.objects.filter(status_progress=True, excel_malumot=False)
            kelgan_ariza_soni = len(anketa)
            jarayonda = len(like)


            
            user  =  User.objects.all()
            s=0
            for i in user:
                if i.status == 'Hakam':
                    s+=1

            print(s)
            
            
            anketa1 = Anketa.objects.all().filter(status_progress=True)
            print(anketa1)
            for i in anketa1:
                if i.dislike_number >= s/2:
                    i.status_cancel = True
                    i.status_progress = False
            
                    i.save()
                    print("bekor qilindi")
            



            print(request.user.username)
            context = {
                'cancel':cancel,
                'anketa':anketa,
                'kelgan_ariza_soni':kelgan_ariza_soni,
                'jarayonda':jarayonda
             
            }
            print(anketa)
            return render(request, 'Hunarmand_Admin/cancel.html', context)
        else:
            return redirect("Login_admin")
    
    def post(self, request, *args, **kwargs):
        pass




import datetime

def all_anketa(request):
    if request.user.is_authenticated:
        anketa =  Anketa.objects.all()
        anketa_arxiv = Anketa.objects.filter(archive=True)
        today = datetime.date.today()
      
        for i in anketa:
            if len(i.guvohnoma_end_date) < 15:
                try:
                    date = datetime.datetime.strptime(i.guvohnoma_end_date, "%Y-%m-%d").date()
                    print(i)
                except ValueError:
                    # If the first format fails, try the alternative format
                    date = datetime.datetime.strptime(i.guvohnoma_end_date, "%d.%m.%Y").date()
                    print(i)
            else:
                print(i)
                date = datetime.datetime.strptime(i.guvohnoma_end_date, "%Y-%m-%d  %H:%M:%S.%f").date()
            

            print(date)
            if date < today:
                anketa1 = Anketa.objects.get(id=i.id)
                
                anketa1.archive = True
                anketa1.save()
                print(date)
                


        
            
        context = { 
            'anketa':anketa,
            'today' : today,
            'anketa_arxiv':anketa_arxiv
        }
        return render(request,'Hunarmand_Admin/all_anketa.html', context )
    else:
        return redirect("Login_admin")

def ball(request):
    if request.user.is_authenticated:
        ball_data = Ball.objects.all()
        if ball_data:

            bal = ball_data.latest('id')
        else:
            bal =3 
        ball =  request.POST.get("ball")

        if ball:
            Ball.objects.all().delete()
            ball_create = Ball.objects.create(
                ball = ball
            )
            ball_create.save()
            return render(request, 'Hunarmand_Admin/progress.html')
        return render(request, 'Hunarmand_Admin/ball.html', {'bal':bal})
    else:
        return redirect("Login_admin")



def hunarmand_delate(request, id):
    anketa = Anketa.objects.filter(id=id)
    anketa.delete()
    return redirect('all_anketa')


def bekor_hammasi_ochirish(request):
    anketa = Anketa.objects.all().filter(status_cancel=True)
    anketa.delete()
    return redirect('cancel')


def customer_status_edit(request, id):
    anketa = Anketa.objects.filter(id=id)
    
    context ={
        'anketa':anketa
    }
    return render(request, 'Hunarmand_Admin/customer_status_edit.html', context)


def customer_delete(request, id):
    anketa = Anketa.objects.filter(id=id)
    anketa1 = Anketa.objects.get(id=id)
    anketa_image_profile = Anketa_Profile_Image.objects.filter(anketa=anketa1)
    print(anketa_image_profile)
    if request.method == "POST":
        anketa.delete()
        return redirect("cancel")
    context ={
        'anketa':anketa,
        'anketa_image_profile':anketa_image_profile,
    }
    return render(request, 'Hunarmand_Admin/customer_delete.html', context)



