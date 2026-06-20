"""Core ATS analysis orchestrator — deterministic, explainable."""

from resumeiq.constants import (
    EDUCATION_SIGNALS,
    EXPERIENCE_SIGNALS,
    FORMATTING_SIGNALS,
    PROJECT_SIGNALS,
    ROLE_KEYWORDS,
    SCORE_WEIGHTS,
)
from resumeiq.evidence import build_skill_evidence
from resumeiq.interview import get_interview_questions, get_interview_readiness
from resumeiq.matcher import match_skills, pct, score_signal_hits
from resumeiq.recruiter import build_recruiter_summary, generate_recruiter_feedback


def analyze_ats(text: str, role: str, filename: str) -> dict:
    """
    Compute deterministic ATS analysis from resume text.

    Pipeline:
      1. Set-based keyword matching (word boundaries)
      2. Evidence verification (skills without quotes are rejected)
      3. Weighted scoring from verified matches + section signals
    """
    text_lower = text.lower()
    keywords = ROLE_KEYWORDS[role]

    # Step 1: initial keyword presence check
    candidates, _ = match_skills(keywords, text)

    # Step 2: evidence gate — only verified skills count
    skill_evidence, skills_found = build_skill_evidence(text, candidates)
    skills_found_set = set(skills_found)
    missing_skills = [kw for kw in keywords if kw not in skills_found_set]

    match_pct = pct(len(skills_found), len(keywords))
    keyword_score = match_pct

    proj_hits = score_signal_hits(PROJECT_SIGNALS, text_lower)
    project_score = pct(proj_hits, len(PROJECT_SIGNALS))
    exp_hits = score_signal_hits(EXPERIENCE_SIGNALS, text_lower)
    experience_score = pct(exp_hits, len(EXPERIENCE_SIGNALS))
    edu_hits = score_signal_hits(EDUCATION_SIGNALS, text_lower)
    education_score = pct(edu_hits, len(EDUCATION_SIGNALS))
    fmt_hits = score_signal_hits(FORMATTING_SIGNALS, text_lower)
    formatting_score = pct(fmt_hits, len(FORMATTING_SIGNALS))

    ats_score = round(
        SCORE_WEIGHTS["keyword"] * keyword_score
        + SCORE_WEIGHTS["project"] * project_score
        + SCORE_WEIGHTS["experience"] * experience_score
        + SCORE_WEIGHTS["education"] * education_score
        + SCORE_WEIGHTS["formatting"] * formatting_score
    )

    weak_skills = [e["skill"] for e in skill_evidence if e["strength"] == "weak"]
    interview_readiness = get_interview_readiness(match_pct)

    strengths: list[str] = []
    if keyword_score >= 70:
        strengths.append(f"Strong keyword alignment for {role} ({keyword_score}% match)")
    if project_score >= 70:
        strengths.append("Project experience clearly documented in resume")
    if experience_score >= 70:
        strengths.append("Professional experience section is well-evidenced")
    if education_score >= 70:
        strengths.append("Educational background clearly presented")
    if formatting_score >= 70:
        strengths.append("Resume structure passes ATS section detection")

    weaknesses: list[str] = []
    if keyword_score < 60:
        weaknesses.append(f"Only {match_pct}% of required {role} keywords detected with evidence")
    if project_score < 60:
        weaknesses.append("Project section lacks quantified outcomes or GitHub links")
    if experience_score < 60:
        weaknesses.append("Work experience section signals are weak or absent")
    if weak_skills:
        weaknesses.append(
            f"{len(weak_skills)} skill(s) mentioned with weak context: "
            f"{', '.join(weak_skills[:3])}"
        )

    recommendations: list[str] = []
    if missing_skills[:5]:
        recommendations.append(
            f"Add missing keywords to resume: {', '.join(missing_skills[:5])}"
        )
    if project_score < 70:
        recommendations.append(
            "Add GitHub links and quantify project impact with metrics"
        )
    if experience_score < 70:
        recommendations.append(
            "Use strong action verbs: Led, Built, Deployed, Optimized, Reduced"
        )
    if weak_skills:
        recommendations.append(
            f"Strengthen evidence for: {', '.join(weak_skills[:3])} "
            "— show usage in project context"
        )
    recommendations.append(
        f"Tailor your professional summary specifically for {role} positions"
    )

    recruiter_feedback = generate_recruiter_feedback(
        missing_skills, weak_skills, role, project_score, experience_score
    )
    interview_questions = get_interview_questions(missing_skills)
    recruiter_summary = build_recruiter_summary(role, ats_score, match_pct)

    feedback_legacy = [
        recruiter_summary,
        f"Matched: {', '.join(skills_found) if skills_found else 'None'}",
        f"Missing: {', '.join(missing_skills) if missing_skills else 'None'}",
        f"Focus on {role}-specific projects and technical depth.",
    ]

    return {
        "filename": filename,
        "role": role,
        "ats_score": ats_score,
        "keyword_score": keyword_score,
        "project_score": project_score,
        "experience_score": experience_score,
        "education_score": education_score,
        "formatting_score": formatting_score,
        "skills_found": skills_found,
        "missing_skills": missing_skills,
        "skill_evidence": skill_evidence,
        "weak_skills": weak_skills,
        "interview_readiness": interview_readiness,
        "match_percentage": match_pct,
        "recruiter_feedback": recruiter_feedback,
        "interview_questions": interview_questions,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommendations": recommendations,
        "recruiter_summary": recruiter_summary,
        "feedback": feedback_legacy,
    }
