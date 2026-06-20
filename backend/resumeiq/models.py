"""Pydantic request/response models."""

from pydantic import BaseModel, Field


class SkillEvidence(BaseModel):
    skill: str
    evidence: str
    strength: str  # "strong" | "moderate" | "weak"


class InterviewQuestionSet(BaseModel):
    skill: str
    questions: list[str]


class ATSResponse(BaseModel):
    filename: str
    role: str
    ats_score: int
    keyword_score: int
    project_score: int
    experience_score: int
    education_score: int
    formatting_score: int
    skills_found: list[str]
    missing_skills: list[str]
    strengths: list[str]
    weaknesses: list[str]
    recommendations: list[str]
    recruiter_summary: str
    feedback: list[str]
    skill_evidence: list[SkillEvidence] = Field(default_factory=list)
    weak_skills: list[str] = Field(default_factory=list)
    interview_readiness: str
    match_percentage: int
    recruiter_feedback: list[str] = Field(default_factory=list)
    interview_questions: list[InterviewQuestionSet] = Field(default_factory=list)


class CoachContext(BaseModel):
    """Optional analysis snapshot for context-aware coach answers."""

    role: str = ""
    ats_score: int | None = None
    match_percentage: int | None = None
    interview_readiness: str | None = None
    skills_found: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    weak_skills: list[str] = Field(default_factory=list)
    recruiter_feedback: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)


class AICoachRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)
    role: str = ""
    context: CoachContext | None = None


class AICoachResponse(BaseModel):
    answer: str


class ErrorResponse(BaseModel):
    detail: str
    error_code: str | None = None


class HealthResponse(BaseModel):
    status: str
    version: str
