from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid
import os

################# PAPAKA O"CHIRISH ####################
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import shutil

####################################################





INFORMATION =  (
    ("Oliy", "Oliy"),
    ("To'liqsiz oliy", "To'liqsiz oliy"),
    ("O'rta maxsus, kasb-hunar", "O'rta maxsus, kasb-hunar"),
    ("Ummiy o'rta", "Ummiy o'rta"),
    ("To'liqsiz o'rta", "To'liqsiz o'rta"),
    ("Ma'lumotsiz", "Ma'lumotsiz"),
)


STATE =(
        ("O'zbekiston", "O'zbekiston"),
        ("Avg'oniston", "Avg'oniston"),
        ("Eron", "Eron"),
        ("Ozarbayjon", "Ozarbayjon"),
        ("Qirg'iziston", "Qirg'iziston"),
        ("Qozog'iston","Qozog'iston"),
        ("Rossiya","Rossiya"),
        ("Tojikiston","Tojikiston"),
        ("Turkiya","Turkiya"),
        ("Turkmaniston","Turkmaniston"),

    )

JOB = (

        ("Bosh kiyimlar tayyorlash", "Bosh kiyimlar tayyorlash"),
        ("Charm mahsulotlari", "Charm mahsulotlari"),
        ("Chinni, fayans va sopol buyumlari", "Chinni, fayans va sopol buyumlari"),
        ("Emallash ishlari", "Emallash ishlari"),
        ("Esdalik buyumlari", "Esdalik buyumlari"),
        ("Ganch o'ymakorligi", "Ganch o'ymakorligi"),
        ("Gul bosilgan gazlamalar va chokli buyumlar","Gul bosilgan gazlamalar va chokli buyumlar"),
        ("Hajmli va shaklli qoliplarda quyilgan buyumla", "Hajmli va shaklli qoliplarda quyilgan buyumlar"),
        ("Kandakorlik, misgarlik buyumlari", "Kandakorlik, misgarlik buyumlari"),
        ("Kashtachilik", "Kashtachilik"),
        ("Ko'zgu tayyorlash", "Ko'zgu tayyorlash"),
        ("Mayda haykaltaroshlik buyumlari", "Mayda haykaltaroshlik buyumlari"),
        ("Metalldan yasalgan buyumlar", "Metalldan yasalgan buyumlar"),
        ("Milliy liboslar tayyorlash", "Milliy liboslar tayyorlash"),
        ("Milliy poyabzal tayyorlash", "Milliy poyabzal tayyorlash"),
        ("Miniatyura, rang tasvir, naqqoshlik va bo'yoqli naqshlar", "Miniatyura, rang tasvir, naqqoshlik va bo'yoqli naqshlar"),
        ("Mozaika ishlari", "Mozaika ishlari"),
        ("Mualliflik mebellarini tayyorlash", "Mualliflik mebellarini tayyorlash"),
        ("Musiqa asboblari", "Musiqa asboblari"),
        ("Novdalardan buyumlar to'qish", "Novdalardan buyumlar to'qish"),
        ("O'yinchoqla", "O'yinchoqlar"),
        ("Oddiy metalldan milliy uslubda tayyorlangan taqinchoqlar", "Oddiy metalldan milliy uslubda tayyorlangan taqinchoqlar"),
        ("Pechka va kaminlar yasash","Pechka va kaminlar yasash"),
        ("Qimmatbaho metalldan yasalgan zargarlik buyumlari", "Qimmatbaho metalldan yasalgan zargarlik buyumlari"),
        ("Qo'lda gazlamalar to'qish", "Qo'lda gazlamalar to'qish"),
        ("Qo'lda gilam to'qish","Qo'lda gilam to'qish"),
        ("Shisha puflash ishlari", "Shisha puflash ishlari"),
        ("Soatsozlik", "Soatsozlik"),
        ("Suyakka o'yma naqsh solish", "Suyakka o'yma naqsh solish"),
        ("Tosh o'ymakorligi", "Tosh o'ymakorligi"),
        ("Tunukadan yasalgan buyumlar", "Tunukadan yasalgan buyumlar"),
        ("Yog'och o'ymakorligi", "Yog'och o'ymakorligi"),
        ( "Yog'ochdan tayyorlangan xalq hunarmandchiligi mahsulotlari", "Yog'ochdan tayyorlangan xalq hunarmandchiligi mahsulotlari",),
        ( "Zardo'zlik buyumlari", "Zardo'zlik buyumlari"),

    )
