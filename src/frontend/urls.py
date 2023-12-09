from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

app_name = "frontend"

urlpatterns = [
    path('', cache_page(0*60)(HomeView.as_view()), name="home_view"),
    path('about-us/', AboutUsView.as_view(), name="about_us"),
    path('contact-us/', ContactUsView.as_view(), name="contact_us"),

    path('peak/lists/', cache_page(0*60)(PeeksListsView.as_view()), name="peek-lists"),

    path('peek/details/<int:id>/', cache_page(0*60)(ToursDetailsView.as_view()), name="tour_details"),

    path('blogs/', BlogsView.as_view(), name="blogs"),
    path('blogs/details/<int:id>/', BlogDetailsView.as_view(), name="blog_details"),

    path('terms-and-conditions/', TermsandConditionView.as_view(), name="terms"),
    path('trip-advisory/', TripAdvisory.as_view(), name="trip-advisory"),

    path('faq/', FAQView.as_view(), name="faq"),
]
