from django.contrib import admin

# Register your models here.

from systemapp.models import (User, PhoneOTP , Courses, Genders, KPI, Percentage, 
                               TeacherDegrees, FunctionsTeacher, ModDegrees, ModBonuses, Employees, Employment, TeacherInheri, ModeratorInheri)
# list_display=('title','content','created_at','updated_at','photos','is_bool')
#     list_display_links=('title','content') #link qib beradi
    # search_fields=('title','content') # search qo'shib beradi
class UserAdmin(admin.ModelAdmin):
    ordering=['id']
    list_display=(
        ['phone']
    )
    search_fields=('phone','date') # search qo'shib beradi

admin.site.register(User,UserAdmin)
admin.site.register(PhoneOTP)
admin.site.register(Courses)
admin.site.register(Genders)
admin.site.register(KPI)
admin.site.register(Percentage)
admin.site.register(TeacherDegrees)
admin.site.register(Employment)
admin.site.register(ModDegrees)
admin.site.register(ModBonuses)
admin.site.register(Employees)
admin.site.register(TeacherInheri)
admin.site.register(ModeratorInheri)