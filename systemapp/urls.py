from django.urls import path,include
from systemapp.views import ValidatePhoneSendOTP, ValidateOTP, Register, CoursesAPIView,TeacherInheriAPIView, ModeratorInheriAPIView, PermissionsGroupAPIView

urlpatterns = [
    path('validate_form/', ValidatePhoneSendOTP.as_view(), name='validate_form'),
    path('validate_otp/', ValidateOTP.as_view(), name='validate_otp'),
    path('register/', Register.as_view(), name='register'),
    path('course/',CoursesAPIView.as_view(),name='Courses'),
    # path('employees/',EmployeesAPIView.as_view(),name='Employees'),
    path('employee_teachers/',TeacherInheriAPIView.as_view(),name='Employees Teacher'),
    path('employee_moderator/',ModeratorInheriAPIView.as_view(),name='Employees Moderator'),
    path('permissions_group/',PermissionsGroupAPIView.as_view(),name='Permissions Group'),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]