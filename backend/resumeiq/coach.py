"""Rule-based career coach — structured knowledge only, no LLM."""

from resumeiq.constants import CRITICAL_SKILLS, ROLE_KEYWORDS


def _format_list(items: list[str], limit: int = 5) -> str:
    if not items:
        return "none detected"
    shown = items[:limit]
    text = ", ".join(shown)
    if len(items) > limit:
        text += f" (+{len(items) - limit} more)"
    return text


def _answer_from_context(question: str, role: str, ctx: dict) -> str | None:
    """Return a context-specific answer when analysis data is available."""
    q = question.lower()
    target_role = role or ctx.get("role") or "your target role"

    score = ctx.get("ats_score")
    match_pct = ctx.get("match_percentage")
    readiness = ctx.get("interview_readiness")
    missing = ctx.get("missing_skills") or []
    weak = ctx.get("weak_skills") or []
    matched = ctx.get("skills_found") or []
    recruiter = ctx.get("recruiter_feedback") or []
    recommendations = ctx.get("recommendations") or []
    critical = set(CRITICAL_SKILLS.get(target_role, []))
    critical_missing = [s for s in missing if s in critical]

    if any(w in q for w in ["score", "my result", "my analysis", "how did i", "why is my"]):
        if score is None:
            return None
        lines = [
            f"Your ATS score is {score}/100 for {target_role}.",
            f"Keyword match: {match_pct}% ({len(matched)} skills with evidence).",
            f"Interview readiness: {readiness}.",
        ]
        if missing:
            lines.append(f"Top gaps: {_format_list(missing)}.")
        if weak:
            lines.append(f"Weak signals: {_format_list(weak)}.")
        return " ".join(lines)

    if any(w in q for w in ["missing", "gap", "gaps", "lack", "don't have", "do not have"]):
        if not missing:
            return (
                f"No missing {target_role} keywords detected in your last analysis. "
                "Verify skills appear in project bullets, not only in a skills list."
            )
        msg = f"You are missing {len(missing)} role keywords: {_format_list(missing, 8)}."
        if critical_missing:
            msg += f" Critical gaps for hiring: {_format_list(critical_missing)}."
        return msg

    if any(w in q for w in ["weak", "weak signal", "weak skills"]):
        if not weak:
            return "No weak skill signals in your last analysis — matched skills had usable context."
        return (
            f"Weak signals in your resume: {_format_list(weak)}. "
            "These keywords appear with shallow context (e.g. 'familiar with'). "
            "Move each into a project bullet with concrete usage."
        )

    if any(w in q for w in ["recruiter", "reject", "risk", "concern", "honest"]):
        if recruiter:
            top = recruiter[:3]
            return "Recruiter-risk notes from your analysis: " + " ".join(
                f"({i + 1}) {item}" for i, item in enumerate(top)
            )
        return None

    if any(w in q for w in ["next", "what should i", "what do i", "priority", "fix first", "focus"]):
        if recommendations:
            top = recommendations[:4]
            return "Priority actions from your analysis: " + " ".join(
                f"({i + 1}) {item}" for i, item in enumerate(top)
            )
        return None

    if any(w in q for w in ["matched", "skills found", "what skills", "strengths"]):
        if matched:
            return (
                f"Skills verified with resume evidence: {_format_list(matched, 10)}. "
                "Each includes a quoted sentence from your PDF — no guessed skills."
            )
        return None

    if any(w in q for w in ["interview", "ready", "readiness", "prepare"]):
        if readiness and match_pct is not None:
            return (
                f"Your interview readiness is '{readiness}' ({match_pct}% keyword match). "
                "Prepare for questions on missing skills shown in your dashboard. "
                "Be ready to explain every project and skill listed on your resume."
            )
        return None

    return None


def answer_coach_question(question: str, role: str, context: dict | None = None) -> str:
    """Return a deterministic answer based on keywords and optional analysis context."""
    q = question.lower().strip()
    target_role = role.strip() or (context or {}).get("role", "") or "your target role"

    if context:
        contextual = _answer_from_context(question, target_role, context)
        if contextual:
            return contextual

    if "hallucin" in q or "how does this work" in q or "deterministic" in q:
        return (
            "Career Coach is rule-based — not generative AI. "
            "It routes your question to fixed hiring guidance and, when available, "
            "uses your uploaded analysis (scores, gaps, evidence). "
            "It will never invent skills or experience not in your resume."
        )

    if "ats" in q:
        return (
            "ATS scoring uses: 40% keyword match (with evidence), 20% project signals, "
            "20% experience signals, 10% education, 10% formatting. "
            "Same resume + role always produces the same score."
        )

    if any(w in q for w in ["reject", "rejection", "why"]):
        return (
            f"Common rejection reasons for {target_role} roles: "
            "(1) Missing critical keywords. "
            "(2) Skills listed without project evidence. "
            "(3) No quantified outcomes. "
            "(4) Weak phrasing ('familiar with', 'basic'). "
            "Upload a resume to see role-specific gaps."
        )

    if any(w in q for w in ["improve", "better", "boost", "increase"]):
        return (
            f"To improve for {target_role}: "
            "(1) Add missing keywords into project bullets. "
            "(2) Quantify impact with numbers. "
            "(3) Replace weak skill phrasing with demonstrated usage. "
            "(4) Add GitHub or deployment links. "
            "Run an analysis first for targeted recommendations."
        )

    if any(w in q for w in ["skill", "keyword", "technology", "learn"]):
        keywords = ROLE_KEYWORDS.get(target_role, [])
        top = ", ".join(keywords[:10]) if keywords else "relevant technical skills"
        return (
            f"Core {target_role} keywords tracked by ResumeIQ: {top}. "
            "Only list a skill if you can quote a project or job bullet using it."
        )

    if any(w in q for w in ["project", "github", "portfolio"]):
        return (
            "Strong project bullets include: purpose, stack, your contribution, "
            "measurable outcome, and a link. "
            "Example: 'Built FastAPI service handling 2k req/min; deployed with Docker on AWS.'"
        )

    if any(w in q for w in ["interview", "ready", "prepare"]):
        return (
            "Interview readiness tiers: Below 40% = Beginner, 40–69% = Intermediate, 70%+ = Ready. "
            "Practice questions for your missing skills and prepare to defend every line on your resume."
        )

    if any(w in q for w in ["weak", "signal", "evidence"]):
        return (
            "A weak signal means the keyword appears without strong context. "
            "Fix by embedding the skill in a project bullet with concrete usage — "
            "not in a standalone skills list."
        )

    if any(w in q for w in ["summary", "objective", "headline"]):
        return (
            f"Write a 2–3 line summary targeting {target_role}: "
            "role title, years of experience, top 3 verified skills, and one quantified achievement. "
            "Avoid generic adjectives ('passionate', 'hardworking')."
        )

    if any(w in q for w in ["format", "layout", "section", "structure"]):
        return (
            "Use standard sections: Summary, Skills, Experience, Projects, Education. "
            "One column, simple fonts, no tables or graphics that break PDF text extraction."
        )

    return (
        f"I can help with {target_role} resume strategy using rule-based guidance. "
        "Ask about: your score, missing skills, weak signals, recruiter risks, or interview prep. "
        "Upload and analyze a resume for answers tied to your actual results."
    )
