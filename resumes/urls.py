from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AnalysisViewSet, JobDescriptionViewSet, ResumeViewSet

router = DefaultRouter()
router.register("resumes", ResumeViewSet)
router.register("job-descriptions", JobDescriptionViewSet)
router.register("analyses", AnalysisViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
