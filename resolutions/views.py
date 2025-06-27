import os
import tempfile
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ConsumerResolutionForm, OtherRolesForm, ApplicableResolutionsForm
from .models import Role, Domain, Cause, Resolution
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from uuid import uuid4
from dashboard.models import PDFDownloadLog

# Create your views here.

# NEW WORKFLOW VIEWS

def select_consumer_resolutions(request):
    """Step 1: Select consumer resolutions grouped by domain"""
    if request.method == "POST":
        form = ConsumerResolutionForm()
        selected_resolution_ids = form.get_selected_resolutions(request.POST)
        request.session["consumer_resolution_ids"] = selected_resolution_ids
        return redirect("resolutions:select_other_roles")
    
    # Get consumer role and its resolutions
    try:
        consumer_role = Role.objects.get(name__iexact='consumer')
        consumer_resolutions = Resolution.objects.filter(role=consumer_role).select_related('domain').order_by('domain__name', 'label', 'positive_action')
        
        # Group resolutions by domain
        domains_with_resolutions = []
        current_domain = None
        current_resolutions = []
        
        for resolution in consumer_resolutions:
            domain_name = resolution.domain.name if resolution.domain else 'Other'
            
            if current_domain != domain_name:
                # Save previous domain if it exists
                if current_domain is not None:
                    domains_with_resolutions.append({
                        'domain': current_domain,
                        'resolutions': current_resolutions
                    })
                # Start new domain
                current_domain = domain_name
                current_resolutions = []
            
            current_resolutions.append(resolution)
        
        # Add the last domain
        if current_domain is not None:
            domains_with_resolutions.append({
                'domain': current_domain,
                'resolutions': current_resolutions
            })
            
    except Role.DoesNotExist:
        domains_with_resolutions = []
    
    context = {
        "domains_with_resolutions": domains_with_resolutions,
    }
    
    return render(request, "resolutions/select-consumer-resolutions.html", context)


def select_other_roles(request):
    """Step 2: Select roles that have resolutions related to selected consumer resolutions"""
    consumer_resolution_ids = request.session.get("consumer_resolution_ids", [])
    
    if not consumer_resolution_ids:
        return redirect("resolutions:select_consumer_resolutions")
    
    # Get selected consumer resolutions
    consumer_resolutions = Resolution.objects.filter(id__in=consumer_resolution_ids)
    
    # Find all roles that have resolutions that reference the selected consumer resolutions
    available_roles = set()
    
    # Find resolutions that have any of the selected consumer resolutions in their related_resolutions
    for consumer_res in consumer_resolutions:
        # Find resolutions that have this consumer resolution as a related resolution
        resolutions_with_this_consumer_res = Resolution.objects.filter(related_resolutions=consumer_res)
        for resolution in resolutions_with_this_consumer_res:
            available_roles.add(resolution.role)
        # Also include the consumer role itself
        available_roles.add(consumer_res.role)
    
    if request.method == "POST":
        form = OtherRolesForm(available_roles, request.POST)
        if form.is_valid():
            selected_role_ids = [int(id) for id in form.cleaned_data.get('roles', [])]
            request.session["selected_role_ids"] = selected_role_ids
            return redirect("resolutions:further_personalise_list")
    else:
        form = OtherRolesForm(available_roles)
    
    context = {
        "form": form,
        "available_roles": available_roles,
        "all_roles": Role.objects.all().order_by('name'),
    }
    
    return render(request, "resolutions/select-other-roles.html", context)


