from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .auth_views import LoginView, RegisterView
from .views import AnalysisViewSet, JobDescriptionViewSet, ResumeViewSet

router = DefaultRouter()
router.register("resumes", ResumeViewSet)
router.register("job-descriptions", JobDescriptionViewSet)
router.register("analyses", AnalysisViewSet)

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("", include(router.urls)),
]