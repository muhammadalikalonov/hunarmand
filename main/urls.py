from django.urls import path, include

from .views import (
        home, milliy_catalog, online_ariza,
        table, AnketaViews,Milliy_Catalog,
        KengashView, ConfirmationView,CanceledView,
        TasdiqlashDetailView,ArizaEdit,
        login_anketa, delete_anketa_file,
        anketa_file, anketa_json, anketa_image_profile, sertifkat, generate_certificate_pdf, menejr, logout_home,
        Anketa_ListAPIiew1, Anketa_data_Json_View, bazaga_yuborildi

)   
from .hunarmand_admin import home_admin, ball,Bekor_qilganlar, Kelgan_Ariza, Jarayonda,customer_delete, bekor_hammasi_ochirish,all_anketa,customer_status_edit, hunarmand_delate, Tasdiqlash
from .login_register import register, user_delete, change_user_password, Login_admin, logout_view
from .auth import auth_middleware, auth_middleware_admin


urlpatterns = [
    path('', Milliy_Catalog.as_view(), name="home"),
    path("milliy_catalog/", Milliy_Catalog.as_view() ,name="milliy_catolog"),
    path('login/', login_anketa, name="login"),
    path('milliy/', milliy_catalog, ),
    path('online_ariza/', online_ariza, name="online_ariza"), 
    path('table/', table, name="table"),
    # path("milliy_catalog/", Milliy_Catalog.as_view() ,name="milliy_catolog"),
    path("online/<int:id>/", AnketaViews.as_view(), name="anketaview"),
    path('ariza_edit/<int:id>/', ArizaEdit.as_view(), name="ariza_edit"),
    path('kengashma/', auth_middleware(KengashView.as_view()), name="kengash"),
    path('confirmation/', auth_middleware(ConfirmationView.as_view()), name="confirmation"),
    path('canceled/', auth_middleware(CanceledView.as_view()), name="canceled"),
    path('ariza_detail/<int:id>/', TasdiqlashDetailView.as_view(), name="ariza_detail"),
    path("delete_anketa_file/<int:id>", delete_anketa_file, name="delete_anketa_file"),
    path("anketa_file/<int:pk>/", anketa_file, name="anketa_file"),
    path("anketa_data_json/", anketa_json, name="anketa_json"),
    path("anketa_image_profile/<int:pk>/", anketa_image_profile, name="anketa_image_profile"),
    path('sertifkat/', sertifkat, name="sertifkat"),
    path("generate_certificate_pdf/<int:ids>", generate_certificate_pdf, name="generate_certificate_pdf"),
    path('menejr/', auth_middleware(menejr), name="menejr"),
    path('logout_home',logout_home, name="logout_home"),
    path('bazaga_yuborildi/',bazaga_yuborildi, name="bazaga_yuborildi"),
    path('api_json_datas/',Anketa_data_Json_View.as_view(), name="Anketa_data_Json_View"),



    #########################################################################################
    ###############################  Admin  ##################################################
    path("home_admin/",home_admin, name="home_admin"),
    path('hakam_ball/',  auth_middleware_admin(ball),  name="ball"),
    path("kelgan_ariza/", auth_middleware_admin(Kelgan_Ariza.as_view()), name="kelgan_ariza"),
    path("jarayonda/", auth_middleware_admin(Jarayonda.as_view()), name="kutilmoqda"),
    path('all_anketa/', auth_middleware_admin(all_anketa), name="all_anketa"),
    path('customer_status_edit/<int:id>/', customer_status_edit, name="customer_status_edit"),
    path('customer_delete/<int:id>/', customer_delete, name="customer_delete"),
    path('hunarmand_delate/<int:id>/',hunarmand_delate, name="hunarmand_delate"),
    path('confirmation_admin/', auth_middleware_admin(Tasdiqlash.as_view()), name="conf"),
    path('cancel_admin/', auth_middleware_admin(Bekor_qilganlar.as_view()), name="cancel"),
    path('bekor_hammasi_ochirish/', auth_middleware_admin(bekor_hammasi_ochirish), name="bekor_hammasi_ochirish"),

    

    #############################################################################################
    ########################### LOGIN AND REGISTER ##############################################
    path("Register/", register, name="Register"), 
 
    path("user_delete/<int:id>/", user_delete, name="user_delete"),
    path('change_user_password/<int:id>/',change_user_password, name="change_user_password"),
    path('Login_admin/', Login_admin, name="Login_admin"),
    path('logout/',auth_middleware_admin(logout_view), name="logout" ),


#################################  API ###################################################
   
  
    path('pinfl/<int:pin>/',Anketa_ListAPIiew1.as_view(),name="api_j")


  


]



