"""dj_diploma URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main_view, name='home'),
    path('section/<int:id>', views.section_view, name='section'),
    path('section/', views.section_view, name='section_0'),
    path('good/', views.good_view, name='good'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cart/', views.cart_view, name='cart'),
    path('add_cart/', views.add_cart_view, name='add_cart'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += [
#     url(r'^accounts/', include('django.contrib.auth.urls')),
# ]
