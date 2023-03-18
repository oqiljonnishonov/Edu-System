from django.shortcuts import render

from django.shortcuts import render
from django.http import Http404
from rest_framework import status
# status.HTTP_400_BAD_REQUEST
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from drf_yasg.utils import swagger_auto_schema
import random
from rest_framework.views import APIView
from rest_framework.response import Response

from systemapp.models import (User, PhoneOTP, Courses)
from systemapp.serializers import (ValidatePhoneSendOTPSerializer, ValidateOTPSerializer, CreateUserSerializer, 
                                  UserSerializer, CoursesSerializers)

import requests


from django.contrib.auth.models import Group, Permission
from systemapp.serializers import PermissionSerializer, GroupSerializer
from django.contrib.contenttypes.models import ContentType
from systemapp.models import (Genders, KPI, Percentage, 
                               TeacherDegrees, FunctionsTeacher, ModDegrees, ModBonuses, Employees, TeacherInheri, ModeratorInheri, Employment)
from systemapp.serializers import (GendersSerializer, KPISerializer, PercentageSerializer, TeacherDegreesSerializer, FunctionsTeacherSerializer, 
                                   ModDegreesSerializer, ModBonusesSerializer, EmployeesSerializer, TeacherInheriSerializer, ModeratorInheriSerializer,
                                   EmploymentSerializer)
from django.contrib.auth.decorators import permission_required

from systemapp.permissions import HasGroupPermission , is_in_group
# Create your views here.

class CoursesAPIView(APIView):
    serializer_class=CoursesSerializers
    permission_classes=(IsAdminUser,)
    @swagger_auto_schema(request_body=CoursesSerializers)
    def post(self,request):
        serializer=CoursesSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response('Cant posted !')
        
    def get(self,request):
        actors=Courses.objects.all()
        serializer=CoursesSerializers(actors,many=True)
        return Response(data=serializer.data)


#Auth: for ansor foreign human:
class ValidatePhoneSendOTP(APIView):
    serializer_class=ValidatePhoneSendOTPSerializer
    permission_classes=(AllowAny,)
    
    @swagger_auto_schema(request_body=ValidatePhoneSendOTPSerializer)
    def post(self,request):
        phone_number=request.data.get('phone')
        full_name=request.data.get('full_name')
        course=request.data.get('course')
        
        if phone_number and full_name and course:
            phone=str(phone_number)
            user=User.objects.filter(phone__iexact=phone)
            if user.exists():
                return Response(
                    {
                        'status':False,
                        'detail':'this phone number already exist !',
                    }
                )
            else:
                key=send_otp(phone)
                if key:
                    old=PhoneOTP.objects.filter(phone__iexact=phone)
                    if old.exists():
                        old.first()
                    serializer=ValidatePhoneSendOTPSerializer(data=request.data)
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                    ootp= PhoneOTP.objects.get(phone__iexact=phone)
                    ootp.otp=key
                    ootp.save()
	
                    # PhoneOTP.objects.create(phone=phone,otp=key ,full_name=full_name , course=course )
                    
                    return Response(
                        {
                            'status':True,
                            'detail':'OTP sent successfully !',
                        }
                    )
                else:
                    return Response(
                        {
                            'status':False,
                            'detail':'sending otp error !',
                        }
                    )
        else:
            return Response(
                {
                    'status':False,
                    'detail':'phone number is not given post request !'
                }
            )



def send_otp(phone):
    if phone:
        key = random.randint(99999, 999999)
        print(key)
        return key
    else:
        return False


