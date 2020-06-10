from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View

from analytics.models import UrlViews
from urlshortener.utils import get_client_ip

from .forms import UrlForm
from .models import CondenseURL

# Create your views here.


class AutoSearchView(View):
    def get(self, request, *args, **kwargs):
        custom_shortcode = request.GET.get("q")

        try:
            if not custom_shortcode.isalnum():
                json = {"message":f"{custom_shortcode} is not alphanumeric, leave blank for system to auto generate"}
                return JsonResponse(json, status=200)
            else:
                obj = CondenseURL.objects.filter(shortcode__iexact=custom_shortcode)

                if obj.exists():
                    json = {"message":f"{custom_shortcode} exists, leave blank for system to auto generate"}
                else:
                    json = {"message":f"{custom_shortcode} does not exist, you can go ahead and use it"}
                return JsonResponse(json, status=200)
        except:
            json = {"Ajax call cannot auto-check at this time"}
            return JsonResponse(json, status=500)

        json = {"Ajax call cannot auto-check at this time"}
        return JsonResponse(json, status=500)




class HomeView(View):
    def get(self, request, *args, **kwargs):
        form = UrlForm()
        context = {"form": form,}
        return render(request, "shortener/index.html", context)

    def post(self, request, *args, **kwargs):
        form = UrlForm(request.POST)
        context = {"form": form}
        template = "shortener/index.html"
        if form.is_valid():
            new_url = form.cleaned_data.get("url")
            custom = form.cleaned_data.get("custom_shortcode")
            if not request.user.is_anonymous:
                obj, created = CondenseURL.objects.create_shortcode(owner=request.user, url=new_url, custom_shortcode=custom)
            else:
                obj, created = CondenseURL.objects.create_shortcode(url=new_url, custom_shortcode=custom)
            context = {"object": obj,"form": form}

            if created:
                template = "shortener/success.html"
            else:
                template = "shortener/index.html"
                messages.add_message(request, messages.WARNING,
                    "Shortcode exists, leave blank for the system to auto generate.")
    
        return render(request, template ,context)




class SiteLogicView(View):
    def get(self, request, shortcode=None, *args, **kwargs):
        ip_address = get_client_ip(request)
        obj = get_object_or_404(CondenseURL, shortcode__iexact=shortcode)
        """
        obj = CondenseURL.objects.filter(shortcode__iexact=shortcode)
        if obj.count() != 1 and not qs.exists():
            raise Http404
        obj = qs.first()
        """
        UrlViews.objects.create_event(obj, ip_address)
        return HttpResponseRedirect(obj.url)