GRIFT = (

        ( "Tavsiyanoma", "Tavsiyanoma"),
        ( "Xalq ustasi", "Xalq ustasi"),
        ( "Xalqaro ko‘rgazma, ko‘rik tanlov, festival g‘olibi yoki laurеati", "Xalqaro ko‘rgazma, ko‘rik tanlov, festival g‘olibi yoki laurеati"),
    )


LIKE = (
        ('none', 'none'),
        ('like', 'like'),
        ('dislike', 'dislike')
    )

#################################################################################################################
class User(AbstractUser):
    STATUS = (
        ('hakam', "hakam"),
        ('admin', "admin"),
        ('menejer', "menejer"),
    )

    status=models.CharField(max_length=50,blank=True,null=True, choices=STATUS)


    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

############################################################################################################################

def upload_to(instance, filename):
    now = timezone.now()
    path = '{}/{}/{}'.format(now.year,now.month, filename)
    return path


from django.core.exceptions import ValidationError


###################################################################################################################
class Anketa(models.Model):
    fist_name =  models.CharField(max_length=200, blank=True, null=True)
    sur_name =  models.CharField(max_length=200, blank=True, null=True)
    mid_name  =  models.CharField(max_length=200, blank=True, null=True)
    birthday =  models.CharField(max_length=200, blank=True, null=True)
    millati = models.CharField(max_length=200, blank=True, null=True)
    pport_no = models.CharField(max_length=20, blank=True, null=True)
    pport_file = models.FileField(blank=True, null=True, upload_to=upload_to)
    information  = models.CharField(max_length=200, choices=INFORMATION, blank=True, null=True)#malumotingiz
    guvohnoma =  models.CharField(max_length=15, blank=True, null=True)
    guvohnoma_file =  models.FileField(blank=True, null=True, upload_to=upload_to)
    guvohnoma_start_date = models.CharField(max_length=55, blank=True, null=True)
    guvohnoma_end_date = models.CharField(max_length=55, blank=True, null=True)
    tin = models.CharField(max_length=200, blank=True, null=True)
    pin = models.CharField(max_length=200, blank=True, null=True)
    yashash_manzili = models.CharField(max_length=400, blank=True, null=True)
    viloyati =  models.CharField(max_length=400, blank=True, null=True)
    tumani = models.CharField(max_length=400, blank=True, null=True) 
    mahalla =  models.CharField(max_length=400, blank=True, null=True) 
    fl_address_V =  models.CharField(max_length=400, blank=True, null=True) 
    fl_address_T =  models.CharField(max_length=400, blank=True, null=True) 
    fl_address_U =  models.CharField(max_length=400, blank=True, null=True) 
    phone =  models.CharField(max_length=20, blank=True, null=True)
    email =  models.EmailField(blank=True, null=True)
    ish_manzili = models.CharField(max_length=400, blank=True, null=True) 
    ctzn  =  models.CharField(max_length=200, choices=STATE, blank=True, null=True)
    memberyear =  models.CharField(max_length=200, blank=True, null=True) #Uyushmaga birinchi marta a'zo bolgan yili\
    job =  models.CharField(max_length=200, choices=JOB, blank=True, null=True)  # Faoliyat turi
    additional_activity_type =  models.CharField(max_length=400, blank=True, null=True) 
    image_url  =  models.TextField(blank=True, null=True)
    web_site =  models.CharField(max_length=299, blank=True, null=True)
    number_of_students =  models.IntegerField(blank=True, null=True)
    girft =  models.CharField(max_length=300, choices=GRIFT, blank=True, null=True) #QAY BIRIGA EGASIZ 
    state_award  =  models.CharField(max_length=400, blank=True, null=True) #Davlat mukofati
    yurtmizda_tadbir  = models.TextField(blank=True, null=True) #yURTIMIZDA O'TKAZILGAN KO'RGAZMA TANLOVLARI
    xorjiy_tadbir =  models.TextField(blank=True, null=True) # Xorijiy davlatlarda O'tkazilgan korgazma-tanlovlar 
    personal_event =  models.TextField(blank=True, null=True) #Shaxsiy korgazmalar 
    creativity = models.TextField(blank=True, null=True)  # Ijodning o'ziga xosligi 
    manufactured_product =  models.TextField(blank=True, null=True)# Ishlab chiqargan mahsulot turlari va nomlari 
    additional_Information =  models.TextField(null=True, blank=True) #Qo'shimcha malumotlar 
    like  =  models.CharField(max_length=12, choices=LIKE, blank=True, null=True)
    like_number =  models.IntegerField(default=0, blank=True, null=True)
    dislike_number = models.IntegerField(default=0, blank=True, null=True)
    likes =  models.ManyToManyField(User,   related_name="like_user", blank=True)
    dislikes =  models.ManyToManyField(User,   related_name="dislike_user", blank=True)
    status_new = models.BooleanField(default=True)
    status_progress =  models.BooleanField(default=False)
    status_confirm =  models.BooleanField(default=False)
    status_cancel =  models.BooleanField(default=False)
    excel_malumot = models.BooleanField(default=False, blank=True, null=True)
    date1 = models.DateTimeField(auto_now=True)
    tasdiqlangan_data =  models.DateField(null=True, blank=True, auto_now=False)
    baza_save = models.BooleanField(default=True, verbose_name="Baza saqlash yoki saqlanmaslik", null=True, blank=True)



    general_shutdown  =  models.BooleanField(default=False) # Agar hunarmandlar saytdan ham o'chsa bu yerda ham o'chirish
    archive  =  models.BooleanField(default=False)  # Puli tugagan vaqt o'chirish
    def anketa_list(self):
        print(self.like_number)
        if self.like_number > self.dislike_number:
           
            print("sssss")
            self.save()
        else:
            self.excel_malumot = False
            self.save()


    def update_like_number(self):
        self.like_number = self.likes.count()
        self.save()

    def update_dislike_number(self):
        self.dislike_number = self.dislikes.count()
        self.save()

    def add_like(self, user):
        self.likes.add(user)
        self.update_like_number()

    def remove_like(self, user):
        self.likes.remove(user)
        self.update_like_number()

    def add_dislike(self, user):
        self.dislikes.add(user)
        self.update_dislike_number()

    def remove_dislike(self, user):
        self.dislikes.remove(user)
        self.update_dislike_number()
    
    def status_Progress(self):
        self.status_progress = True
        self.save()
    

