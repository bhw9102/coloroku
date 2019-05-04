from django import forms
from session import models


class PlayerForm(forms.ModelForm):
    class Meta:
        model = models.Player
        fields = ('name',)

