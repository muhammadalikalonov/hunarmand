from django.contrib import admin

from .models import Anketa, User, Anketa_File, Anketa_Profile_Image, Ball, Customer_Comment

from import_export.admin import ImportExportModelAdmin

from django.contrib.auth.admin import UserAdmin




class AnketaImportAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['id', 'fist_name', 'sur_name', 'mid_name', 'status_new', ]
    list_filter = ['like_number', 'dislike_number', 'status_cancel']
    list_display = ['id', 'fist_name', 'sur_name', 'mid_name', 'status_new', 'like_number', 'dislike_number']
    #list_per_page = 15


admin.site.register(Anketa, AnketaImportAdmin)


admin.site.register(User, UserAdmin)
admin.site.register(Anketa_File)
admin.site.register(Anketa_Profile_Image)
admin.site.register(Ball)

admin.site.register(Customer_Comment)

