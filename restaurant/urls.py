"""
URL configuration for restaurant project.

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

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path
from Food.views import *

from Users_app.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',first_page, name='first_page'),
    path('menu/',menu, name='menu'),
    path('signup/', signup_view, name='signup'),
    path('profile/', profile_view, name='make_profile'),
    path('login/', login_view, name='login'),
    path('home/',menu, name='home'),
    path('add_to_cart/<str:item_type>/<int:item_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart'),
    path('logout/', logout_view, name='logout'),
    path('place_order/', place_order, name='place_order'),
    path('success_buying/',success_buying,name="success_buying"),
    path('remove-from-cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('information/', info, name='info'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
