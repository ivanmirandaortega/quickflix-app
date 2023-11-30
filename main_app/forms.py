from django.forms import ModelForm
from .models import Review
from django import forms 


class ReviewForm(forms.ModelForm):
    recommend = forms.BooleanField(required=False)
    class Meta:
        
        model = Review
        fields = ['comment','recommend' ]

    