from rest_framework import serializers
from django.forms import ValidationError
from  systemapp.models import (User, PhoneOTP, Courses, Group,Genders, KPI, Percentage, 
                               TeacherDegrees, FunctionsTeacher, ModDegrees, ModBonuses,Employment, Employees, TeacherInheri, ModeratorInheri)
from django.contrib.auth.models import Group, Permission


class CoursesSerializers(serializers.ModelSerializer):
    class Meta:
        model=Courses
        fields=('id','course_name')


class ValidatePhoneSendOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneOTP
        fields = ('full_name','phone','course_id')

class ValidateOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneOTP
        fields = ('phone', 'otp',)

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('phone','password')
        extra_kwargs={'password':{'write_only':True}}

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','phone')

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Permission
        fields=('name','content_type','codename')

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model=Group
        fields=('name','permissions')



#settings:

class GendersSerializer(serializers.ModelSerializer):
    class Meta:
        model=Genders
        fields=('id','gender_type')

class KPISerializer(serializers.ModelSerializer):
    class Meta:
        model=KPI
        fields=('id','amount_one','amount_two')

class PercentageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Percentage
        fields=('id','name','percentage')

class TeacherDegreesSerializer(serializers.ModelSerializer):
    class Meta:
        model=TeacherDegrees
        fields=('id','level','full_time','part_time')

class FunctionsTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model=FunctionsTeacher
        fields=('id','salary','course','level')

class ModDegreesSerializer(serializers.ModelSerializer):
    class Meta:
        model=ModDegrees
        fields=('id','level','full_time','part_time')

class ModBonusesSerializer(serializers.ModelSerializer):
    class Meta:
        model=ModBonuses
        fields=('id','amount_one','amount_two','amount_three')

class EmploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Employment
        fields=('id','full_time','part_time')

class EmployeesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Employees
        fields=('id','first_name','last_name','phone_num','email','gender','birth_date','salary','function','role','photo','user_id')




class TeacherInheriSerializer(serializers.ModelSerializer):
    class Meta:
        model=TeacherInheri
        fields=('id','first_name','last_name','phone_num','email','gender','birth_date','employee_salary','salary','course','level','role','photo','user_id')

class ModeratorInheriSerializer(serializers.ModelSerializer):
    class Meta:
        model=ModeratorInheri
        fields=('id','first_name','last_name','phone_num','email','gender','birth_date','employee_salary','level','employment','role','photo','user_id')