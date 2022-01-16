from django import forms
from . import models


class AddProgramForm(forms.ModelForm):
    class Meta:
        model = models.Program
        fields = '__all__'

