from django.views.generic import TemplateView

# Create your views here.
class HomePageView(TemplateView):
    template_name = "pages/home.html"

class AboutPageView(TemplateView):
    template_name = "pages/about.html"

class VulnerabilitiesPageView(TemplateView):
    template_name = "pages/vulnerabilities.html"

class PrivacyPageView(TemplateView):
    template_name = "pages/privacy.html"

class CopyrightPageView(TemplateView):
    template_name = "pages/copyright.html"

class AccessibilityPageView(TemplateView):
    template_name = "pages/accessibility.html"