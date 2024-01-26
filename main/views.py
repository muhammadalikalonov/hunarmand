
from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpRequest, response, HttpResponse
import requests
from .models import Anketa, Anketa_File, User, Anketa_Profile_Image, Customer_Comment
# Create your views here.
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import json
from django.views import generic
from urllib.request import urlopen
from django.urls import reverse_lazy
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout




############################# API ############################################
from rest_framework import viewsets
from .serializers import Anketa_Serializers
from rest_framework.response import Response

from rest_framework import generics 
from rest_framework import status

class Anketa_ListAPIiew1(generics.ListAPIView):
    queryset = Anketa.objects.all()
    serializer_class = Anketa_Serializers

    def get(self, request, pin,*args, **kwargs):
        try:

            anketa = self.get_queryset().get(pin=pin)
       
            serializer =self.get_serializer(anketa)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
     

    

def bazaga_yuborildi(request):
    return render(request, 'saqlandi.html')



 
# class Anketa_ListAPIView(viewsets.ModelViewSet):
#     queryset = Anketa.objects.all()
#     serializer_class = Anketa_Serializers



























def error_404(request, exception):
    return render(request, '404.html')

def login_anketa(request):
    
    if request.method == 'POST':
        print("salom")
        username =  request.POST['username']
        password = request.POST['password']
        print(username)
        user =  authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(user)
            if  User.objects.filter(username=user, status = "Hakam"):
                
                return redirect("kengash")
            elif User.objects.filter(username=user, status = "Menejer"):
                return redirect("menejr")
            elif User.objects.filter(username=user, status = "Admin"):
                return redirect("kelgan_ariza")
            elif User.objects.filter(username=user, status = None):
                return redirect("kelgan_ariza")
            
            
        else:
            message  = "login yoki parol xato"
            return render(request, 'login.html', {'message':message})

   
    return render(request, 'login.html')



def logout_home(request):
    logout(request)
    return redirect('home')
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def anketa_file(request, pk):
    if request.method == "POST":
        anketa = Anketa.objects.get(id=pk)
        print(anketa)
        file = request.FILES.get("file")
        anketa_file = Anketa_File.objects.create(
            anketa=anketa,
            file = file
        )
        anketa_file.save()
        return JsonResponse({'file_id':anketa_file.id}) 




@csrf_exempt
def anketa_image_profile(request, pk):
    if request.method == "POST":
        anketa = Anketa.objects.get(id=pk)
        print(anketa)
        image_profile = request.FILES.get("cropimage")
        anketa_file = Anketa_Profile_Image.objects.create(
            anketa=anketa,
            image_profile = image_profile
        )
        anketa_file.save()
        return JsonResponse({'file_id':anketa_file.id}) 

class AnketaViews(generic.CreateView):
    template_name = "ariza.html"
    queryset = Anketa.objects.all()
    fields = "__all__"
    success_url = reverse_lazy('anketapostview')
    


    def get_context_data(self, **kwargs):
       
        context =  super().get_context_data(**kwargs)
        anketa = Anketa.objects.get(id=self.kwargs['id'])
        anketa_file = Anketa_File.objects.filter(anketa=anketa)
        anketa_image_profile = Anketa_Profile_Image.objects.filter(anketa=anketa)
        if anketa_image_profile:
            anketa_image_profile = Anketa_Profile_Image.objects.filter(anketa=anketa).latest("id")

        print(anketa_image_profile)
        context = { 
             'anketa':anketa,
             'anketa_image_profile':anketa_image_profile,
             'anketa_file':anketa_file,
        }


        return context
    
    def post(self, request, *args, **kwargs):
       
        form =  request.POST
        file1  =  request.FILES

        
        anketa =  Anketa.objects.get(id=self.kwargs['id'])


        telfon_raqam = form.get("phone")
        if telfon_raqam[-1] == ',':
            telfon_raqam = telfon_raqam.replace(f'{telfon_raqam[-1]}', '')
          
        else:
            telfon_raqam =telfon_raqam

        
        print(form.get("girft"))
        anketa.tin = form.get("tin")
        anketa.fl_address_U = form.get("fl_address_U")
        anketa.mahalla = form.get("mahalla")
        anketa.girft = form.get("girft")
        anketa.phone = telfon_raqam
        anketa.birthday = form.get("birthday")
        anketa.information = form.get("information")
        anketa.email =  form.get("email")
        anketa.ctzn = form.get("ctzn")
        anketa.millati = form.get("millati")
        anketa.fl_address_V = form.get("fl_address_V")
        anketa.fl_address_T = form.get("fl_address_T")
        anketa.viloyati = form.get('viloyati')
        anketa.tumani = form.get('tumani')
        anketa.pport_file = file1.get("pport_file")
        anketa.guvohnoma_file = file1.get('guvohnoma')
        anketa.web_site = form.get("web_site")
        anketa.number_of_students = form.get("number_of_students")
        anketa.state_award =  form.get("state_award")
        anketa.yurtmizda_tadbir = form.get("yurtmizda_tadbir")
        anketa.xorjiy_tadbir = form.get("xorjiy_tadbir")
        anketa.personal_event =  form.get("personal_event")
        anketa.memberyear = form.get("memberyear")
        anketa.creativity = form.get("creativity")
        anketa.manufactured_product =  form.get("manufactured_product")
        anketa.additional_Information = form.get("additional_Information")
        
        anketa.save()
        
     
        return redirect("ariza_edit", anketa.pk)
    
