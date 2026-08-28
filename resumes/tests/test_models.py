import pytest
from resumes.models import Resume, JobDescription, Analysis


@pytest.mark.django_db
def test_job_description_str_uses_title(test_user):
    jd = JobDescription.objects.create(
        user=test_user, title="Backend Dev", raw_text="Python required."
    )
    assert str(jd) == "Backend Dev"


@pytest.mark.django_db
def test_analysis_default_status_is_pending(test_user):
    jd = JobDescription.objects.create(
        user=test_user, title="Backend Dev", raw_text="Python required."
    )
    resume = Resume.objects.create(user=test_user, extracted_text="Python experience.")
    analysis = Analysis.objects.create(resume=resume, job_description=jd)
    assert analysis.status == "pending"


@pytest.mark.django_db
def test_analysis_missing_keywords_defaults_to_empty_list(test_user):
    jd = JobDescription.objects.create(
        user=test_user, title="Backend Dev", raw_text="Python required."
    )
    resume = Resume.objects.create(user=test_user, extracted_text="Python experience.")
    analysis = Analysis.objects.create(resume=resume, job_description=jd)
    assert analysis.missing_keywords == []