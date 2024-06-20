from django import forms
from .models import Role, Cause

class RoleForm(forms.Form):
    roles = forms.ModelMultipleChoiceField(queryset=Role.objects.all(), widget=forms.CheckboxSelectMultiple, label='Select the roles you identify with:')

class CauseForm(forms.Form):
    causes = forms.ModelMultipleChoiceField(queryset=Cause.objects.all(), widget=forms.CheckboxSelectMultiple, label='Select the causes you care about:')

