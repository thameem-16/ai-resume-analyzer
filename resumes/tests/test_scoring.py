from resumes.scoring import calculate_match_score


def test_perfect_match():
    resume = "I have experience with Python, Django, and PostgreSQL."
    jd = "Looking for a developer skilled in Python, Django, and PostgreSQL."
    score, missing = calculate_match_score(resume, jd)
    assert score == 100
    assert missing == []


def test_partial_match():
    resume = "I know Python and Django."
    jd = "We need Python, Django, AWS, and Docker experience."
    score, missing = calculate_match_score(resume, jd)
    assert score == 50
    assert set(missing) == {"AWS", "Docker"}


def test_no_match():
    resume = "I enjoy painting and hiking."
    jd = "Looking for someone skilled in Python and Django."
    score, missing = calculate_match_score(resume, jd)
    assert score == 0
    assert set(missing) == {"Python", "Django"}


def test_jd_with_no_recognized_skills_returns_full_score():
    """Edge case: if the JD has no recognizable skills, nothing can be 'missing'."""
    resume = "I have some experience."
    jd = "We want a hardworking, friendly team player."
    score, missing = calculate_match_score(resume, jd)
    assert score == 100
    assert missing == []


def test_case_insensitive_matching():
    resume = "Experienced with python and DJANGO."
    jd = "Need PYTHON and django skills."
    score, missing = calculate_match_score(resume, jd)
    assert score == 100
    assert missing == []


def test_multiword_skill_matches_correctly():
    """Edge case: multi-word skills like 'REST API' shouldn't be split into separate words."""
    resume = "Built REST API endpoints using Django."
    jd = "Must have REST API experience."
    score, missing = calculate_match_score(resume, jd)
    assert score == 100
    assert missing == []