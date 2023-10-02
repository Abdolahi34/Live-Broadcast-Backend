from django import forms

from api import models


# ModelForm for create program instace in new admin panel
class AdminAddProgramForm(forms.ModelForm):
    class Meta:
        model = models.Program
        fields = '__all__'
