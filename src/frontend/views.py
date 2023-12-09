from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from .models import *

class HomeView(View):

    def dispatch(self, request, *args, **kwargs):
        self.template_name = "index.html"
        self.args = {}
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        popular_destinatioon = PopularPeaks.objects.select_related("peek_info").filter(popular_last_month=False)[:3]
        this_month = PopularPeaks.objects.select_related("peek_info").filter(popular_last_month=True).first()
        blogs = Blogs.objects.all()[:5]
        self.args = {
            "popular_destinatioon":popular_destinatioon,
            "this_month":this_month,
            
            "blogs":blogs
        }
        return render(request, self.template_name, self.args)

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



class PeeksListsView(View):
    def dispatch(self, request, *args, **kwargs):
        self.template_name = "peeklists.html"
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    

class ToursDetailsView(View):
    def dispatch(self, request, *args, **kwargs):
        self.template_name = "details.html"
        return super().dispatch(request, *args, **kwargs)
    
    def data_get(self, tours_details):
        comments = CommentsTours.objects.filter(peek_info=tours_details)
        return comments
    
    def get(self, request, *args, **kwargs):
        id = kwargs.get("id")
        # tours_details = get_object_or_404(PeeksLists, id=id)
        self.args = {
            # "tour":tours_details,
            # "highlight": tours_details.peek_highlights.first(),
            # "itemary": tours_details.peek_itemary,
            # "comment": self.data_get(tours_details)
        }

        return render(request, self.template_name, self.args)
    
    def post(self, request, *args, **kwargs):
        id = kwargs.get("id")
        tours_details = get_object_or_404(PeeksLists, id=id)
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken', None)

        if "comments" in request.POST:
            data.pop('comments', None)
            comment = CommentsTours(**data, peek_info=tours_details)
            comment.save()
            message = "Comment Added Successfully!"
        else:
            data.pop('book_tour', None)
            print(data)
            tour = BookaTour(**data, peek_info=tours_details)
            tour.save()
            message = "Booked Successfully!"

        self.args = {
            "tour":tours_details,
            "highlight": tours_details.peek_highlights.first(),
            "itemary": tours_details.peek_itemary.first(),
            "message":message,
            "comment": self.data_get(tours_details)
        }
        return render(request, self.template_name, self.args)


class BlogsView(View):
    def dispatch(self, request, *args, **kwargs):
        self.template_name = "blogs.html"
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        # blog_lists = Blogs.objects.all()
        return render(request, self.template_name)
    

class BlogDetailsView(View):
    def dispatch(self, request, *args, **kwargs):
        self.template_name = "blogs-details.html"
        self.args = {}
        return super().dispatch(request, *args, **kwargs)
    


    def get(self, request, *args, **kwargs):
            # id = kwargs.get("id")
            # blogs = get_object_or_404(Blogs, id=id)
            # self.args = {
            #     "blog":blogs
            # }
            return render(request, self.template_name, self.args)


class TermsandConditionView(View):
    def dispatch(self, request, *args, **kwargs):
        self.template_name = "terms.html"
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class TripAdvisory(View):
    def dispatch(self, request, *args, **kwargs):
        self.template_name = "trip_advisory.html"
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        
        return render(request, self.template_name)

class FAQView(View):
    def dispatch(self, request, *args, **kwargs):
        self.template_name = "faq.html"
        self.payload = {}
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)