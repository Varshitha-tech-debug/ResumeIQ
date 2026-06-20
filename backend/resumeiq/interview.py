"""Deterministic interview question lookup — no AI generation."""

from resumeiq.constants import INTERVIEW_QUESTIONS


def _fallback_questions(skill: str) -> list[str]:
    return [
        f"What is {skill} and when would you use it in a real project?",
        f"Describe a specific project or task where you applied {skill}.",
        f"What are the main advantages of {skill} compared to its alternatives?",
    ]


def get_interview_readiness(match_pct: int) -> str:
    if match_pct >= 70:
        return "Ready"
    if match_pct >= 40:
        return "Intermediate"
    return "Beginner"


def get_interview_questions(missing_skills: list[str]) -> list[dict]:
    """Return fixed interview questions for missing skills."""
    result: list[dict] = []
    for skill in missing_skills[:6]:
        questions = INTERVIEW_QUESTIONS.get(skill, _fallback_questions(skill))
        result.append({"skill": skill, "questions": questions})
    return result
