import os
import tempfile
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)  # Redirect is a new import to save the Roles and Causes in the session and then use these values to filter the Resolutions.
from .forms import RoleForm, CauseForm
from .models import Role, Cause, Resolution
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from uuid import uuid4

# Create your views here.
def select_roles(request):
    if request.method == "POST":
        form = RoleForm(request.POST)
        if form.is_valid():
            roles = form.cleaned_data["roles"]  # Get the Role instances
            role_names = [
                role.name for role in roles
            ]  # Get the names from the Role instances
            request.session["role_names"] = (
                role_names  # Save the Role names in the session.
            )
            return redirect("resolutions:select_causes")
    else:
        form = RoleForm()
    return render(request, "resolutions/select-roles.html", {"form": form})


def select_causes(request):
    if request.method == "POST":
        form = CauseForm(request.POST)
        if form.is_valid():
            causes = form.cleaned_data["causes"]  # Get the Cause instances
            cause_names = [
                cause.name for cause in causes
            ]  # Get the names from the Cause instances
            request.session["cause_names"] = (
                cause_names  # Save the Cause names in the session.
            )
            return redirect("resolutions:select_resolutions")
    else:
        form = CauseForm()
    return render(request, "resolutions/select-causes.html", {"form": form})


def select_resolutions(request):
    role_names = request.session.get(
        "role_names", []
    )  # Get the Role names from the session
    cause_names = request.session.get(
        "cause_names", []
    )  # Get the Cause names from the session
    # Get the Role and Cause instances based on the names
    roles = Role.objects.filter(name__in=role_names)
    causes = Cause.objects.filter(name__in=cause_names)

    roles_with_resolutions = []
    for role in roles:
        # Filter the Resolution instances based on the selected role and causes
        resolutions = Resolution.objects.filter(role=role, cause__in=causes)
        roles_with_resolutions.append(
            {
                "role": role,
                "resolutions": resolutions,
            }
        )

    context = {
        "roles_with_resolutions": roles_with_resolutions,
        "causes": causes,
    }

    return render(request, "resolutions/select-resolutions.html", context)

def personal_list(request):
    if request.method == "POST":
        included_roles = request.POST.getlist("include_role")
        included_resolutions = request.POST.getlist("include_resolution")

        # Save selected IDs in session for later retrieval in generate_pdf
        request.session['included_roles_ids'] = included_roles
        request.session['included_resolutions_ids'] = included_resolutions

        roles = Role.objects.filter(id__in=included_roles)
        resolutions = Resolution.objects.filter(id__in=included_resolutions)

        return render(
            request,
            "resolutions/personal-list.html",
            {
                "roles": roles,
                "resolutions": resolutions,
            },
        )

def generate_pdf(request):
    # Fetch IDs from session
    included_roles_ids = request.session.get('included_roles_ids', [])
    included_resolutions_ids = request.session.get('included_resolutions_ids', [])

    # Fetch Role and Resolution instances based on retrieved IDs
    roles = Role.objects.filter(id__in=included_roles_ids)
    resolutions = Resolution.objects.filter(id__in=included_resolutions_ids)

    # Log the types of the data being passed into the table cells
    for role in roles:
        print(f"Role: {role.name} (type: {type(role.name)})")
        for resolution in resolutions:
            if resolution.role.id == role.id:
                print(f"Resolution: {resolution.positive_action} (type: {type(resolution.positive_action)})")

    # Render the HTML content
    html_content = render_to_string('resolutions/pdf-template.html', {'roles': roles, 'resolutions': resolutions})

    # Generate PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="personal_resolutions.pdf"'

    # Create a temporary file to hold the PDF
    fd, path = tempfile.mkstemp()
    try:
        # Generate PDF and save to the temporary file
        with open(path, 'w+b') as pdf_file:
            pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)
            pdf_file.seek(0)
            response.write(pdf_file.read())

            # Check for errors in PDF generation
            if pisa_status.err:
                raise Exception("Error generating PDF")

    except Exception as e:
        # Log the error and HTML content for debugging
        print(f"Error generating PDF: {e}")
        print(f"HTML content: {html_content}")
        return HttpResponse("There was an error generating the PDF.", status=500)

    finally:
        os.close(fd)  # Close the file descriptor
        os.remove(path)  # Delete the temporary file

    return response