def validate_unique_file(instance):
    # Bu funktsiya berilgan Fayl obyektning ma'lumotlar bazasida mavjud bo'lip bo'lmaganini tekshiradi.
    # Agar bu Fayl nomi bilan bitta Fayl obyekt topilsa, ValidationError chiqadi.
    if Anketa_File.objects.filter(file=instance.file).exclude(pk=instance.pk).exists():
        print("mavjud")



class Anketa_File(models.Model):
    anketa  =  models.ForeignKey(Anketa, on_delete=models.CASCADE)
    file  =  models.FileField(upload_to=upload_to, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Fayl nomini bazada tekshirish
        existing_files = Anketa_File.objects.filter(file=self.file.name)
        if self.pk:
            existing_files = existing_files.exclude(pk=self.pk)

        if existing_files.exists():
            raise ValidationError("Bu nomdagi fayl mavjud. Iltimos, boshqa nom kiriting.")

        super(Anketa_File, self).save(*args, **kwargs)

    def __str__(self):
        return "2023-" + self.anketa.fist_name + "_" + self.anketa.sur_name

class Anketa_Profile_Image(models.Model):
    anketa = models.ForeignKey(Anketa, on_delete=models.CASCADE)
    image_profile = models.ImageField(upload_to=upload_to, blank=True, null=True)
    
    def __str__(self):
        return "2023-" + self.anketa.fist_name + "_" + self.anketa.sur_name
    

@receiver(pre_delete, sender=Anketa)
def delete_file(sender, instance, **kwargs):
    if instance.pport_file:
        file_path = instance.pport_file.path
        if os.path.exists(file_path):
            folder_path = os.path.dirname(file_path)
            shutil.rmtree(folder_path)  

@receiver(pre_delete, sender=Anketa_File, )
def delete_file(sender, instance, **kwargs):
    if instance.file:

        file_path = instance.file.path
        if os.path.exists(file_path):
            os.remove(file_path)







class Ball(models.Model):
    ball = models.IntegerField(default=3)

    def __str__(self):
        return str(self.ball)




class Customer_Comment(models.Model):
    anketa =  models.ForeignKey(Anketa, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text  =  models.TextField()

class Customer_Support(models.Model):
    username  = models.CharField(max_length=200)
    password = models.CharField(max_length=200)



    def __str__(self) -> str:
        return self.username







class Support_Chat(models.Model):
    text =  models.TextField()
    date =  models.DateTimeField(auto_now_add=True)
    customer =  models.ForeignKey(Customer_Support, on_delete=models.SET_NULL, null=True)




