class ValidateOTP(APIView):
    serializer_class=ValidateOTPSerializer
    permission_classes=(AllowAny,)

    @swagger_auto_schema(request_body=ValidateOTPSerializer)
    def post(self,request):
        phone=request.data.get('phone',False)
        otp_send=request.data.get('otp',False)
        
        if phone and otp_send:
            old=PhoneOTP.objects.filter(phone__iexact=phone)
            if old.exists():
                old=old.first()
                otp=old.otp
                if str(otp_send)==str(otp):
                    full_name=old.full_name
                    phone_num=old.phone
                    subject=old.course_id
                    
                    bot_token='6066491939:AAEDBrclIjq88En5z-Vzy33IHCwjl6xOEsM'
                    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                    message_data=f"New Applicant:\n{full_name}\n{phone_num}\n{subject}"
                    chat_id=1731117573
                    payload = {
                        "text": message_data,
                        "parse_mode": "HTML",
                        "disable_web_page_preview": False,
                        "disable_notification": False,
                        "reply_to_message_id": 0,
                        "chat_id": chat_id
                    }
                    headers = {
                        "accept": "application/json",
                        "User-Agent": "Telegram Bot SDK - (https://github.com/irazasyed/telegram-bot-sdk)",
                        "content-type": "application/json"
                    }
                    response = requests.post(url, json=payload, headers=headers)
                    print(response.text)
                    
                    old.validated=True
                    old.delete()
                    return Response(
                        {
                            'status':True,
                            'detail':'OTP matched. Please proceed for registration !',
                        }
                    )
                else:
                    return Response(
                        {
                            'status':False,
                            'detail':'OTP INCORRECT !',
                        }
                    )
            else:
                return Response(
                    {
                        'status':False,
                        'detail':'First proceed via sending otp request !',
                    }
                )
        else:
            return Response({
                'status': False,
                'detail': 'please provide both phone and OTP for validation !',
            })


# add students:

class Register(APIView):
    serializer_class=CreateUserSerializer
    permission_classes=(IsAdminUser,)
    
    @swagger_auto_schema(request_body=CreateUserSerializer)
    def post(self,request):
        phone=request.data.get('phone',False)
        password=request.data.get('password',False)
        username=request.data.get('username',False)
        if phone and password:
            # old=PhoneOTP.objects.filter(phone__iexact=phone)
            # if old.exists():
            #     old=old.first()
            #     validated=old.validated
            #     data=request.data
                # if validated:
            data=request.data
            reg_serializer=CreateUserSerializer(data=data)
            if reg_serializer.is_valid():
                password=reg_serializer.validated_data.get('password')
                reg_serializer.validated_data['password']=make_password(password)
                new_user=reg_serializer.save()
                # old.delete()
                return Response(
                    {
                        'status':True,
                        'detail':'Account successfuly created !'
                    }
                )
            else:
                return Response(
                    {
                        'status':False,
                        'detail':"OTP haven't verified .First do that step !"
                    }
                )
                        
        # else:
        #     return Response(
        #         {
        #             'status':False,
        #             'detail':'please verify phone first !',
        #         }
        #     )
        else:
            return Response(
                {
                    'status': False,
                    'datail': "Both Phone and password are not sent !",
                }
            )

# class PermissionAPIView(APIView):
    

class PermissionsGroupAPIView(APIView):
    serializer_class=GroupSerializer
    permission_classes=(AllowAny,)
    
    @swagger_auto_schema(request_body=GroupSerializer)
    def post(self,request):
        # name=request.data.get('name')
        serializer=GroupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save
            
            return Response(data=serializer.data)
        else:
            return Response('Cant posted !')
        
            # name=request.data.get('name')
            # new_group, created = Group.objects.get_or_create(name=name)
            
            # ct = ContentType.objects.get_for_model(User)
            # permission = Permission.objects.create(codename ='can_go_haridwar', name ='Can go to Haridwar', content_type = ct)
            
    def get(self,request):
        groups=Group.objects.all()
        serializer=GroupSerializer(groups,many=True)
        return Response(data=serializer.data)
    
    
    
    
    # @swagger_auto_schema(request_body=CoursesSerializers)
    # def post(self,request):
    #     serializer=CoursesSerializers(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #         return Response(data=serializer.data)
    #     else:
    #         return Response('Cant posted !')
        
    # def get(self,request):
    #     courses=Courses.objects.all()
    #     serializer=CoursesSerializers(courses,many=True)
    #     return Response(data=serializer.data)