def further_personalise_list(request):
    """Step 3: Final selection of roles and their associated resolutions"""
    consumer_resolution_ids = request.session.get("consumer_resolution_ids", [])
    selected_role_ids = request.session.get("selected_role_ids", [])
    
    if not consumer_resolution_ids or not selected_role_ids:
        return redirect("resolutions:select_consumer_resolutions")
    
    # Get selected consumer resolutions and roles
    consumer_resolutions = Resolution.objects.filter(id__in=consumer_resolution_ids)
    selected_roles = Role.objects.filter(id__in=selected_role_ids)
    
    # Build data structure for roles and their associated resolutions
    roles_with_resolutions = []
    
    for role in selected_roles:
        role_resolutions_set = set()  # Use set to avoid duplicates
        
        if role.name.lower() == 'consumer':
            # For consumer role, include the originally selected resolutions
            consumer_role_resolutions = consumer_resolutions.filter(role=role)
            role_resolutions_set.update(consumer_role_resolutions)
        else:
            # For other roles, find resolutions that reference the selected consumer resolutions
            for consumer_res in consumer_resolutions:
                # Find resolutions of this role that have the consumer resolution as related
                resolutions_with_consumer_ref = Resolution.objects.filter(
                    role=role, 
                    related_resolutions=consumer_res
                )
                role_resolutions_set.update(resolutions_with_consumer_ref)
        
        # Convert set back to list
        role_resolutions = list(role_resolutions_set)
        
        if role_resolutions:
            roles_with_resolutions.append({
                'role': role,
                'resolutions': role_resolutions
            })
    
    if request.method == "POST":
        form = ApplicableResolutionsForm(roles_with_resolutions, request.POST)
        if form.is_valid():
            selected_role_ids, selected_resolution_ids = form.get_selected_items()
            request.session['final_role_ids'] = selected_role_ids
            request.session['final_resolution_ids'] = selected_resolution_ids
            return redirect("resolutions:personal_list_new")
    else:
        form = ApplicableResolutionsForm(roles_with_resolutions)
    
    context = {
        "form": form,
        "roles_with_resolutions": roles_with_resolutions,
    }
    
    return render(request, "resolutions/further-personalise-list.html", context)


def personal_list_new(request):
    """Step 4: Display the personal list"""
    final_role_ids = request.session.get('final_role_ids', [])
    final_resolution_ids = request.session.get('final_resolution_ids', [])
    
    if not final_role_ids or not final_resolution_ids:
        return redirect("resolutions:select_consumer_resolutions")
    
    roles = Role.objects.filter(id__in=final_role_ids)
    resolutions = Resolution.objects.filter(id__in=final_resolution_ids)
    
    # Group resolutions by role for better display
    roles_with_resolutions = []
    for role in roles:
        role_resolutions = resolutions.filter(role=role)
        if role_resolutions:
            roles_with_resolutions.append({
                'role': role,
                'resolutions': role_resolutions
            })
    
    context = {
        "roles": roles,
        "resolutions": resolutions,
        "roles_with_resolutions": roles_with_resolutions,
    }
    
    return render(request, "resolutions/personal-list-new.html", context)

def generate_pdf(request):
    # Fetch IDs from session - only use new workflow keys now
    final_role_ids = request.session.get('final_role_ids', [])
    final_resolution_ids = request.session.get('final_resolution_ids', [])

    # Fetch Role and Resolution instances based on retrieved IDs
    roles = Role.objects.filter(id__in=final_role_ids)
    resolutions = Resolution.objects.filter(id__in=final_resolution_ids).distinct()

    # Log the PDF download
    log = PDFDownloadLog.objects.create()
    log.roles.set(roles)
    log.resolutions.set(resolutions)
    log.save()

    # Render the HTML content
    html_content = render_to_string('resolutions/pdf-template.html', {'roles': roles, 'resolutions': resolutions})

    # Generate PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="personal_resolutions.pdf"'

    # Create a temporary file to hold the PDF
    fd, path = tempfile.mkstemp()
    try:
        # Generate PDF and save to the temporary file
        HTML(string=html_content).write_pdf(target=path)
        with open(path, 'rb') as pdf_file:
            response.write(pdf_file.read())
    finally:
        os.close(fd)  # Close the file descriptor
        os.remove(path)  # Delete the temporary file

    return response

def introduction(request):
    """Introduction page explaining the resolution workflow"""
    return render(request, "resolutions/introduction.html")