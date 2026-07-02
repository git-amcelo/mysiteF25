from django import forms
from .models import Book

class FeedbackForm(forms.Form):
    FEEDBACK_CHOICES = [
        ('B', 'Borrow'),
        ('P', 'Purchase'),
    ]
    feedback = forms.ChoiceField(choices=FEEDBACK_CHOICES)

class SearchForm(forms.Form):
    name = forms.CharField(label='Your Name', required=False)
    category = forms.ChoiceField(
        choices=Book.CATEGORY_CHOICES,
        widget=forms.RadioSelect,
        required=False,
        label='Select a category:'
    )
    max_price = forms.IntegerField(label='Maximum Price', min_value=0, required=True)