mess1 =[]
class ArizaEdit(generic.UpdateView):
    queryset = Anketa.objects.all()
    template_name = 'ariza_edit.html'

    def get(self, request, *args, **kwargs):
        mess1.clear()
        anketa = Anketa.objects.get(id=self.kwargs['id'])
        anketa1 =  Anketa.objects.filter(id=anketa.id)
        anketa_file = Anketa_File.objects.filter(anketa=anketa)
        anketa_image_profile = Anketa_Profile_Image.objects.filter(anketa=anketa)
        if anketa_image_profile:
            anketa_image_profile = Anketa_Profile_Image.objects.filter(anketa=anketa).latest("id")
       
        context = {
            'anketa1':anketa1,
            'anketa':anketa,
            'anketa_file':anketa_file,
            'anketa_image_profile' :anketa_image_profile
        }
        return render(request, 'ariza_edit.html', context)

    def post(self, request, *args, **kwargs):
        anketa11 = Anketa.objects.get(id=self.kwargs['id'])
        anketa11.baza_save = False
        anketa11.save()
        mess1.append("Bazaga saqlandi !")
        return redirect('bazaga_yuborildi')


class Milliy_Catalog(generic.CreateView):
    template_name = "milliy_katalog.html"
    queryset =  Anketa.objects.all()
    fields = "__all__"
    success_url = reverse_lazy('anketaview')

    def get(self, request, *args, **kwargs):
        all_anketa =  Anketa.objects.all().count()
        conf = Anketa.objects.all().filter(status_confirm=True).count()
        cancel =  Anketa.objects.all().filter(status_cancel=True).count()
        see =  conf + cancel

        bazada_mavjud_emas =  Anketa.objects.filter(baza_save=True)
        if bazada_mavjud_emas:
            bazada_mavjud_emas.delete()

        anketa = Anketa.objects.all().filter(status_confirm=True)
   

        context = {
            
            'anketa':anketa,
            'all_anketa':all_anketa,
            'conf':conf,
            'cancel':cancel,
            'see':see,
            'mess':mess1,

        }
        # mess1.remove('Bazaga saqlandi !')
        return render(request,'milliy_katalog.html', context)


    def post(self,request, *args, **kwargs):
        mess1.clear()
        anketa  =  Anketa.objects.all()
        form = request.POST
        for i in anketa:
            bazada_mavjud_emas =  Anketa.objects.filter(baza_save=True)
            if bazada_mavjud_emas:
                bazada_mavjud_emas.delete()
            if i.pin == form["pnfil"]:
                bazada_mavjud_emas =  Anketa.objects.filter(baza_save=True)
                if bazada_mavjud_emas:
                    bazada_mavjud_emas.delete()
                message =  "Sizning ma'lumotlaringiz bazada mavjud ikkinchi marta topshirish uchun admin bilan bo'glaning "
                all_anketa =  Anketa.objects.all().count()
                conf = Anketa.objects.all().filter(status_confirm=True).count()
                cancel =  Anketa.objects.all().filter(status_cancel=True).count()
                see =  conf + cancel

                

                anketa = Anketa.objects.all().filter(status_confirm=True)
        

                context = {
                    
                    'anketa':anketa,
                    'all_anketa':all_anketa,
                    'conf':conf,
                    'cancel':cancel,
                    'see':see,
                    'message':message,

                }
                # mess1.remove('Bazaga saqlandi !')
                return render(request,'milliy_katalog.html', context)

        link = f'https://hunar.uz/api/getRegistryIndividual?pinfl={form["pnfil"]}&passportSerial=AB123'
        response = requests.get(link)
        
        if response.status_code == 200:

            response = urlopen(link)
            content = response.read()
            json_object = json.loads(content.decode('utf-8'))
            data = json_object['body']
            print(data)
            anketa = Anketa.objects.create(
                tin=data['tin'],
                pin=data['pin'],
                # ctzn=form["O'zbekiston"],
                pport_no=data['pport_no'],
            
                fist_name=data['first_name'],
                mid_name=data['mid_name'],
                sur_name=data['sur_name'],
                email=data['email'],

                phone=data['telefon'],
         
                guvohnoma=data['guvohnoma'],
                guvohnoma_start_date=data['guvohnoma_start_date'][:10],
                guvohnoma_end_date=data['guvohnoma_end_date'][:10],
                memberyear=data['memberyear'][:10],
                yashash_manzili=data['yashash_manzili'],
                viloyati=data['viloyati'],
                tumani=data['tumani'],
                mahalla=data['mahalla'],
                fl_address_U=data['home_mahalla'],
                fl_address_V=data['home_viloyati'],
                fl_address_T=data['home_tumani'],
                job=data['asosy_faoliyat_turi'],
                ish_manzili=data['ish_manzili'],

            )

            return redirect('anketaview', anketa.pk)
        else:

            message =  "Sizning ma'lumotlaringiz Hunar.uz saytida  topilmadi siz hunar.uz saytidan ro'yhatdan o'ting "
            all_anketa =  Anketa.objects.all().count()
            conf = Anketa.objects.all().filter(status_confirm=True).count()
            cancel =  Anketa.objects.all().filter(status_cancel=True).count()
            see =  conf + cancel

            

            anketa = Anketa.objects.all().filter(status_confirm=True)
    

            context = {
                
                'anketa':anketa,
                'all_anketa':all_anketa,
                'conf':conf,
                'cancel':cancel,
                'see':see,
                'message':message,

            }
            # mess1.remove('Bazaga saqlandi !')
            return render(request,'milliy_katalog.html', context)
