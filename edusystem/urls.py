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
        title='API DOC',
        default_version='v1',
        description='swagger documentation for Next Developers Team',
        terms_of_service='© Next Developers Team 2023.',
        contact=openapi.Contact(email='o.islomov@tuit.uz'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    path("korinmas_admin/", admin.site.urls),
    path('korinmas_api/',include('systemapp.urls')),
    path('korinmas_api/',include('dj_rest_auth.urls')),
    path('',schema_view.with_ui('swagger',cache_timeout=0),name='schema-swagger-ui')
    #path('swagger/',schema_view.with_ui('swagger',cache_timeout=0),name='schema-swagger-ui')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
