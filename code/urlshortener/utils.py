from django.utils.crypto import get_random_string
from django.conf import settings




#   Generating random code for the shortcode
#   Making use of Django inbuilt get_random_string
SHORTCODE_MIN = getattr(settings, "SHORTCODE_MIN", 6)

def generate_code(instance, size=SHORTCODE_MIN, type_="shortcode"):
    new_code = get_random_string(length = size)
    Klass = instance.__class__
    
    if type_ == "verification":
        obj_exists = Klass.objects.filter(key = new_code).exists()
    else:
        obj_exists = Klass.objects.filter(shortcode = new_code).exists()
    if obj_exists:
        return generate_code(instance)
    return new_code



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR", None)
    return ip