def home(request):


    return render(request, 'home.html')


def milliy_catalog(request):
    page_obj = Anketa.objects.all()
    pnifl =  request.POST.get('pnfil')
    # pasport = request.POST.get("pasport")
    message = ""
    if pnifl:
        url = f"https://hunar.uz/api/getRegistryIndividual?pinfl={pnifl}&passportSerial=AB123"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            first_name = data['body']['first_name']
            # return HttpResponse(json.dumps(data), content_type='application/json')
            content = {
                "first_name":first_name,
            }
            return render(request, 'online_ariza.html', content)
        
        else:
            message = "Ma'lumotlar Topilmadi "
        print(response)
    else:
        message = "Maydon bo'sh"
    content = {
        'page_obj':page_obj,
        "message":message,

    }
    return render(request, 'milliy_katalog.html', content)



def online_ariza(request):
    return render(request, 'online_ariza.html')


def table(request):
    return render(request, 'table.html')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

@csrf_exempt
def delete_anketa_file(request, id):
    if request.method == "POST":
        try:
            image = Anketa_File.objects.get(id=id)
            image.delete()
            return JsonResponse({'message': 'Image deleted successfully.'})
        except ObjectDoesNotExist:
            return JsonResponse({'message': 'Image not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Invalid request method.'}, status=400)


    
