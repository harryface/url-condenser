from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator, RegexValidator



#   Try and ensure the URL is valid
def validate_url(url):
    url_validator = URLValidator()
    input_url = url
    if "http" in input_url:
        new_url = input_url
    else:
        new_url = "http://" + url
    try:
        url_validator(new_url)
    except:
        raise ValidationError("URL is not valid")


#   Create a form 
class UrlForm(forms.Form):
    url = forms.CharField(
            validators = [validate_url],
            widget = forms.TextInput(
                attrs = {
                    "placeholder": "Input URL",
                    #"class": "form-control"
                    }
                )
            )
    custom_shortcode = forms.CharField(
            required = False,
            validators = [RegexValidator(r"^[0-9a-zA-Z]*$",
                            "Only alphanumeric characters are allowed.")],
            widget = forms.TextInput(
                attrs = {
                    "placeholder": "Custom shortcode",
                    #"class": "form-control"
                    }
                )
            )

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('url', css_class='form-group col-md-6 mb-0'),
                Column('custom_shortcode', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'others',
            Submit('submit', 'Condense')
        )
    """