"""Smoke tests for ResumeIQ backend."""

from resumeiq.analyzer import analyze_ats
from resumeiq.coach import answer_coach_question
from resumeiq.evidence import build_skill_evidence
from resumeiq.matcher import keyword_in_text, match_skills, validate_role


def test_no_java_in_javascript():
    assert not keyword_in_text("java", "I use javascript daily")
    assert keyword_in_text("javascript", "I use javascript daily")


def test_no_api_in_capital():
    assert not keyword_in_text("api", "capital markets")
    assert keyword_in_text("api", "Built REST API endpoints")


def test_evidence_gate():
    text = "Built REST API endpoints using Python and FastAPI. Deployed with Docker containers."
    matched, _ = match_skills(["python", "docker", "kubernetes"], text)
    evidence, verified = build_skill_evidence(text, matched)
    assert "python" in verified
    assert "kubernetes" not in verified
    assert all(len(e["evidence"]) >= 18 for e in evidence)
    assert all("detected in resume" not in e["evidence"].lower() for e in evidence)


def test_analyzer_output_shape():
    sample = """
    SKILLS: Python, JavaScript, React, Git, SQL, REST API, Testing
    Built REST API endpoints using Python and FastAPI for internal tooling.
    Developed React dashboards with JavaScript and used Git for version control.
    Wrote unit tests using pytest. Bachelor of Computer Science.
    """
    result = analyze_ats(sample, "Software Engineer", "test.pdf")
    required = [
        "skills_found", "missing_skills", "skill_evidence", "weak_skills",
        "interview_readiness", "match_percentage", "recruiter_feedback",
        "interview_questions",
    ]
    for key in required:
        assert key in result, f"Missing {key}"
    assert len(result["skill_evidence"]) == len(result["skills_found"])


def test_validate_role():
    assert validate_role("Software Engineer") == "Software Engineer"
    try:
        validate_role("Invalid Role")
        raise AssertionError("Should have raised")
    except ValueError:
        pass


def test_coach_with_context():
    context = {
        "role": "Software Engineer",
        "ats_score": 62,
        "match_percentage": 55,
        "interview_readiness": "Intermediate",
        "skills_found": ["python", "react"],
        "missing_skills": ["docker", "kubernetes"],
        "weak_skills": ["sql"],
        "recruiter_feedback": ["No containerization experience detected."],
        "recommendations": ["Add missing keywords: docker, kubernetes"],
    }
    answer = answer_coach_question("What are my biggest gaps?", "Software Engineer", context)
    assert "docker" in answer.lower()
    assert "kubernetes" in answer.lower()

    score_answer = answer_coach_question("Explain my ATS score", "Software Engineer", context)
    assert "62" in score_answer
    assert "Intermediate" in score_answer


def test_coach_no_hallucination_claim():
    answer = answer_coach_question("How does this work?", "Software Engineer", None)
    assert "rule-based" in answer.lower()
    assert "not generative" in answer.lower() or "never invent" in answer.lower()


if __name__ == "__main__":
    test_no_java_in_javascript()
    test_no_api_in_capital()
    test_evidence_gate()
    test_analyzer_output_shape()
    test_validate_role()
    test_coach_with_context()
    test_coach_no_hallucination_claim()
    print("All smoke tests passed")
