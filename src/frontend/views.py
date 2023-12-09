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

