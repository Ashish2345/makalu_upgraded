from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.db.models import Q
from django.http import JsonResponse

from datetime import timedelta

from .instagram_fetcher import scrape_user_posts

from .models import *

from django.utils import timezone
from django.shortcuts import render
from .models import Region, PopularPeaks, Blogs

from .emailsetup import _sendNormalEmail

from django.conf import settings
import urllib,json

class FrontendMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        region = Region.objects.all()
        all_region_treks = []
        expediton_peeks = []
        all_expedition = ["8000","7000","6000"]
        for region in region:
            region_trek = PeeksLists.objects.filter(region_peak=region, peek_type="treks")[:6]
            all_region_treks.append(region_trek)

        for region in all_expedition:
            region_trek = PeeksLists.objects.filter(peek_type="expedition", peeks_catg__name=region)[:6]
            expediton_peeks.append(region_trek)
        # print(PeeksLists.objects.filter(region_peak__in=region))
        context["regions"] = Region.objects.all()
        context["regions_peek"] = all_region_treks
        context["recent_searchs"] = PeeksLists.objects.order_by("?")[:5]

        context["expeditions_peek"] = expediton_peeks
        context["instagram_post"] = InstagramPost.objects.order_by("-created_at")[:4]
        return context

class HomeView(FrontendMixin, TemplateView):
    template_name = "index.html"

    def fetch_instagram_posts(self):
        post_count = InstagramPost.objects.count()
        current_time = timezone.now()
        try:
            if post_count < 3:
                posts = scrape_user_posts("makalumountaineering", num_posts=5)
            else:
                oldest_post = InstagramPost.objects.order_by("created_at").first()
                if oldest_post and (current_time - oldest_post.created_at) > timedelta(days=1):
                    InstagramPost.objects.all().delete()
                    posts = scrape_user_posts("makalumountaineering", num_posts=5)
                else:
                    posts =  InstagramPost.objects.all()
        except:
            posts =  InstagramPost.objects.all()
        return posts[:3]

    def get_context_data(self, **kwargs):
        trending_destination = PeeksLists.objects.select_related("region_peak").filter(trending=True)[:5]
        context = super().get_context_data(**kwargs)
        context["all_exp"] = PeeksLists.objects.filter(peek_type="expedition").order_by("?")[:4]
        context["top_trendings"] = trending_destination
        context["blogs"] = Blogs.objects.all()[:3]

        context["instagram_posts"] = self.fetch_instagram_posts()


        return context


    def post(self, request, *args, **kwargs):
        print(request.POST)
        if "execlusive" in request.POST:
            email = request.POST.get("exe_email")
            ExeclusiveApplied.objects.get_or_create(email=email)
            return JsonResponse({"sucesss": True,"message":"Applied Successfully"})

        email = request.POST.get("email")
        NewsLetterModel.objects.get_or_create(email=email)
        return JsonResponse({"sucesss": True})


