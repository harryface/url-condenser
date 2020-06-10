from django.views import View
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from analytics.models import UrlViews
from shortener.models import CondenseURL
from .forms import SignUpForm
from .models import EmailVerification

# Create your views here.


class DashBoardHomeView(View):

    def get(self, request, key=None, *args, **kwargs):
        self.key = key
        if key is not None:
            obj = EmailVerification.objects.filter(key__iexact=key, activated=False)
            if obj.exists():
                obj = obj.first()
                obj.activate()
                messages.success(request, "Your email has been verified. Please login.")
                return redirect("login")
            else:
                msg = "Your email has already been confirmed, kindly log in"
                messages.success(request, msg)
                return redirect("login")
        messages.success(request, "this link is invalid, check your mail for the correct link")
        return redirect("login")


class EmailVerificationView(View):

    def get(self, request, key=None, *args, **kwargs):
        self.key = key
        if key is not None:
            obj = EmailVerification.objects.filter(key__iexact=key, activated=False)
            if obj.exists():
                obj = obj.first()
                obj.activate()
                messages.success(request, "Your email has been verified. Please login.")
                return redirect("login")
            else:
                msg = "Your email has already been confirmed, kindly log in"
                messages.success(request, msg)
                return redirect("login")
        messages.success(request, "this link is invalid, check your mail for the correct link")
        return redirect("login")


class SignUpView(SuccessMessageMixin, CreateView):
    form_class = SignUpForm
    template_name = 'registration/registration_form.html'
    success_url = '/login/'
    success_message = "Account created successfully, check your email for verification email"


class UrlListView(LoginRequiredMixin, ListView):

    paginate_by = 10
    template_name = "dashboard/list.html"

    def get_queryset(self):
        user = self.request.user
        return CondenseURL.objects.filter(owner=user)


class UrlDetailView(LoginRequiredMixin, DetailView):
    model = CondenseURL
    template_name = "dashboard/detail.html"

