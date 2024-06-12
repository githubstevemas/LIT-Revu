from django import forms
from flux.models import Ticket, Review


class TicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect
    )

    class Meta:
        model = Review
        fields = ['ticket', 'rating', 'headline', 'body']


class ReviewTicketForm(forms.ModelForm):
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect
    )

    class Meta:
        model = Review
        fields = ['rating', 'headline', 'body']


class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)
