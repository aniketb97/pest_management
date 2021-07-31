"""pstmgmt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings
admin.site.site_header = "Pest Management Admin"
admin.site.site_title = "Pest Management Admin Portal"
admin.site.index_title = "Welcome to Pest Management Admin Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='apis')),
    path('insect/', include('insect.urls', namespace='insect')),
    path('signup/', include('signup.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
