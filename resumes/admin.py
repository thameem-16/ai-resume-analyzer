from django.contrib import admin

from .models import Analysis, JobDescription, Resume


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "file", "uploaded_at")
    list_filter = ("uploaded_at",)
    search_fields = ("user__username", "extracted_text")


@admin.register(JobDescription)
class JobDescriptionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "created_at")
    list_filter = ("created_at",)
    search_fields = ("title", "raw_text", "user__username")


@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "resume",
        "job_description",
        "status",
        "match_score",
        "created_at",
        "completed_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("ai_feedback", "resume__user__username")
