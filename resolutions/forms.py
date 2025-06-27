from django import forms
from .models import Role, Domain, Cause, Resolution


class ConsumerResolutionForm(forms.Form):
    """Form for selecting consumer resolutions grouped by domain - processes raw POST data"""
    
    def __init__(self, consumer_resolutions_by_domain=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # This form doesn't need dynamic fields - it processes raw POST data
        self.consumer_resolutions_by_domain = consumer_resolutions_by_domain or {}

    def get_selected_resolutions(self, post_data):
        """Return list of selected resolution IDs from POST data"""
        return [int(id) for id in post_data.getlist('include_resolution')]


class OtherRolesForm(forms.Form):
    """Form for selecting other roles based on available related resolutions"""
    def __init__(self, available_roles=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if available_roles:
            # Create choices with enabled/disabled status
            choices = []
            for role in Role.objects.all().order_by('name'):
                if role in available_roles:
                    choices.append((role.id, role.name))
            
            self.fields['roles'] = forms.MultipleChoiceField(
                choices=choices,
                widget=forms.CheckboxSelectMultiple,
                label="Select the roles you identify with:",
                required=False
            )


class ApplicableResolutionsForm(forms.Form):
    """Form for final selection of roles and resolutions"""
    def __init__(self, roles_with_resolutions=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if roles_with_resolutions:
            # Create fields for each role and its resolutions
            for role_data in roles_with_resolutions:
                role = role_data['role']
                resolutions = role_data['resolutions']
                
                # Role checkbox
                role_field_name = f'include_role_{role.id}'
                self.fields[role_field_name] = forms.BooleanField(
                    label=f"Include role: {role.name}",
                    required=False,
                    initial=True
                )
                
                # Resolution checkboxes for this role
                for resolution in resolutions:
                    res_field_name = f'include_resolution_{resolution.id}'
                    self.fields[res_field_name] = forms.BooleanField(
                        label=resolution.display_label,
                        required=False,
                        initial=True
                    )

    def get_selected_items(self):
        """Return selected role and resolution IDs"""
        selected_roles = []
        selected_resolutions = []
        
        for field_name, value in self.cleaned_data.items():
            if value:  # If checkbox is checked
                if field_name.startswith('include_role_'):
                    role_id = int(field_name.split('_')[-1])
                    selected_roles.append(role_id)
                elif field_name.startswith('include_resolution_'):
                    resolution_id = int(field_name.split('_')[-1])
                    selected_resolutions.append(resolution_id)
        
        return selected_roles, selected_resolutions
