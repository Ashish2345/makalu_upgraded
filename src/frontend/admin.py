from django.apps import  apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

from .models import *


# Register your models here.
for pn_model in apps.get_app_config('frontend').get_models():
    try:
        admin.site.register(pn_model)
    except AlreadyRegistered:
        pass



