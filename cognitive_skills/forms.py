from django import forms
from captcha.fields import ReCaptchaField

from .models import Result, Worker


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['age', 'state', 'gender', 'ethnicity', 'years_of_education', 'marital_status', 'orientation', 'employment', 'preliminary_diagnosis']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['age'].widget.attrs.update({'min': 18, 'max': 120})

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