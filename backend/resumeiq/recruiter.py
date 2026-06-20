"""Honest recruiter feedback — hiring-relevant only, no motivational language."""

from resumeiq.constants import CRITICAL_SKILLS, SKILL_REJECTION_REASONS


def generate_recruiter_feedback(
    missing_skills: list[str],
    weak_skills: list[str],
    role: str,
    project_score: int,
    experience_score: int,
) -> list[str]:
    """Generate rejection-risk statements from detected gaps only."""
    feedback: list[str] = []
    critical = set(CRITICAL_SKILLS.get(role, []))
    seen: set[str] = set()

    for skill in missing_skills:
        if skill in critical and skill in SKILL_REJECTION_REASONS:
            msg = SKILL_REJECTION_REASONS[skill]
            if msg not in seen:
                feedback.append(msg)
                seen.add(msg)

    for skill in missing_skills:
        if skill not in critical and skill in SKILL_REJECTION_REASONS:
            msg = SKILL_REJECTION_REASONS[skill]
            if msg not in seen:
                feedback.append(msg)
                seen.add(msg)
        if len(feedback) >= 6:
            break

    for skill in weak_skills:
        feedback.append(
            f'"{skill.title()}" appears only briefly in the resume with limited context. '
            "Recruiters may question depth of practical experience."
        )
        if len(feedback) >= 8:
            break

    if project_score < 50:
        feedback.append(
            "No quantified project outcomes detected. Hiring managers expect impact metrics "
            "(e.g. 'reduced API latency by 40%', 'served 10k daily users')."
        )
    if experience_score < 40:
        feedback.append(
            "Limited professional experience signals detected. "
            "This resume is likely to be screened for entry-level or internship positions only."
        )

    return feedback[:8]


def build_recruiter_summary(role: str, ats_score: int, match_pct: int) -> str:
    if ats_score >= 80:
        return (
            f"Strong candidate for {role}. {match_pct}% keyword match with solid "
            "resume structure. Recommended for interview stage."
        )
    if ats_score >= 60:
        return (
            f"Moderate match for {role} ({match_pct}% keyword coverage). "
            "Key gaps exist. Resume requires targeted revision before applying."
        )
    return (
        f"Weak match for {role} ({match_pct}% keyword coverage). "
        "Significant gaps detected. Substantial improvements required."
    )