from django.db.models import Q
from django.contrib.auth.decorators import login_required
class KengashView(generic.CreateView):
    queryset = Anketa.objects.all()
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
    
        if request.user.is_authenticated:
            print(request.user)

                


            anketa = Anketa.objects.filter(status_new=True, excel_malumot=False).exclude(Q(likes=request.user) | Q(dislikes=request.user))
            print(anketa)
            # anketa = Anketa.objects.filter(status_new=True,excel_malumot=False, likes=request.user, dislikes=request.user)
            print(request.user.username)
            context = {
                'anketa':anketa,
             
            }
            print(anketa)
            return render(request, 'kengash.html', context)
        else:
            return redirect("login")
    
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
       
            anketa =  Anketa.objects.get(id=request.POST.get("pID"))
            if request.GET.get('like') == 'yes':
                anketa.likes.add(User.objects.get(id=request.user.pk))
                anketa.add_like(User.objects.get(id=request.user.pk))
                anketa.remove_dislike(User.objects.get(id=request.user.pk))
                anketa.dislikes.remove(User.objects.get(id=request.user.pk))
               
                anketa.status_Progress()
                anketa.save()
                return redirect("canceled")


            elif request.GET.get('like') == 'no':
                anketa.dislikes.add(User.objects.get(id=request.user.pk))
                anketa.add_dislike(User.objects.get(id=request.user.pk))
                anketa.remove_like(User.objects.get(id=request.user.pk))
                anketa.likes.remove(User.objects.get(id=request.user.pk))
                anketa.status_Progress()
               
                text = request.POST.get("comment_text")
                print(text)
                comment =  Customer_Comment.objects.create(
                        anketa = anketa,
                        user = User.objects.get(id=request.user.pk),
                        
                        text = request.POST.get("comment_text")
                    )
                comment.save()
                anketa.save()
                return redirect("confirmation")
                


        return redirect("kengash")
    
class ConfirmationView(generic.CreateView):
    queryset =  Anketa.objects.all()
    permission_classes = [IsAuthenticated]
    template_name = 'confirmation.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            like = Anketa.objects.filter(likes=request.user)
            context = {
                'like':like,
            }
            return render(request, 'confirmation.html', context)
        else:
            return redirect("login")
    

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            anketa = Anketa.objects.get(id=request.GET.get('id'))
            anketa.likes.add(User.objects.get(id=request.user.pk))
            anketa.save()
        return redirect("kengash")
    

class CanceledView(generic.CreateView):
    queryset = Anketa.objects.all()
    permission_classes = [IsAuthenticated]
    template_name = 'canceled.html'


    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            dislikes = Anketa.objects.filter(dislikes=request.user)
            print(dislikes)
            context = {
                'dislikes':dislikes
            }
            return render(request, 'canceled.html', context)
        else:
            return redirect("login")
    


    def post(self, request, *args, **kwargs):
        anketa = Anketa.objects.get(id=request.GET.get('id'))
        
        anketa.dislikes.add(User.objects.get(id=request.user.pk))
        anketa.save()

        return redirect("kengash")






class TasdiqlashDetailView(generic.CreateView):

    def get(self, request, *args, **kwargs):
        anketa = Anketa.objects.get(id=self.kwargs['id'])
        anketa1 =  Anketa.objects.filter(id=anketa.id, status_confirm=True)
        anketa_file = Anketa_File.objects.filter(anketa=anketa)
        anketa_image_profile = Anketa_Profile_Image.objects.filter(anketa=anketa)
        if anketa_image_profile:
            anketa_image_profile = Anketa_Profile_Image.objects.filter(anketa=anketa).latest("id")
       
        context = {
            'anketa1':anketa1,
            'anketa':anketa,
            'anketa_file':anketa_file,
            'anketa_image_profile' :anketa_image_profile
        }
        return render(request, 'ariza_detail.html', context)
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed

