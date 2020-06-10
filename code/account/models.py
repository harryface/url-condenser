from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save

from django.core.mail import send_mail
from django.template.loader import get_template


from urlshortener.utils import generate_code

# Create your models here.



class EmailVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(unique = True)
    key = models.CharField(max_length=120, blank=True, null=True)
    activated = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    #objects = EmailVerificationManager()

    def __str__(self):
        return self.email

    def activate(self):
        if not self.activated:
            user = self.user
            user.is_active = True
            user.save()
            self.activated = True
            self.save()

    def send_activation(self):
        if not self.activated:
            if self.key:
                site = getattr(settings, "BASE_URL", "https://www.127.0.0.1:8000")
                path = f"{site}/email/verify/{self.key}/"
                context = {
                    "name":f"{self.user.first_name} {self.user.last_name}",
                    "path": path,
                    "email": self.email
                }
                body_txt = get_template("registration/emails/verify.txt").render(context)
                body_html = get_template("registration/emails/verify.html").render(context)
                subject = "Email Verification"
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [self.email]
                sent_mail = send_mail(subject, body_txt, from_email, recipient_list,
                            html_message = body_html,
                            fail_silently = False,
                    )
                return sent_mail
        return False



def pre_save_email_verification(sender, instance, *args, **kwargs):
    if not instance.activated:
        if not instance.key:
            instance.key = generate_code(instance, size=15, type_="verification")

pre_save.connect(pre_save_email_verification, sender=EmailVerification)


def post_save_user_create_reciever(sender, instance, created, *args, **kwargs):
    if created:
        obj = EmailVerification.objects.create(user=instance, email=instance.email)
        obj.send_activation()

post_save.connect(post_save_user_create_reciever, sender=User)