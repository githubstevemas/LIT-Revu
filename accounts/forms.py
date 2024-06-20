from django import forms

from accounts.models import UserFollows


class FollowUserForm(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = ['followed_user']
        widgets = {
            'followed_user': forms.Select(attrs={'class': 'form-control'}),
        }
