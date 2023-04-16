from django import forms

from api import models


class AdminAddProgramForm(forms.ModelForm):
    class Meta:
        model = models.Program
        fields = '__all__'
