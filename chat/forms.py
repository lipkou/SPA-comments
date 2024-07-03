from django import forms
from captcha.fields import CaptchaField
from .models.messages import Message

class MessageForm(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = Message
        fields = ['user_name', 'email', 'home_page', 'text', 'captcha']
