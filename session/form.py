from django import forms
from session.models import Player


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ('name',)

    # def clean_name(self):
    #     name = self.cleaned_data['name']
    #     if Player.objects.filter(name=name).exists():
    #         raise forms.ValidationError("name already exists")
    #     return name

