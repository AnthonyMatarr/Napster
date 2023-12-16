from django import forms
from django.db.models.signals import post_save
from django.forms import ModelForm
from .models import *

class ProfileForm(forms.Form):
    name = forms.CharField(label = "Your name", max_length = 100)
    admin = forms.BooleanField()
    profileMade = forms.BooleanField()

modes = (
    ("driving", "driving"), 
    ("walking", "walking"),
    ("bicycling", "bicycling"),
    ("transit", "transit")
)

class DistanceForm(ModelForm): 
    from_location = forms.ModelChoiceField(label="Location from", required=True, queryset=Locations.objects.all())
    to_location = forms.ModelChoiceField(label="Location to", required=True, queryset=Locations.objects.all())
    mode = forms.ChoiceField(choices=modes, required=True)
    class Meta: 
        model = Distances
        exclude = ['created_at', 'edited_at', 'distance_km','duration_mins','duration_traffic_mins']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['message']
        
class LocationImageForm(forms.ModelForm):
    class Meta:
        model = LocationImage
        fields = ['image']