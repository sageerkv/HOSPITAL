from django import forms
from .models import Booking
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth  import get_user_model
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


class DateInput(forms.DateInput):
    input_type = 'date'

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'
        widgets = {
            'Booking_date':DateInput()
        }
        labels = {
            'p_name':'Patient Name:',
            'p_phone':'Patient Phone', 
            'p_email':'Patient Email',
            'doc_name':'Doctor Name',
            'Booking_date':'Booking Date', 
        }

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text='A valid email address, please.', required=True)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = get_user_model()
        fields = [ 'username','first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        return user

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Username or Email'}),
            label="Username or Email")

    password = forms.CharField(widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password'}))
    
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']
    
class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ('new_password1', 'new_password2')


class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

