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



# class PeeksListsAdmin(admin.ModelAdmin):
#     list_display = ('name', 'peek_type', 'region_peak', 'rating', 'trending', 'popular')
#     list_filter = ('peek_type', 'region_peak', 'trending', 'popular')
#     search_fields = ('name', 'region_peak__name')

#     fieldsets = (
#         ('General Information', {
#             'fields': ('name', 'peek_type', 'region_peak', 'peeks_catg', "price")
#         }),
#         ('Media', {
#             'fields': ('thumbnail', 'main_iamge')
#         }),
#         ('Details', {
#             'fields': ('rating', 'rate_total', 'overview', 'duration', 'highest_elevation',
#                        'accomodation', 'season', 'age', 'location', 'location_frame')
#         }),
#         ('Flags', {
#             'fields': ('popular', 'trending')
#         }),
#     )

# admin.site.register(PeeksLists, PeeksListsAdmin)