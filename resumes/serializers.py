from rest_framework import serializers

from .models import Analysis, JobDescription, Resume


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ["id", "user", "file", "extracted_text", "uploaded_at"]
        read_only_fields = ["user", "extracted_text", "uploaded_at"]


class JobDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDescription
        fields = ["id", "user", "title", "raw_text", "created_at"]
        read_only_fields = ["user", "created_at"]


class AnalysisSerializer(serializers.ModelSerializer):
    resume_id = serializers.PrimaryKeyRelatedField(
        queryset=Resume.objects.all(), source="resume", write_only=True,
    )
    job_description_id = serializers.PrimaryKeyRelatedField(
        queryset=JobDescription.objects.all(), source="job_description", write_only=True,
    )

    class Meta:
        model = Analysis
        fields = [
            "id", "resume", "job_description",
            "resume_id", "job_description_id",
            "status", "match_score", "missing_keywords",
            "ai_feedback", "created_at", "completed_at",
        ]
        read_only_fields = [
            "resume", "job_description",
            "status", "match_score", "missing_keywords",
            "ai_feedback", "created_at", "completed_at",
        ]
