"""Hardcoded demo fixture — predictable for live presentations."""

DEMO_RESULT: dict = {
    "filename": "demo_resume_alex_chen.pdf",
    "role": "Software Engineer",
    "ats_score": 62,
    "keyword_score": 55,
    "project_score": 75,
    "experience_score": 67,
    "education_score": 90,
    "formatting_score": 85,
    "skills_found": ["python", "javascript", "react", "sql", "git", "api", "rest", "testing"],
    "missing_skills": ["docker", "kubernetes", "system design", "typescript", "aws", "ci/cd", "microservices"],
    "skill_evidence": [
        {"skill": "python", "evidence": "Built 3 REST APIs using Python and FastAPI for internal tooling", "strength": "strong"},
        {"skill": "javascript", "evidence": "Developed interactive dashboards using JavaScript and Chart.js", "strength": "strong"},
        {"skill": "react", "evidence": "Built responsive UI components in React for e-commerce platform", "strength": "strong"},
        {"skill": "sql", "evidence": "Familiar with SQL for basic database queries", "strength": "weak"},
        {"skill": "git", "evidence": "Used Git and GitHub for version control across all projects", "strength": "strong"},
        {"skill": "api", "evidence": "Designed and implemented RESTful APIs consumed by mobile apps", "strength": "strong"},
        {"skill": "rest", "evidence": "Designed and implemented RESTful APIs consumed by mobile apps", "strength": "moderate"},
        {"skill": "testing", "evidence": "Wrote basic unit tests using pytest", "strength": "weak"},
    ],
    "weak_skills": ["sql", "testing"],
    "interview_readiness": "Intermediate",
    "match_percentage": 55,
    "recruiter_feedback": [
        "No containerization experience detected. Docker is a standard requirement for most backend and full-stack engineering roles.",
        "System design not evidenced in any project. Mid-to-senior interviews test this heavily — often as a dedicated round.",
        "TypeScript not shown. Increasingly required at companies with serious frontend codebases.",
        "No CI/CD pipeline experience found. DevOps practices are standard in modern engineering teams.",
        '"Sql" appears only briefly in the resume with limited context. Recruiters may question depth of practical experience.',
        '"Testing" appears only briefly in the resume with limited context. Recruiters may question depth of practical experience.',
    ],
    "interview_questions": [
        {
            "skill": "docker",
            "questions": [
                "What is Docker and how does containerization differ from traditional virtualization?",
                "Write a Dockerfile for a Python FastAPI application. Walk me through each line.",
                "What is the difference between a Docker image and a Docker container?",
            ],
        },
        {
            "skill": "system design",
            "questions": [
                "How would you design a URL shortening service like bit.ly? Walk through components.",
                "Design a notification system that delivers 1 million messages per day.",
                "How would you design a distributed cache to reduce database load?",
            ],
        },
        {
            "skill": "typescript",
            "questions": [
                "What is the difference between 'interface' and 'type' in TypeScript?",
                "Explain TypeScript generics and give a real-world example.",
                "What are TypeScript utility types? Explain Partial, Pick, and Omit.",
            ],
        },
    ],
    "strengths": [
        "Strong Python and API development skills with project evidence",
        "React frontend experience clearly demonstrated",
        "Good educational background — CS degree detected",
        "Well-structured resume with standard section headings",
    ],
    "weaknesses": [
        "Only 55% of required Software Engineer keywords detected",
        "No deployment or DevOps experience detected",
        "2 skills mentioned with weak context: sql, testing",
    ],
    "recommendations": [
        "Add missing keywords: docker, kubernetes, system design, typescript, aws",
        "Add GitHub links and quantify project impact with metrics",
        "Strengthen evidence for: sql, testing — show usage in project context",
        "Set up a CI/CD pipeline (GitHub Actions) for any existing project",
        "Tailor your professional summary specifically for Software Engineer positions",
    ],
    "recruiter_summary": (
        "Moderate match for Software Engineer (55% keyword coverage). "
        "Strong core coding skills but missing DevOps, system design, and TypeScript — "
        "commonly required for backend and full-stack roles."
    ),
    "feedback": [
        "Moderate match for Software Engineer. Key skills missing: docker, kubernetes, system design.",
        "Matched: python, javascript, react, sql, git, api, rest, testing",
        "Missing: docker, kubernetes, system design, typescript, aws, ci/cd, microservices",
        "Focus on Software Engineer-specific projects and technical depth.",
    ],
}