#settings:

class GendersAPIView(APIView):
    serializer_class=GendersSerializer
    permission_classes=(IsAdminUser,)
    
    @swagger_auto_schema(request_body=GendersSerializer)
    def post(self,request):
        serializer=GendersSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response('Cant posted !')
        
    def get(self,request):
        genders=Genders.objects.all()
        serializer=GendersSerializer(genders,many=True)
        return Response(data=serializer.data)

class KPIsAPIView(APIView):
    serializer_class=KPISerializer
    permission_classes=(IsAdminUser,)
    
    @swagger_auto_schema(request_body=KPISerializer)
    def post(self,request):
        serializer=KPISerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response('Cant posted !')
        
    def get(self,request):
        kpis=KPI.objects.all()
        serializer=KPISerializer(kpis,many=True)
        return Response(data=serializer.data)


class PercentageAPIView(APIView):
    serializer_class=PercentageSerializer
    permission_classes=(IsAdminUser,)
    
    @swagger_auto_schema(request_body=PercentageSerializer)
    def post(self,request):
        serializer=PercentageSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response('Cant posted !')
        
    def get(self,request):
        percentages=Percentage.objects.all()
        serializer=PercentageSerializer(percentages,many=True)
        return Response(data=serializer.data)

class TeacherDegreesAPIView(APIView):
    serializer_class=TeacherDegreesSerializer
    permission_classes=(IsAdminUser,)
    
    @swagger_auto_schema(request_body=TeacherDegreesSerializer)
    def post(self,request):
        serializer=TeacherDegreesSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response('Cant posted !')
        
    def get(self,request):
        teacherdegrees=TeacherDegrees.objects.all()
        serializer=TeacherDegreesSerializer(teacherdegrees,many=True)
        return Response(data=serializer.data)

class FunctionsTeacherAPIView(APIView):
    serializer_class=FunctionsTeacherSerializer
    permission_classes=(IsAdminUser,)
    
    @swagger_auto_schema(request_body=FunctionsTeacherSerializer)
    def post(self,request):
        serializer=FunctionsTeacherSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response('Cant posted !')
        
    def get(self,request):
        functionsteacher=FunctionsTeacher.objects.all()
        serializer=FunctionsTeacherSerializer(functionsteacher,many=True)
        return Response(data=serializer.data)

class ModDegreesAPIView(APIView):
    serializer_class=ModDegreesSerializer
    permission_classes=(IsAdminUser,)
    
    @swagger_auto_schema(request_body=ModDegreesSerializer)
    def post(self,request):
        serializer=ModDegreesSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response('Cant posted !')
        
    def get(self,request):
        moddegrees=ModDegrees.objects.all()
        serializer=ModDegreesSerializer(moddegrees,many=True)
        return Response(data=serializer.data)

class ModBonusesAPIView(APIView):
    serializer_class=ModBonusesSerializer
    permission_classes=(IsAdminUser,)
    
    @swagger_auto_schema(request_body=ModBonusesSerializer)
    def post(self,request):
        serializer=ModBonusesSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response('Cant posted !')
        
    def get(self,request):
        modbonuses=ModBonuses.objects.all()
        serializer=ModBonusesSerializer(modbonuses,many=True)
        return Response(data=serializer.data)

class EmploymentAPIViev(APIView):
    serializer_class=EmploymentSerializer
    permission_classes=(IsAdminUser,)
    
    @swagger_auto_schema(request_body=EmploymentSerializer)
    def post(self,request):
        serializer=EmploymentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response('Cant posted !')
        
    def get(self,request):
        employments=Employment.objects.all()
        serializer=EmploymentSerializer(employments,many=True)
        return Response(data=serializer.data)



# Xodimlar qo'shish | add Employees : 1-usul:

# class EmployeesAPIView(APIView):
#     serializer_class=EmployeesSerializer
#     permission_classes=(AllowAny,)
#     # permission_classes = [HasGroupPermission,IsAuthenticated]
    
