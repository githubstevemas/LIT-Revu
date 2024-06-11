from django import forms
from flux.models import Ticket, Review


class TicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = Ticket
        fields = '__all__'


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'


class ReviewTicketForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'headline', 'body']


class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)
