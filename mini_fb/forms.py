from django import forms
from .models import Profile, StatusMessage, Image

class CreateProfileForm(forms.ModelForm):
    first = forms.CharField(label="First Name", required=True)
    last = forms.CharField(label="Last Name", required=True)
    city = forms.CharField(label="City", required=True)
    email = forms.EmailField(label="Email", required=True)
    image_url = forms.URLField(label="Image URL", required=False)

    class Meta:
        model = Profile
        fields = ['first', 'last', 'city', 'email', 'image_url']


class CreateStatusMessageForm(forms.ModelForm):
    image_file = forms.ImageField(label="Upload Image", required=False)
    class Meta:
        model = StatusMessage
        fields = ['message']

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['city', 'email', 'image_url']
