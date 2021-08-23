from django import forms
from captcha.fields import ReCaptchaField

class RegisterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['turk_id'].widget.attrs = {
            'class': 'form-control'
        }

    turk_id = forms.CharField(label="Turk ID", max_length=100, help_text="The ID provided to you by Amazon Mechanical Turk")
    captcha = ReCaptchaField()