#     @swagger_auto_schema(request_body=EmployeesSerializer)
#     def post(self,request):
#         serializer=ModBonusesSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             phone=request.data.get('phone',False)
#             password=request.data.get('password',False)
#             user_create_status=Register(phone,password)
#             print("***************************")
#             print(user_create_status)
#             print("***************************")
#             if user_create_status==True:
#                 serializer_obj=serializer
#                 serializer_obj.save()
#             return Response(data=serializer.data)
#         else:
#             return Response('Cant posted !')
        
#     def get(self,request):
#         employees=Employees.objects.all()
#         serializer=EmployeesSerializer(employees,many=True)
#         return Response(data=serializer.data)


# # Xodimlar qo'shish | add Employees : 2-usul:

# class TeacherInheriAPIView(APIView):
#     serializer_class=TeacherInheriSerializer
#     permission_classes=(AllowAny,)
#     # permission_classes = [HasGroupPermission,IsAuthenticated]
    
#     @swagger_auto_schema(request_body=TeacherInheriSerializer)
#     def post(self,request):
#         serializer=TeacherInheriSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             phone=request.data.get('phone')
#             password=request.data.get('password')
#             user_create_status=Register(phone,password)
#             user_create_status.post()
#             print("***************************")
#             print(user_create_status)
#             print("***************************")
#             if user_create_status==True:
#                 user_id=user_create_status.phone.id
#                 print("***************************")
#                 print(user_id)
#                 print("***************************")
#                 serializer_obj=serializer
#                 serializer_obj.save(user_id=user_id)
#             return Response(data=serializer_obj.data)
#         else:
#             return Response('Cant posted !')
        
#     def get(self,request):
#         teacherinheris=TeacherInheri.objects.all()
#         serializer=TeacherInheriSerializer(teacherinheris,many=True)
#         return Response(data=serializer.data)

#2-usul:

default='ansoracademy'
generate=random.randint(99, 999)

class TeacherInheriAPIView(APIView):
    serializer_class=TeacherInheriSerializer
    permission_classes=(AllowAny,)
    # permission_classes = [HasGroupPermission,IsAuthenticated]
    
    @swagger_auto_schema(request_body=TeacherInheriSerializer)
    def post(self,request):
        serializer=TeacherInheriSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone=request.data.get('phone_num')
            password=f"{default}{generate}"
            if phone and password:
            # old=PhoneOTP.objects.filter(phone__iexact=phone)
            # if old.exists():
            #     old=old.first()
            #     validated=old.validated
            #     data=request.data
                # if validated:
                data={
                    "phone":phone,
                    'password':password
                }
                reg_serializer=CreateUserSerializer(data=data)
                if reg_serializer.is_valid():
                    password=reg_serializer.validated_data.get('password')
                    reg_serializer.validated_data['password']=make_password(password)
                    new_user=reg_serializer.save()
                    # old.delete()
                    if new_user:
                        new_user=new_user
                        user_ids=new_user.id
                        uss=User.objects.get(pk=user_ids)
                        
                        serializer.save()
                        
                        get_emp_id = serializer.data.get('id')
                        emp=TeacherInheri.objects.get(pk=get_emp_id)
                        emp.user_id=uss
                        
                        emp.save()
                        first_name=emp.first_name
                        last_name=emp.last_name
                        phone_num=emp.phone_num
                        password=password
                        TelegramMessage(first_name,last_name,phone_num,password)
                    else:
                        return Response('Cant posted !')
                    return Response(
                        {
                            'status':True,
                            'detail':'Account successfuly created !'
                        }
                    )
                else:
                    return Response(
                        {
                            'status':False,
                            'detail':"OTP haven't verified .First do that step !"
                        }
                    )
            else:
                return Response(
                    {
                        'status': False,
                        'datail': "Both Phone and password are not sent !",
                    }
                )

        
    def get(self,request):
        teacherinheris=TeacherInheri.objects.all()
        serializer=TeacherInheriSerializer(teacherinheris,many=True)
        return Response(data=serializer.data)


