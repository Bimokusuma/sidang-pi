from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm
from django import forms
from .models import Record

class BootstrapAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control form-control-user',
                                   'placeholder': 'Username'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control form-control-user',
                                   'placeholder': 'Password'}))

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=25,
                               widget=forms.TextInput({
                               'class': 'form-control input'}))
    first_name = forms.CharField(max_length=48,
                               widget=forms.TextInput({
                                   'class': 'form-control input'}))
    last_name = forms.CharField(max_length=48,
                               widget=forms.TextInput({
                                   'class': 'form-control input'}))
    password1 = forms.CharField(label=_("Password"),
                           widget=forms.PasswordInput({
                               'class': 'form-control input'}))

    password2 = forms.CharField(label=_("Password"),
                           widget=forms.PasswordInput({
                               'class': 'form-control input'}))
    class Meta:
        model = User
        fields = ('username','first_name','last_name','password1', 'password2')

class RecordForm(ModelForm):
    class Meta:
        model = Record
        fields = ['user', 'score', 'score_addition', 'score_substraction','score_multiplication','score_division']
