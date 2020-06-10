from django.urls import path, re_path
from django.conf.urls import url

app_name = 'Shortener'

from .views import AutoSearchView, HomeView, SiteLogicView


urlpatterns = [
    path('search/', AutoSearchView.as_view(), name='auto_search'),
    path('', HomeView.as_view(), name='home'),
    re_path('(?P<shortcode>[0-9A-Za-z]+)/$', 
            SiteLogicView.as_view(), 
            name='shortcode'),
]
