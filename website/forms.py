from django import forms
from .models import User

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['fullname','username', 'email', 'image']
 
    image = forms.ImageField(required=True,)