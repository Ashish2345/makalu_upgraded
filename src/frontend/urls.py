from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

app_name = "frontend"

urlpatterns = [
    path('', cache_page(0*60)(HomeView.as_view()), name="home_view"),
    path('about-us/', AboutUsView.as_view(), name="about_us"),
    path('contact-us/', ContactUsView.as_view(), name="contact_us"),
    

    path('peeks/', cache_page(0*60)(PeekListsView.as_view()), name="peek-lists"),
    path('search/', cache_page(0*60)(SearchPeekListsView.as_view()), name="search-peek-lists"),


    path('expeditions/', cache_page(0*60)(ExpeditionListsView.as_view()), name="expeditions-lists"),
    path('trekkings/', cache_page(0*60)(TrekkingListsView.as_view()), name="trekkings-lists"),

    path('peek/details/<int:pk>/', cache_page(0*60)(ToursDetailsView.as_view()), name="tour_details"),

    path('blogs/', BlogsView.as_view(), name="blogs"),
    path('blogs/details/<int:id>/', BlogDetailsView.as_view(), name="blog_details"),

    path('terms-and-conditions/', TermsandConditionView.as_view(), name="terms"),
    path('trip-advisory/', TripAdvisory.as_view(), name="trip-advisory"),

    path('faq/', FAQView.as_view(), name="faq"),
    path('gallery/', GalleryView.as_view(), name="gallery"),

    path('search/json/', cache_page(0*60)(SearchPeekJsonView.as_view())),
    path('blogs/book/<int:id>/', BookTour.as_view(), name="book_tour"),


    path('document-and-certificates/', CertificatesView.as_view()),


    

]
