from django import forms

from Programs import models


class AdminAddProgramForm(forms.ModelForm):
    class Meta:
        model = models.Program
        fields = '__all__'
