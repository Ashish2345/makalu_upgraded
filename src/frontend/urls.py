from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

app_name = "frontend"

urlpatterns = [
    path('', cache_page(0*60)(HomeView.as_view()), name="home_view"),

]
