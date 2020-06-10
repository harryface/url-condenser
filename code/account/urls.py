from django.urls import path, re_path
from django.contrib.auth.views import LoginView, LogoutView


from .views import(
                EmailVerificationView,
                DashBoardHomeView,
                UrlDetailView,
                UrlListView
            )


app_name = 'Account'

urlpatterns = [

    re_path('email/verify/(?P<key>[0-9A-Za-z]+)/',
            EmailVerificationView.as_view(),
            name='verify_email'),

    path('detail/<pk>/', UrlDetailView.as_view(), name='url_detail'),
    path('', UrlListView.as_view(), name='dashboard'),
]