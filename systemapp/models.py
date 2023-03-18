from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator

from django.contrib.auth.models import Group, Permission

# Create your models here.

class Courses(models.Model):
    course_name=models.CharField(max_length=100 , verbose_name='Course title')

    def __str__(self):
        return self.course_name

class UserManager(BaseUserManager):
    def create_user(self,phone,password=None,is_staff=False,is_active=True,is_admin=False):
        if not phone:
            raise ValueError('Users must have a phone number')
        if not password:
            raise ValueError('Users must have a password')
        
        user_obj=self.model(phone=phone)
        user_obj.set_password(password)
        # user_obj.username=username
        user_obj.staff=is_staff
        user_obj.admin=is_admin
        user_obj.active=is_active
        user_obj.save(using=self._db)
        return user_obj
    
    def create_staffuser(self,phone,password=None):
        user=self.create_user(phone,password=password,is_staff=True)
        return user
    
    def create_superuser(self, phone, password=None):
        user = self.create_user(phone=phone,password=password,is_staff=True,is_admin=True)
        return user
    

class User(AbstractBaseUser):
    phone_regex=RegexValidator(regex=r'^\+?1?\d{9,14}$',message="Phone number nust be entered in the format: '+998906417999'. Up to 14 digits allowed")
    phone=models.CharField(validators=[phone_regex],max_length=20,unique=True)
    # photos=models.ImageField(upload_to='photos/%Y/%m/%d/',blank=True , verbose_name="Rasm")
    first_login=models.BooleanField(default=False)
    active=models.BooleanField(default=True)
    staff=models.BooleanField(default=False)
    admin=models.BooleanField(default=False)
    # comment=models.ForeignKey(Comment,on_delete=models.CASCADE)
    username=None #models.CharField(max_length=20,blank=True,verbose_name='username')
    USERNAME_FIELD='phone'
    REQUIRED_FIELDS=[]
    
    objects=UserManager()
    
    def __str__(self):
        return self.phone
    
    def get_full_name(self):
        if self.phone:
            return self.phone
    
    def get_short_name(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.staff
    
    @property
    def is_admin(self):
        return self.admin
    
    @property
    def is_active(self):
        return self.active
    
    class Meta:
        permissions = (("class_schedule", "To provide class_schodule | dars jadvalini ko'rish"),
                        ("feedback", "To provide feedbacks | firk-mulohazalarni ko'rish"),
                        ("add_a _student", "To provide add a student | talaba qo'shish"),
                        ("see students list", "To provide see students "),
                        ("can_see_fgh", "jfbhjsb"),
                        ("can_go_msdsh", "fhebhb"),
                        ("can_change_bjsbhj", "fjfbjvhv"),
                        ("can_change_rshdh", "fvjfvbhbvd"))


class PhoneOTP(models.Model):
    phone_regex=RegexValidator(regex=r'^\+?1?\d{9,14}$',message="Phone number nust be entered in the format: '+998906417999'. Up to 14 digits allowed")
    phone=models.CharField(validators=[phone_regex],max_length=20,unique=True)
    otp=models.CharField(max_length=6,blank=True,null=True)
    validated=models.BooleanField(default=False,help_text='if it is true,that means user have validate otp correctly i second API')
    
    full_name=models.CharField(max_length=50 , verbose_name='Applicant Full Name',blank=True,null=True)
    # phone_num=models.CharField(max_length=13,verbose_name='Applicant phone number')
    course_id=models.ForeignKey(Courses,on_delete=models.CASCADE , verbose_name='Course type',blank=True,null=True)
    
    def __str__(self):
        return str(self.phone) + ' if sent ' + str(self.otp)



# class GroupModel(models.Model):
#     group_name=models.CharField(max_length=50 , verbose_name='Group name')

class Genders(models.Model):
    gender_type=models.CharField(max_length=15 , verbose_name='gender type')
    
    def __str__(self):
        return self.gender_type
    

class KPI(models.Model):
    amount_one=models.FloatField(max_length=9 , verbose_name='bonus | fine emaunt')
    amount_two=models.FloatField(max_length=9 , verbose_name='bonus | fine emaunt')
    # is_bool=models.BooleanField(default=False,verbose_name="bool")
    
    def __str__(self):
        return f'{self.amount_one} | {self.amount_two}'

class Percentage(models.Model):#teacher func
    name=models.CharField(max_length=100 , verbose_name='Percentage name')
    percentage=models.FloatField(max_length=5 , verbose_name='Percentage amount')
    
    def __str__(self):
        return f'{self.name} | {self.percentage}'

class TeacherDegrees(models.Model):#teacher func
    level=models.CharField(max_length=50 , verbose_name='Level')
    full_time=models.FloatField(max_length=9, null=True, verbose_name='Salary emaunt')
    part_time=models.FloatField(max_length=9, null=True, verbose_name='Salary emaunt')
    
    def __str__(self):
        return f'{self.level} | {self.full_time} | {self.part_time}'

# class TeacherFunc(models.Model):
#     pass

class FunctionsTeacher(models.Model):
    salary=models.ForeignKey(Percentage,on_delete=models.CASCADE,verbose_name="Percentage salary")
    course=models.ManyToManyField(Courses,verbose_name="Course name")
    level=models.ForeignKey(TeacherDegrees,on_delete=models.CASCADE,verbose_name="Level")
    
    def __str__(self):
        return f'{self.salary.name} | {self.course.name} | {self.level.level}'


class ModDegrees(models.Model):#meneger func
    level=models.CharField(max_length=50 , verbose_name='Level')
    full_time=models.FloatField(max_length=9, null=True, verbose_name='Salary emaunt')
    part_time=models.FloatField(max_length=9, null=True, verbose_name='Salary emaunt')
    
    def __str__(self):
        return f'{self.level} | {self.full_time} | {self.part_time}'

class ModBonuses(models.Model):#meneger func
    amount_one=models.FloatField(max_length=9 , verbose_name='bonus | fine emaunt')
    amount_two=models.FloatField(max_length=9 , verbose_name='bonus | fine emaunt')
    amount_three=models.FloatField(max_length=9 , verbose_name='bonus | fine emaunt')
    # is_bool=models.BooleanField(default=False,verbose_name="bool")
    
    def __str__(self):
        return f'{self.amount_one} | {self.amount_two} | {self.amount_three}'

class Employment(models.Model):
    full_time=models.CharField(max_length=50, null=True, verbose_name='full time salary emaunt')
    part_time=models.CharField(max_length=50, null=True, verbose_name='part time salary emaunt')
    
    def __str__(self):
        return f'{self.full_time} | {self.part_time}'

# class Functions(models.Model):
#     moderator=models.ForeignKey(ModDegrees,on_delete=models.CASCADE,verbose_name="Level")


#birinchi usul:
# class Employees(models.Model):
    
#     CITY_CHOICES = [
#         ('Teacher',FunctionsTeacher),

#         ('Moderator', ModDegrees),
#     ]
    
#     phone_regex=RegexValidator(regex=r'^\+?1?\d{9,14}$',message="Phone number nust be entered in the format: '+998906417999'. Up to 14 digits allowed")
#     email_regex=RegexValidator(regex=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b',message="email nust be entered in the format: 'example@demein'-> oqiljonnishonov@gmail.com.")
#     first_name=models.CharField(max_length=100 , verbose_name='First name')
#     last_name=models.CharField(max_length=100 , verbose_name='Last name')
#     phone_num=models.CharField(validators=[phone_regex],max_length=20,unique=True)
#     email=models.CharField(validators=[email_regex],max_length=20,unique=True)
#     gender=models.ForeignKey(Genders,on_delete=models.CASCADE,verbose_name="Gender")
#     birth_date=models.DateField()
#     salary=models.FloatField(default=0,max_length=9,verbose_name="Salary")
#     # functions=models.ForeignKey(Functions,on_delete=models.CASCADE,verbose_name="Gender")
#     function=models.CharField(max_length=100, choices=CITY_CHOICES, verbose_name="Choices")
#     # branch=""
#     role=models.ForeignKey(Group,on_delete=models.CASCADE)
#     photo=models.ImageField(upload_to='photos',blank=True , verbose_name="Photo")
#     created_at=models.DateTimeField(auto_now_add=True, verbose_name="Added time")
#     updated_at=models.DateTimeField(auto_now=True, verbose_name="Updated time")
#     user_id=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="User id")



#Ikkinchi usul:
class Employees(models.Model):
    phone_regex=RegexValidator(regex=r'^\+?1?\d{9,14}$',message="Phone number nust be entered in the format: '+998906417999'. Up to 14 digits allowed")
    email_regex=RegexValidator(regex=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b',message="email nust be entered in the format: 'example@demein'-> oqiljonnishonov@gmail.com.")
    first_name=models.CharField(max_length=100 , verbose_name='First name')
    last_name=models.CharField(max_length=100 , verbose_name='Last name')
    phone_num=models.CharField(validators=[phone_regex],max_length=20,unique=True)
    email=models.CharField(validators=[email_regex],max_length=50,unique=True)
    gender=models.ForeignKey(Genders,on_delete=models.CASCADE,verbose_name="Gender")
    birth_date=models.DateField()
    employee_salary=models.FloatField(default=0,max_length=9,verbose_name="Salary")
    role=models.ForeignKey(Group,on_delete=models.CASCADE, null=True,default=None)
    photo=models.ImageField(upload_to='photos',blank=True , verbose_name="Photo")
    created_at=models.DateTimeField(auto_now_add=True, verbose_name="Added time")
    updated_at=models.DateTimeField(auto_now=True, verbose_name="Updated time")
    user_id=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="User id",null=True,default=None)
    
    def __str__(self):
        return f'{self.first_name} | {self.employee_salary} | {self.user_id.phone}'
    

class TeacherInheri(Employees):
    salary=models.ForeignKey(Percentage,on_delete=models.CASCADE,verbose_name="Percentage salary")
    course=models.ManyToManyField(Courses,verbose_name="Course name")
    level=models.ForeignKey(TeacherDegrees,on_delete=models.CASCADE,verbose_name="Level")
    
    def __str__(self):
        return f'{self.first_name} | {self.level.level} | {self.level.full_time} {self.level.part_time}'

class ModeratorInheri(Employees):
    level=models.ForeignKey(ModDegrees,on_delete=models.CASCADE , verbose_name='Level')
    employment=models.ForeignKey(Employment, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.first_name} | {self.employment.full_time} {self.employment.part_time}'
    