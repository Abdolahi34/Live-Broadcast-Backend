from django import forms

from Programs import models


class AdminProgramEditForm(forms.ModelForm):
    class Meta:
        model = models.Program
        fields = '__all__'
        exclude = ['created_by', 'last_modified_by', 'date_created', 'date_modified']
