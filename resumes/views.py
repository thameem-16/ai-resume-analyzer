from rest_framework import viewsets
from rest_framework.parsers import FormParser, MultiPartParser

from .models import Analysis, JobDescription, Resume
from .ai_client import get_ai_feedback
from .scoring import calculate_match_score
from .serializers import (
    AnalysisSerializer,
    JobDescriptionSerializer,
    ResumeSerializer,
)
from .utils import extract_text_from_pdf


class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        resume = serializer.save(user=self.request.user)
        resume.extracted_text = extract_text_from_pdf(resume.file)
        resume.save(update_fields=["extracted_text"])


class JobDescriptionViewSet(viewsets.ModelViewSet):
    queryset = JobDescription.objects.all()
    serializer_class = JobDescriptionSerializer

    def get_queryset(self):
        return JobDescription.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AnalysisViewSet(viewsets.ModelViewSet):
    queryset = Analysis.objects.select_related("resume", "job_description").all()
    serializer_class = AnalysisSerializer

    def get_queryset(self):
        return Analysis.objects.filter(resume__user=self.request.user)

    def perform_create(self, serializer):
        analysis = serializer.save()
        resume_text = analysis.resume.extracted_text
        jd_text = analysis.job_description.raw_text

        from django.utils import timezone
        score, missing = calculate_match_score(resume_text, jd_text)
        feedback = get_ai_feedback(resume_text, jd_text, missing)

        analysis.match_score = score
        analysis.missing_keywords = missing
        analysis.ai_feedback = feedback
        analysis.status = Analysis.Status.COMPLETED
        analysis.completed_at = timezone.now()
        analysis.save(update_fields=[
            "match_score", "missing_keywords", "ai_feedback",
            "status", "completed_at",
        ])