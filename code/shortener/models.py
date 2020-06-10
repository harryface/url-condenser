from django.db import models
from django.conf import settings
#from django_hosts.resolvers import reverse
from django.urls import reverse
from django.utils.encoding import smart_text
from urlshortener.utils import generate_code
from django.contrib.auth.models import User

# Create your models here.



class CondenseURLManager(models.Manager):
    def all(self, *args, **kwargs):
        obj_main = super(CondenseURLManager, self).all(*args, **kwargs)
        obj = obj_main.filter(active=True)
        return obj
    def create_shortcode(self, url, owner=None, custom_shortcode=None):
        created = False
        obj = self.get_queryset().filter(
                    shortcode__iexact=custom_shortcode
                    )
        if obj.count() == 1:
            obj = obj.first()
        else:
            obj = self.model.objects.create(
                    owner=owner,
                    url=url,
                    shortcode=custom_shortcode 
                    )
            created = True
        return obj, created



class CondenseURL(models.Model):
    owner = models.ForeignKey(User, null=True, blank=True,
                                    on_delete=models.CASCADE)
    url = models.CharField(max_length=220)
    shortcode = models.CharField(max_length=15,
                                    unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    objects = CondenseURLManager()

    #   if the owner doesnt feed in a custom shortcode ...
    def save(self, *args, **kwargs):
        if self.shortcode is None or self.shortcode == "":
            self.shortcode = generate_code(self)
        if not "http" in self.url:
            self.url = f"http://{self.url}"
        super(CondenseURL, self).save(*args, **kwargs)


    def __str__(self):
        return smart_text(self.url)


    def get_condensed_url(self):
        #url_path = reverse("shortcode", kwargs={'shortcode': self.shortcode}, host='www', scheme='http')
        url_path = reverse("shortener:shortcode", kwargs={'shortcode': self.shortcode})
        return f"{settings.SITE_URL}{url_path}"
