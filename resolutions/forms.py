from django import forms
from .models import Role, Cause

class RoleForm(forms.Form):
    roles = forms.ModelMultipleChoiceField(queryset=Role.objects.all(), widget=forms.CheckboxSelectMultiple)

class CauseForm(forms.Form):
    causes = forms.ModelMultipleChoiceField(queryset=Cause.objects.all(), widget=forms.CheckboxSelectMultiple)

