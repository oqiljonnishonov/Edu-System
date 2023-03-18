"""edusystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include

from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view=get_schema_view(
    openapi.Info(
        title='Ansor IT Academy',
        default_version='v0',
        description='AFPT',
        terms_of_service='HTU',
        contact=openapi.Contact(email='T@T.U'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    path("admin/", admin.site.urls),
        path('',include('systemapp.urls')),
    path('',include('dj_rest_auth.urls')),
    path('swagger/',schema_view.with_ui('swagger',cache_timeout=0),name='schema-swagger-ui')
]
