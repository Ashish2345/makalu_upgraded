from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

from django.http import JsonResponse

from .models import *


from django.shortcuts import render
from .models import Region, PopularPeaks, Blogs

class FrontendMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        region = Region.objects.all()
        all_region_treks = []
        expediton_peeks = []
        all_expedition = ["8000","7000","6000"]
        for region in region:
            region_trek = PeeksLists.objects.filter(region_peak=region, peek_type="treks").values("name","id")[:6]
            all_region_treks.append(region_trek)

        for region in all_expedition:
            region_trek = PeeksLists.objects.filter(peek_type="expedition", peeks_catg__name=region)[:6]
            expediton_peeks.append(region_trek)
        # print(PeeksLists.objects.filter(region_peak__in=region))
        context["regions"] = Region.objects.all()
        context["regions_peek"] = all_region_treks
        
        context["expeditions_peek"] = expediton_peeks
        return context

class HomeView(FrontendMixin, TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        trending_destination = PeeksLists.objects.select_related("region_peak").filter(trending=True)[:5]
        context = super().get_context_data(**kwargs)
        context["all_exp"] = PeeksLists.objects.filter(peek_type="expedition")[:4]
        context["top_trendings"] = trending_destination
        context["blogs"] = Blogs.objects.all()[:3]
        return context


    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        NewsLetterModel.objects.get_or_create(email=email)
        return JsonResponse({"sucesss": True})


class AboutUsView(View):

    def dispatch(self, request, *args, **kwargs):
        self.template_name = "about.html"
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class ContactUsView(View):

    def dispatch(self, request, *args, **kwargs):
        self.template_name = "contact.html"
        self.args = {}
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        data.pop("csrfmiddlewaretoken")
        contact = ContactUsModel(**data)
        contact.save()
        if contact:
            self.args = {
                "success": "Thank you for contacting Malaku Mountaineering! Your message has been successfully sent."
            }   
        return render(request, self.template_name, self.args)



class TrekkingListsView(FrontendMixin, ListView):
    model = PeeksLists 
    template_name = "peeklists.html"
    context_object_name = "object_lists"
    paginate_by = 8

    def get_queryset(self):
        if self.request.GET.get("q"):
            return PeeksLists.objects.filter(peek_type="treks",region_peak__name = self.request.GET.get("q"))
        return PeeksLists.objects.filter(peek_type="treks")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get("q"):
            context["type"] = f"{self.request.GET.get('q')} Treks"
        else:
            context["type"] = "Treks"
        return context


class PeekListsView(FrontendMixin, ListView):
    model = PeeksLists 
    template_name = "peeklists.html"
    context_object_name = "object_lists"
    paginate_by = 8

    def get_queryset(self):
        if self.request.GET.get("q") == "trending":
            return PeeksLists.objects.filter(trending = True)
        return PeeksLists.objects.filter(peek_type="expedition")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get("q"):
            context["type"] = f"{self.request.GET.get('q')}"
        else:
            context["type"] = "Peeks"
        return context


class ExpeditionListsView(FrontendMixin, ListView):
    model = PeeksLists 
    template_name = "peeklists.html"
    context_object_name = "object_lists"
    paginate_by = 8

    def get_queryset(self):
        if self.request.GET.get("q"):
            return PeeksLists.objects.filter(peek_type="expedition",peeks_catg__name = self.request.GET.get("q"))
        return PeeksLists.objects.filter(peek_type="expedition")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get("q"):
            context["type"] = f"{self.request.GET.get('q')} Expeditions"
        else:
            context["type"] = "Expeditions"
        return context

class ToursDetailsView(FrontendMixin, DetailView):
    model = PeeksLists
    template_name = "details.html"
    context_object_name = "tour"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_object = self.get_object()
        context['related_tours'] = PeeksLists.objects.filter(peeks_catg=current_object.peeks_catg).exclude(id=current_object.id).order_by('?')[:6]
        return context

    # def post(self, request, *args, **kwargs):
    #     id = kwargs.get("pk")
    #     tours_details = self.get_object()
    #     data = request.POST.dict()
    #     data.pop('csrfmiddlewaretoken', None)

    #     if "comments" in request.POST:
    #         data.pop('comments', None)
    #         comment = CommentsTours(**data, peek_info=tours_details)
    #         comment.save()
    #         message = "Comment Added Successfully!"
    #     else:
    #         data.pop('book_tour', None)
    #         print(data)
    #         tour = BookaTour(**data, peek_info=tours_details)
    #         tour.save()
    #         message = "Booked Successfully!"

    #     self.object = self.get_object()  # Refresh the object after the POST request
    #     self.object.message = message
    #     return self.render_to_response(self.get_context_data())

    

class BlogsView(FrontendMixin, TemplateView):
    template_name = "blogs.html"

class BlogDetailsView(FrontendMixin, TemplateView):
    template_name = "blogs-details.html"

    # You can override the get_context_data method to pass additional context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Example: Fetch blog details using the provided ID
        # context['blog'] = get_object_or_404(Blogs, id=self.kwargs.get("id"))
        return context

class TermsandConditionView(FrontendMixin, TemplateView):
    template_name = "terms.html"

class TripAdvisory(FrontendMixin, TemplateView):
    template_name = "trip_advisory.html"

class FAQView(FrontendMixin, TemplateView):
    template_name = "faq.html"
    
    # You can override the get_context_data method to pass additional context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Example: Add data to the payload
        # context['payload'] = {'key': 'value'}
        return context
    

class GalleryView(FrontendMixin, TemplateView):
    template_name = "gallery.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context