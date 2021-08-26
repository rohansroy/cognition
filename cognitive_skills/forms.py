from django import forms
from captcha.fields import ReCaptchaField
from .models import Result

class RegisterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['turk_id'].widget.attrs = {
            'class': 'form-control'
        }

    turk_id = forms.CharField(label="Turk ID", max_length=100, help_text="The ID provided to you by Amazon Mechanical Turk")
    captcha = ReCaptchaField()


class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['worker', 'test', 'correct', 'total']
        widgets = {
            'correct': forms.HiddenInput(
                attrs={
                    'class': 'form-control correct',
                }
            ),
            'total': forms.HiddenInput(
                attrs={
                    'class': 'form-control total',
                }
            ),
            'worker': forms.HiddenInput(),
            'test': forms.HiddenInput(),
        }
    
    captcha = ReCaptchaField()