from django.urls import path
from .views import HomePageView, AboutPageView, VulnerabilitiesPageView, PrivacyPageView, CopyrightPageView, AccessibilityPageView

urlpatterns = [
    path("about/", AboutPageView.as_view(), name="about"),
    path("", HomePageView.as_view(), name="home"),
    path("vulnerabilities/", VulnerabilitiesPageView.as_view(), name="vulnerabilities"),
    path("privacy/", PrivacyPageView.as_view(), name="privacy"),
    path("copyright/", CopyrightPageView.as_view(), name="copyright"),
    path("accessibility/", AccessibilityPageView.as_view(), name="accessibility"),
]

