"""
URL configuration for invoice project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('invoice/', include('invoice_app.urls')),
    path('invoice_jv/', include('invoice_jv.urls')),
    
]

admin.site.site_header = "Gaurav Jewellers"
admin.site.site_title = "Gaurav Jewellers"
admin.site.index_title = "Welcome to Gaurav Jewellers Invoice App"