class Anketa_data_Json_View(APIView):

    def get(self, request):
        try:
            # # Extract token from the Authorization header
            # authorization_header = request.headers.get('Authorization')
            # if not authorization_header or not authorization_header.startswith('Bearer '):
            #     raise AuthenticationFailed('Token mavjud emas !!!!!')

            # token = authorization_header.split(' ')[1]

            # Your logic to fetch and serialize data
            data = Anketa.objects.all()
            serializer = Anketa_Serializers(data, many=True)

        
            return Response(serializer.data, status=status.HTTP_200_OK)

        except AuthenticationFailed as e:
            return Response({'error': 'Token authentication failed', 'detail': str(e)},
                            status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def anketa_json(request):

    # Agar token tekshirilgan bo'lsa, malumotlarni olish
    anketa = Anketa.objects.filter(status_confirm=True).values()
    data = []

    for i in anketa:
        data.append(i)
        data.append(f"http://31.129.104.246/ariza_detail/{i['id']}/")

    return JsonResponse(data, safe=False)




def delate_pdf(path):
    print("keldi")


from django.http import FileResponse
from django.shortcuts import render
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
import tempfile
import os
import qrcode
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

def generate_certificate_pdf(request, ids):
    anketa = Anketa.objects.filter(pin=ids,status_confirm=True)
    mess1.clear()
    if anketa:
        
        for i in anketa:
            guvohnoma_sana =i.guvohnoma_end_date
            today = datetime.date.today()
            if guvohnoma_sana:
                if len(guvohnoma_sana) < 15:
                    date = datetime.datetime.strptime(guvohnoma_sana, "%Y-%m-%d").date()
                    print(date)
                else:
                    date = datetime.datetime.strptime(guvohnoma_sana, "%Y-%m-%d  %H:%M:%S.%f").date()
                    print(date)
                    

                if date < today:
                    
                    message = "Amal qilish muddati tugagan"

                    context = {
                        'message':message,
                        
                      
                    }
                    return render(request,'wait_not_faund.html', context)
            if i.guvohnoma:


        

                image_path = str(BASE_DIR.joinpath('static/sertifikat.jpg')) # Rasm faylning yo'li
                image = Image.open(image_path)
            
                print(request.META['PATH_INFO'])
                # Matnni yozish uchun matn, rang va fontni sozlash
                for i in anketa:
                    if i.guvohnoma:

                        NOMER_ID = f': {i.guvohnoma}'
                    else:
                        NOMER_ID=""
                    if i.fist_name and i.mid_name and i.sur_name:
                        FISH = f"{i.fist_name} {i.sur_name} {i.mid_name} "
                    else:
                        FISH =""
                    if i.pin:
                        STIR = f"JSHSHR/ПИНФЛ/PINFL: {i.pin}"
                    else:
                        STIR = ""

                    PASSPORT = i.pport_no
                    GUVOHNOMA_start = f'{i.guvohnoma_start_date}'

                    UY_MANZIL = f"{i.viloyati}, {i.tumani},  {i.yashash_manzili}"
                    if i.fl_address_T:
                        tuman = i.fl_address_T
                    else:
                        tuman = ""
                    if i.fl_address_U:
                        uy = i.fl_address_U
                    else:
                        uy = ""
                    if i.fl_address_V:
                        viloyat = i.fl_address_V
                    else:
                        viloyat = ""
                    FAOLIYAT_MANZIL = f"{viloyat} {tuman}"
                    if i.job:

                        JOB = i.job
                    else:
                        JOB = ""
                    GUVOHNOMA_end = f'{i.guvohnoma_end_date}'
                    
                    text = f"http://31.129.104.246/generate_certificate_pdf/{i.pin}"

                text_color = (0,0,0)  # Qora rang (RGB formatida)
                font_size = 24
                font_size1 = 30
                font_size3 = 35
                font_size2 = 50 
                arial_path = str(BASE_DIR.joinpath('static/arial.ttf')) 
                font = ImageFont.truetype( arial_path, font_size)  # Matn fonti
                font1 = ImageFont.truetype(arial_path, font_size1)
                font2 = ImageFont.truetype(arial_path, font_size2)
                font3 = ImageFont.truetype(arial_path, font_size3)
                # Rasmga matnni qo'shish
                draw = ImageDraw.Draw(image)
                draw.text((1100, 1330), NOMER_ID, fill=text_color, font=font2, stroke_width=1)
                draw.text((1220, 1700), FISH.upper(), fill=text_color, font=font2, stroke_width=1, anchor="mt")
                draw.text((780, 1850), STIR.upper(), fill=text_color, font=font2)
                # draw.text((325, 915), PASSPORT, fill=text_color, font=font, anchor="mt")
                draw.text((690, 2920), GUVOHNOMA_start, fill=text_color, font=font3)
                draw.text((1130, 2070), UY_MANZIL.upper(), fill=text_color, font=font3, anchor="mt")
                draw.text((1130, 2250), FAOLIYAT_MANZIL.upper(), fill=text_color, font=font3,anchor="mt" )
                draw.text((1210, 2400), JOB.upper(), fill=text_color, font=font3,anchor="mt" )
                draw.text((774, 3196), GUVOHNOMA_end, fill=text_color, font=font3,anchor="mt" )
                # Save the image to a temporary file
                
                temp_image_path = os.path.join(tempfile.gettempdir(),BASE_DIR,f'static/sertifikat/{ids}.jpg')
            
                qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=2,
            )
                
                qr.add_data(text)
                qr.make(fit=True)
                qr_img = qr.make_image(fill_color="black", back_color="white")
                image.paste(qr_img, (1550, 2930))
                
                

                pdf_path = os.path.join(tempfile.gettempdir(),BASE_DIR, f'static/sertifikat/{ids}.pdf')
                image.save(temp_image_path)

                

                # Rasmni PDF fayliga o'girish funksiyasi
                def convert_image_to_pdf(temp_image_path, pdf_path):
                    img = Image.open(temp_image_path)
                    img_width, img_height = img.size
                    
                    c = canvas.Canvas(pdf_path, pagesize=(img_width, img_height))
                    c.drawImage(temp_image_path, 0, 0, img_width, img_height)
                    c.save()
                    

                convert_image_to_pdf(temp_image_path, pdf_path)
                # Convert the image to PDF
                pdf_path = os.path.join(tempfile.gettempdir(),BASE_DIR, f'static/sertifikat/{ids}.pdf')

                ids = str(ids)
                context = {
                    'ids':ids
                }
                print(type(ids))
                return render(request, "sertifikat.html", context)
            else:
                message = "Guvuhnoma raqami mavjud emas qilish muddati tuggan"

                context = {
                        'message':message,
                        
                      
                    }
                return render(request,'wait_not_faund.html', context)

    else:

        message = "Bazada mavjud emas "

        context = {
                'message':message,
                }
        return render(request,'wait_not_faund.html', context)