class ModeratorInheriAPIView(APIView):
    serializer_class=ModeratorInheriSerializer
    permission_classes=(AllowAny,)
    # permission_classes = [HasGroupPermission,IsAuthenticated]
    
    @swagger_auto_schema(request_body=ModeratorInheriSerializer)
    def post(self,request):
        serializer=ModeratorInheriSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone=request.data.get('phone_num')
            password=f"{default}{generate}"
            if phone and password:
            # old=PhoneOTP.objects.filter(phone__iexact=phone)
            # if old.exists():
            #     old=old.first()
            #     validated=old.validated
            #     data=request.data
                # if validated:
                data={
                    "phone":phone,
                    'password':password
                }
                reg_serializer=CreateUserSerializer(data=data)
                if reg_serializer.is_valid():
                    password=reg_serializer.validated_data.get('password')
                    reg_serializer.validated_data['password']=make_password(password)
                    new_user=reg_serializer.save()
                    # old.delete()
                    if new_user:
                        new_user=new_user
                        user_ids=new_user.id
                        uss=User.objects.get(pk=user_ids)
                        
                        serializer.save()
                        
                        get_emp_id = serializer.data.get('id')
                        emp=ModeratorInheri.objects.get(pk=get_emp_id)
                        emp.user_id=uss
                        
                        emp.save()
                        
                        full_name=f'{emp.first_name} {emp.last_name}'
                        phone_num=emp.phone_num
                        subject=f'login: {emp.phone_num}\npassword{password}'
                        
                        bot_token='6066491939:AAEDBrclIjq88En5z-Vzy33IHCwjl6xOEsM'
                        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                        message_data=f"New Applicant:\n{full_name}\n{phone_num}\n{subject}"
                        chat_id=1731117573
                        payload = {
                            "text": message_data,
                            "parse_mode": "HTML",
                            "disable_web_page_preview": False,
                            "disable_notification": False,
                            "reply_to_message_id": 0,
                            "chat_id": chat_id
                        }
                        headers = {
                            "accept": "application/json",
                            "User-Agent": "Telegram Bot SDK - (https://github.com/irazasyed/telegram-bot-sdk)",
                            "content-type": "application/json"
                        }
                        response = requests.post(url, json=payload, headers=headers)
                        print(response.text)
                        return Response(data=serializer.data)
                    else:
                        return Response('Cant posted !')
                    
                    return Response(
                        {
                                'status':False,
                                'detail':'Cant created account'
                        }
                    )
                else:
                    return Response(
                            {
                                'status':False,
                                'detail':"OTP haven't verified .First do that step !"
                            }
                        )
                            
        else:
            return Response(
                    {
                        'status': False,
                        'datail': "Both Phone and password are not sent !",
                    }
                )
        
    def get(self,request):
        moderatorinheris=ModeratorInheri.objects.all()
        serializer=ModeratorInheriSerializer(moderatorinheris,many=True)
        return Response(data=serializer.data)

def TelegramMessage(first_name,last_name,phone_num,password):
    full_name=f'{first_name} {last_name}'
    phone=phone_num
    subject=f'login: {phone}\npassword: {password}'
                        
    bot_token='6066491939:AAEDBrclIjq88En5z-Vzy33IHCwjl6xOEsM'
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    message_data=f"New Applicant: {full_name}\nPjone number: {phone_num}\n{subject}"
    chat_id=1731117573
    payload = {
                "text": message_data,
                "parse_mode": "HTML",
                "disable_web_page_preview": False,
                "disable_notification": False,
                "reply_to_message_id": 0,
                "chat_id": chat_id
                }
    headers = {
        "accept": "application/json",
        "User-Agent": "Telegram Bot SDK - (https://github.com/irazasyed/telegram-bot-sdk)",
        "content-type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    print(response.text)