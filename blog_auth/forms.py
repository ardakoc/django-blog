from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django_registration import forms

from blog_auth.models import User


class BlogRegistrationForm(forms.RegistrationForm):
    class Meta(forms.RegistrationForm.Meta):
        model = User

    def __init__(self, *args, **kwargs):
        super(BlogRegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Register'))    
