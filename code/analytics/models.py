from django.db import models

# Create your models here.
from shortener.models import CondenseURL

class UrlViewedManager(models.Manager):
    def create_event(self, condensed_object, ip_address):
        if isinstance(condensed_object, CondenseURL):
            obj, created = self.get_or_create(url=condensed_object)
            if created:
                obj.ip_address = ip_address
            else:
                obj.ip_address += f"\n{ip_address}"
            obj.count += 1
            obj.save()
            return
        return

class UrlViews(models.Model):
    url = models.OneToOneField(CondenseURL, on_delete=models.CASCADE)
    ip_address = models.TextField(blank=True, null=True) 
    count = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True) 
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = UrlViewedManager()

    def __str__(self):
        return f"{self.url} - {self.count}"

    class Meta:
        verbose_name = "Url View"