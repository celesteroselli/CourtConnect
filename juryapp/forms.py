from django import forms
from .models import *
from phonenumber_field.formfields import PhoneNumberField

class MessageForm(forms.ModelForm):
    message_form = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    message = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={
                "placeholder": "Message to jurors...",
                "class": "border-0 p-3 h-100 w-100",
            }
        ),
        label="",)

    class Meta:
        model = Message
        exclude = ("judge", "panel",)

class JuryCreate(forms.Form):
    jury_form = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    panel_num = forms.IntegerField(required=True,
    widget=forms.widgets.TextInput(
            attrs={
                "placeholder": "Number of panels",
                "class": "form-control w-100",
            }
        ),
        label="",)
    casename = forms.CharField(required=True,
    widget=forms.widgets.TextInput(
            attrs={
                "placeholder": "Casename",
                "class": "form-control w-100",
            }
        ),
        label="",)

class AddJuror(forms.ModelForm):
    number = PhoneNumberField(region="US")

    class Meta:
        model = Number
        fields = ("number",)

from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email", "first_name", "last_name")

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