import datetime
def sertifkat(request):
    mess1.clear()
    certificate_path = os.path.join(tempfile.gettempdir(),BASE_DIR, 'static/sertifikat')

    # Sertifikat papkasining ichidagi barcha fayllarni olish
    for file_name in os.listdir(certificate_path):
        file_path = os.path.join(certificate_path, file_name)
        # Faylni o'chirish
        if os.path.isfile(file_path):
            os.remove(file_path)
            print("OCHIRLDI")
    pinfl = request.POST.get("pnfil")
    link = f'https://hunar.uz/api/getRegistryIndividual?pinfl={pinfl}&passportSerial=AB123'
    response = requests.get(link)
    anketa = Anketa.objects.filter(pin=pinfl, status_confirm=True)    
    if response.status_code == 200:
        anketa = Anketa.objects.filter(pin=pinfl, status_confirm=True)
        progress = Anketa.objects.filter(pin=pinfl, status_progress=True)
        if progress:
                message = "Hali tasdiqlanmadi ko'rib chiqilmoqda !!!"
                

                context = {
                        'message':message,
                        
                      
                    }
                return render(request,'wait_not_faund.html', context)


        if anketa:

            response = urlopen(link)
            content = response.read()
            json_object = json.loads(content.decode('utf-8'))
            data = json_object['body']

            guvohnoma_sana =data['guvohnoma_end_date']
            today = datetime.date.today()
            if anketa:
                ids = 0
                if len(guvohnoma_sana) < 15:
                    date = datetime.datetime.strptime(guvohnoma_sana, "%d.%m.%Y").date()
                    print(data)
                else:
                    date = datetime.datetime.strptime(guvohnoma_sana, "%Y-%m-%d  %H:%M:%S.%f").date()
                    

                if date < today:
                    
                    message = "Amal qilish muddati tugagan"

                    context = {
                        'message':message,
                        
                      
                    }
                    return render(request,'wait_not_faund.html', context)



                else:
                    for i in anketa:
                        print(i.id)
                        ids=i.pin
                    return redirect('generate_certificate_pdf', ids)
        else:
            message = "Bazada mavjud emas"
           
            context = {
                        'message':message, 
                    }
            return render(request,'wait_not_faund.html', context)
    else:

        message = "Sizning malumotlarigiz Hunar.uz saytidan topilmadi!!!"

        context = {
            'message':message,
            }
        return render(request,'wait_not_faund.html', context)




def menejr(request):
    if request.user.is_authenticated:
        anketa = Anketa.objects.all()
        context = {
            'anketa':anketa
        } 
        return render(request, 'menejr.html', context)


    else:
        return redirect("login")