class AboutUsView(FrontendMixin, TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["teams"] = Teams.objects.all()[:5]
        return context

class TeamDetailView(DetailView):
    model = Teams
    template_name = "team_details.html"
    context_object_name = "team"
    slug_field = "slug"
    slug_url_kwarg = "slug"


class PrivacyPolicyView(FrontendMixin, TemplateView):
    template_name = "privacy_policy.html"

class ContactUsView(FrontendMixin, TemplateView):
    template_name = "contact.html"

    def post(self, request, *args, **kwargs):
        result = validate_captcha(request)
        print(result["success"] != True)

        if result["success"] != True:
            self.extra_context = {
                "success": "Invalid Captcha",
                "invalid": False
            }
            return super().get(request, *args, **kwargs)
        data = request.POST.dict()
        data.pop("csrfmiddlewaretoken")
        data.pop("g-recaptcha-response")
        contact = ContactUsModel(**data)
        contact.save()
        _sendNormalEmail(to="chhiringsh4@gmail.com", context={'object':contact},  template='email/email_set.html', purpose='Someone Contacted')


        if contact:
            self.extra_context = {
                "success": "Thank you for contacting Malaku Mountaineering! Your message has been successfully sent."
            }

        return super().get(request, *args, **kwargs)



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


class SearchPeekListsView(FrontendMixin, ListView):
    model = PeeksLists
    template_name = "peeklists.html"
    context_object_name = "object_lists"
    paginate_by = 8

    def get_queryset(self):
        search_val = self.request.GET.get("q", None)
        if search_val:
            all_peeks =  PeeksLists.objects.filter(Q(name__icontains=search_val) | Q(region_peak__name=search_val)).distinct()
            return all_peeks
        region = self.request.GET.get("region", None)
        tour_type = self.request.GET.get("tour_type", None)
        if tour_type == "Trekking":
            tour_type = "treks"

        if region == "Search destinations" or tour_type == "All tour":
            all_peeks =  PeeksLists.objects.filter(Q(region_peak__name=region) | Q(peek_type=tour_type)).distinct()
            if not all_peeks:
                return PeeksLists.objects.all()
            return all_peeks



        if region and tour_type:
            all_peeks =  PeeksLists.objects.filter(region_peak__name=region,peek_type=tour_type).distinct()
            if not all_peeks:
                return PeeksLists.objects.all()
            return all_peeks
        return PeeksLists.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        region = self.request.GET.get("region", None)
        tour_type = self.request.GET.get("tour_type", None)
        if region == "Search destinations" and tour_type == "All tour":

            context["type"] = "Peeks"
        elif self.request.GET.get("q", None):
            context["type"] = self.request.GET.get("q")
            context["search"] = True

        else:
            if region == "Search destinations":

                context["region_selected"] = self.request.GET.get("tour_type", "Tour")
            elif tour_type == "All tour":
                context["region_selected"] = self.request.GET.get("region", "Region")
            else:
                context["region_selected"] = self.request.GET.get("region", "Region")
                context["type"] = self.request.GET.get("tour_type", "Tour")
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


class BlogsView(FrontendMixin, ListView):
    model = Blogs
    template_name = "blogs.html"
    context_object_name = "object_lists"
    paginate_by = 8


    def get_queryset(self):
        if self.request.GET.get("q"):
            return Blogs.objects.filter(category__name=self.request.GET.get("q"))
        return Blogs.objects.all()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog_category'] = BlogCategory.objects.all()[::-1]
        context['related_posts'] = Blogs.objects.order_by("?")

        return context

class BlogDetailsView(FrontendMixin, TemplateView):
    template_name = "blogs-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog'] = get_object_or_404(Blogs, id=self.kwargs.get("id"))
        return context

    def post(self, request, *args, **kwargs):
        blog_id = kwargs.get("id")
        blog_details = get_object_or_404(Blogs, id=blog_id)
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken', None)

        data.pop('comments', None)
        comment = CommentsTours(**data, blogs=blog_details)
        comment.save()
        message = "Comment Added Successfully!"
        context = {
            "blog": blog_details,
            "message": message
        }
        return render(request, self.template_name, context)



class TermsandConditionView(FrontendMixin, TemplateView):
    template_name = "terms.html"

class TripAdvisory(FrontendMixin, TemplateView):
    template_name = "trip_advisory.html"

class FAQView(FrontendMixin, TemplateView):
    template_name = "faq.html"

    # You can override the get_context_data method to pass additional context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('q', '')
        print(search_query,5555555555555555555)
        if search_query:
            context["all_faq"] = FAQLists.objects.filter(questions__icontains=search_query)
        else:
            context["all_faq"] = FAQLists.objects.all()[:10]
        return context


class GalleryView(FrontendMixin, TemplateView):
    template_name = "gallery.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context




class SearchPeekJsonView(View):

    def get(self, request, *args, **kwargs):
        search_val = self.request.GET.get("q", None)
        if search_val:
            all_peeks =  list(PeeksLists.objects.filter(Q(name__icontains=search_val) | Q(region_peak__name=search_val)).distinct().values("id","name","region_peak__name","thumbnail")[:10])
        print(all_peeks)
        return JsonResponse({"all_peeks":all_peeks})

def validate_captcha(request):
    recaptcha_response = request.POST.get('g-recaptcha-response')
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
            }

    data = urllib.parse.urlencode(values).encode()
    req =  urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())

    return result


class BookTour(FrontendMixin, TemplateView):
    template_name = "details.html"

    def get_context_data(self, **kwargs):
        peek_id = kwargs.get("id")
        tours_details = get_object_or_404(PeeksLists, id=peek_id)

        context = {
            "tour": tours_details,
            "message": None,
            "related_tours": PeeksLists.objects.filter(peeks_catg=tours_details.peeks_catg).exclude(id=tours_details.id).order_by('?')[:6],
        }

        return context

    def post(self, request, *args, **kwargs):

        result = validate_captcha(request)

        peek_id = kwargs.get("id")
        tours_details = get_object_or_404(PeeksLists, id=peek_id)
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken', None)
        data.pop('g-recaptcha-response', None)

        if result["success"] != True:
            context = {
                    "tour": tours_details,
                    "message": "Invalid Captcha!",
                    "success": False,
                    "related_tours": PeeksLists.objects.filter(peeks_catg=tours_details.peeks_catg).exclude(id=tours_details.id).order_by('?')[:6],
                }
            return render(request, self.template_name, context)


        if "comments" in request.POST:
            data.pop('comments', None)
            comment = CommentsTours(**data, peek_info=tours_details)
            comment.save()
            message = "Comment Added Successfully!"
        else:
            data.pop('book_tour', None)
            tour = BookaTour(**data, peek_info=tours_details)
            tour.save()
            message = "Booked Successfully!"

        context = {
            "tour": tours_details,
            "message": message,
            "related_tours": PeeksLists.objects.filter(peeks_catg=tours_details.peeks_catg).exclude(id=tours_details.id).order_by('?')[:6],
            "success": True
        }

        _sendNormalEmail(to="chhiringsh4@gmail.com", context={'object':tour},  template='email/booking_details.html', purpose='Booking Request')


        return render(request, self.template_name, context)



class CertificatesView(FrontendMixin, ListView):
    model = Certificates
    template_name = "certificates.html"
    context_object_name = "object_lists"
    paginate_by = 8



class RoalityFreeView(FrontendMixin, TemplateView):
    template_name = "roality.html"


class HostingExpiredView(FrontendMixin, TemplateView):
    template_name = "hostingexpired.html"
