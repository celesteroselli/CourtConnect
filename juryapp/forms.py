from django import forms
from .models import *

class MessageForm(forms.ModelForm):
    message = forms.CharField(required=True)

    class Meta:
        model = Message
        exclude = ("judge", "panel",)

class JuryCreate(forms.Form):
    panel_num = forms.IntegerField(required=True)

class AddJuror(forms.ModelForm):
    number = forms.IntegerField(required=True)

    class Meta:
        model = Number
        fields = ("number",)

from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)
