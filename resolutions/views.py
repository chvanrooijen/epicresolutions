from django.shortcuts import render, redirect, get_object_or_404 # Redirect is a new import to save the Roles and Causes in the session and then use these values to filter the Resolutions.
from .forms import RoleForm, CauseForm
from .models import Role, Cause, Resolution
from django.http import JsonResponse
from uuid import uuid4

# Create your views here.
def select_role(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            roles = form.cleaned_data['roles']  # Get the Role instances
            role_names = [role.name for role in roles]  # Get the names from the Role instances
            request.session['role_names'] = role_names  # Save the Role names in the session.
            return redirect('resolutions:select_cause')
    else:
        form = RoleForm()
    return render(request, 'resolutions/select_role.html', {'form': form})

def select_cause(request):
    if request.method == 'POST':
        form = CauseForm(request.POST)
        if form.is_valid():
            causes = form.cleaned_data['causes']  # Get the Cause instances
            cause_names = [cause.name for cause in causes]  # Get the names from the Cause instances
            request.session['cause_names'] = cause_names  # Save the Cause names in the session.
            return redirect('resolutions:select_resolutions')
    else:
        form = CauseForm()
    return render(request, 'resolutions/select_cause.html', {'form': form})

def select_resolutions(request):
    role_names = request.session.get('role_names', [])  # Get the Role names from the session
    cause_names = request.session.get('cause_names', [])  # Get the Cause names from the session
    # Get the Role and Cause instances based on the names
    roles = Role.objects.filter(name__in=role_names)
    causes = Cause.objects.filter(name__in=cause_names)

    roles_with_resolutions = []
    for role in roles:
        # Filter the Resolution instances based on the selected role and causes
        resolutions = Resolution.objects.filter(role=role, cause__in=causes)
        roles_with_resolutions.append({
            'role': role,
            'resolutions': resolutions,
        })
    
    context = {
        'roles_with_resolutions': roles_with_resolutions,
        'causes': causes,
    }

    return render(request, 'resolutions/select_resolutions.html', context)

def personal_list(request):
    if request.method == 'POST':
        included_roles = request.POST.getlist('include_role')
        included_resolutions = request.POST.getlist('include_resolution')

        roles = Role.objects.filter(id__in=included_roles)
        resolutions = Resolution.objects.filter(id__in=included_resolutions)

        return render(request, 'resolutions/personal_list.html', {
            'roles': roles,
            'resolutions': resolutions,
        })
    
