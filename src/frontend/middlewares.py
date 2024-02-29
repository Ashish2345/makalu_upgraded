# myapp/middleware.py
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

class HostingExpiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request is not for the "Coming Soon" page
        if not request.path.startswith(reverse('frontend:hosting_expired')):
            # Redirect all requests to the "Coming Soon" page
            return HttpResponseRedirect(reverse('frontend:hosting_expired'))

        # If the request is for the "Coming Soon" page, continue with the normal flow
        response = self.get_response(request)
        return response
