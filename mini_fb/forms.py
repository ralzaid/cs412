from django import forms
from .models import Profile

class CreateProfileForm(forms.ModelForm):
    first = forms.CharField(label="First Name", required=True)
    last = forms.CharField(label="Last Name", required=True)
    city = forms.CharField(label="City", required=True)
    email = forms.EmailField(label="Email", required=True)
    image_url = forms.URLField(label="Image URL", required=False)

    class Meta:
        model = Profile
        fields = ['first', 'last', 'city', 'email', 'image_url']