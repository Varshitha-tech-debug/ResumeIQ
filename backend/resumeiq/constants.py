"""Role keywords, scoring signals, and recruiter lookup tables."""

ROLE_KEYWORDS: dict[str, list[str]] = {
    "Software Engineer": [
        "python", "java", "javascript", "typescript", "golang", "c++",
        "api", "rest", "graphql", "microservices", "system design",
        "database", "sql", "postgresql", "mongodb", "redis",
        "docker", "kubernetes", "aws", "git", "algorithms", "data structures",
        "testing", "ci/cd", "agile", "design patterns", "scalability",
    ],
    "Frontend Developer": [
        "react", "vue", "angular", "html", "css", "javascript", "typescript",
        "responsive", "webpack", "vite", "sass", "tailwind",
        "accessibility", "animation", "jest", "testing",
        "git", "figma", "redux", "next.js", "seo", "rest api",
    ],
    "Backend Developer": [
        "python", "node", "java", "golang", "fastapi", "django", "express",
        "flask", "spring", "sql", "postgresql", "mongodb",
        "redis", "api", "rest", "graphql", "docker", "kubernetes",
        "aws", "microservices", "testing", "authentication", "security",
    ],
    "Data Analyst": [
        "sql", "excel", "python", "r programming", "powerbi", "tableau", "analytics",
        "statistics", "pandas", "numpy", "visualization", "dashboard",
        "etl", "data cleaning", "reporting", "machine learning",
        "a/b testing", "kpi", "forecasting", "bigquery", "snowflake",
    ],
    "AI Engineer": [
        "python", "machine learning", "deep learning", "tensorflow", "pytorch",
        "scikit-learn", "pandas", "numpy", "nlp", "computer vision",
        "transformers", "llm", "fine-tuning", "neural networks",
        "mlops", "model deployment", "api", "docker",
        "langchain", "vector database", "rag", "hugging face",
    ],
}

SUPPORTED_ROLES: frozenset[str] = frozenset(ROLE_KEYWORDS.keys())

PROJECT_SIGNALS: list[str] = [
    "project", "github", "built", "developed", "deployed",
    "implemented", "created", "designed", "architected", "launched",
]

EXPERIENCE_SIGNALS: list[str] = [
    "experience", "worked", "led", "managed", "engineer", "developer",
    "analyst", "years", "team", "senior", "junior", "internship",
    "collaborated", "delivered", "achieved",
]

EDUCATION_SIGNALS: list[str] = [
    "university", "college", "bachelor", "master", "degree",
    "computer science", "engineering", "gpa", "graduated",
    "b.tech", "b.e.", "m.tech", "coursework",
]

FORMATTING_SIGNALS: list[str] = [
    "summary", "objective", "skills", "education", "experience",
    "projects", "certifications", "achievements", "contact", "email",
]

SECTION_HEADERS: list[str] = [
    "summary", "objective", "profile", "skills", "technical skills",
    "experience", "work experience", "professional experience",
    "education", "projects", "certifications", "achievements",
    "contact", "languages",
]

WEAK_CONTEXT_WORDS: list[str] = [
    "familiar", "basic", "beginner", "learning", "exposure",
    "introduction", "some knowledge", "working knowledge",
    "entry level", "fundamental", "awareness", "little", "beginner level",
]

CRITICAL_SKILLS: dict[str, list[str]] = {
    "Software Engineer": ["docker", "testing", "system design", "git", "algorithms"],
    "Frontend Developer": ["react", "testing", "typescript", "accessibility", "git"],
    "Backend Developer": ["docker", "testing", "security", "postgresql", "api"],
    "Data Analyst": ["sql", "python", "visualization", "statistics"],
    "AI Engineer": ["python", "machine learning", "pytorch", "mlops"],
}

SKILL_REJECTION_REASONS: dict[str, str] = {
    "docker": "No containerization experience detected. Docker is a standard requirement for most backend and full-stack engineering roles.",
    "kubernetes": "No Kubernetes experience found. Required for senior and cloud-native engineering positions.",
    "testing": "No testing practice detected. Production-grade roles expect unit, integration, and coverage discipline.",
    "system design": "System design not evidenced in any project. Mid-to-senior interviews test this heavily — often as a dedicated round.",
    "algorithms": "Data structures and algorithms not demonstrated. Required for FAANG and most product company engineering interviews.",
    "git": "Version control (Git) not explicitly mentioned. This is considered table-stakes for any engineering role.",
    "sql": "No SQL proficiency shown. Required for backend, data, and full-stack roles.",
    "postgresql": "No relational database experience found. PostgreSQL or MySQL knowledge is commonly expected.",
    "security": "No security practices mentioned. Authentication, authorization, and secure coding are expected in backend roles.",
    "react": "React not found or not demonstrated in projects. Core requirement for most frontend roles.",
    "typescript": "TypeScript not shown. Increasingly required at companies with serious frontend codebases.",
    "python": "Python not found. Core requirement for backend and AI engineering roles.",
    "machine learning": "No ML experience detected. Fundamental requirement for AI/ML engineering positions.",
    "pytorch": "PyTorch not found. Standard framework for AI/ML engineering roles.",
    "mlops": "No MLOps or model deployment experience. Required for production AI engineering roles.",
    "api": "API development not clearly demonstrated. REST/GraphQL experience is expected for backend roles.",
    "microservices": "No microservices experience detected. Common architecture requirement for senior backend roles.",
    "aws": "No cloud platform experience found. Cloud skills (AWS/GCP/Azure) are increasingly required.",
    "ci/cd": "No CI/CD pipeline experience found. DevOps practices are standard in modern engineering teams.",
    "accessibility": "No accessibility experience shown. Required for senior frontend, government, and enterprise roles.",
    "fastapi": "FastAPI not found. Core framework for Python backend roles.",
    "django": "No Python web framework experience found. Django or FastAPI expected for Python backend positions.",
    "authentication": "Authentication not mentioned. A fundamental security concern for any backend developer.",
    "r programming": "No R programming experience found. Expected for statistical and analytics-heavy data roles.",
}

INTERVIEW_QUESTIONS: dict[str, list[str]] = {
    "docker": [
        "What is Docker and how does containerization differ from traditional virtualization?",
        "Write a Dockerfile for a Python FastAPI application. Walk me through each line.",
        "What is the difference between a Docker image and a Docker container?",
    ],
    "kubernetes": [
        "What is Kubernetes and what specific problem does it solve over Docker alone?",
        "Explain the difference between a Pod, a Deployment, and a Service in Kubernetes.",
        "How does Kubernetes handle rolling updates and rollbacks?",
    ],
    "sql": [
        "Write a SQL query to find the second highest salary from an employees table.",
        "What is the difference between INNER JOIN, LEFT JOIN, and FULL OUTER JOIN?",
        "Explain what database indexing is and when you would add an index.",
    ],
    "postgresql": [
        "What are the main advantages of PostgreSQL over MySQL?",
        "How does PostgreSQL handle transactions and ACID compliance?",
        "Explain the JSONB data type in PostgreSQL and when you would use it.",
    ],
    "system design": [
        "How would you design a URL shortening service like bit.ly? Walk through components.",
        "Design a notification system that delivers 1 million messages per day.",
        "How would you design a distributed cache to reduce database load?",
    ],
    "algorithms": [
        "Explain the time and space complexity of quicksort in best and worst cases.",
        "How would you detect a cycle in a linked list? Write the algorithm.",
        "What is dynamic programming? Describe a problem where you would apply it.",
    ],
    "testing": [
        "What is the difference between unit testing and integration testing?",
        "How do you write testable code? What design patterns support testability?",
        "What is TDD (Test-Driven Development) and what are its practical benefits?",
    ],
    "react": [
        "What is the virtual DOM and how does React use it to improve performance?",
        "Explain the difference between useState and useEffect hooks.",
        "What is the difference between controlled and uncontrolled components in React?",
    ],
    "typescript": [
        "What is the difference between 'interface' and 'type' in TypeScript?",
        "Explain TypeScript generics and give a real-world example.",
        "What are TypeScript utility types? Explain Partial, Pick, and Omit.",
    ],
    "machine learning": [
        "What is the difference between supervised and unsupervised learning?",
        "Explain overfitting and underfitting. How do you address each?",
        "What is cross-validation and why is it important for model evaluation?",
    ],
    "python": [
        "What is the difference between a list and a tuple in Python?",
        "Explain Python's GIL (Global Interpreter Lock) and its implications.",
        "What are Python decorators? Write a simple decorator example.",
    ],
    "git": [
        "What is the difference between git merge and git rebase?",
        "How do you resolve a merge conflict in Git?",
        "Explain a branching strategy you would recommend for a team of 5 engineers.",
    ],
    "api": [
        "What is the difference between REST and GraphQL?",
        "Explain HTTP status codes: 200, 201, 400, 401, 403, 404, 500.",
        "Design a RESTful API for a blog application with posts and comments.",
    ],
    "aws": [
        "What is the difference between EC2, Lambda, and ECS in AWS?",
        "Explain the difference between S3 and EBS storage.",
        "What is IAM and how do you manage least-privilege permissions in AWS?",
    ],
    "mongodb": [
        "When would you choose MongoDB over a relational database?",
        "What is the aggregation pipeline in MongoDB? Give an example.",
        "How does MongoDB handle indexing and what are its limitations?",
    ],
    "redis": [
        "What is Redis and what are its primary use cases?",
        "Explain the difference between Redis as a cache vs a message broker.",
        "What Redis data structures do you know? When would you use each?",
    ],
    "security": [
        "What is the difference between authentication and authorization?",
        "How do you prevent SQL injection in a web application?",
        "What is JWT and how does token-based authentication work?",
    ],
    "microservices": [
        "What are the main advantages and disadvantages of microservices vs monolith?",
        "How do microservices communicate? When would you use REST vs message queues?",
        "How do you handle data consistency across multiple microservices?",
    ],
    "ci/cd": [
        "What is the difference between continuous integration and continuous deployment?",
        "Describe a CI/CD pipeline you would set up for a web application from scratch.",
        "How do you handle environment-specific configuration secrets in a CI/CD pipeline?",
    ],
    "pytorch": [
        "What is the difference between torch.Tensor and torch.autograd?",
        "Explain PyTorch's dynamic computation graph vs TensorFlow's static graph.",
        "How do you implement a custom loss function in PyTorch?",
    ],
    "tensorflow": [
        "What is the difference between TensorFlow 1.x and 2.x?",
        "How do you save and load a trained TensorFlow/Keras model?",
        "What is eager execution in TensorFlow and why was it introduced?",
    ],
    "nlp": [
        "What is tokenization and why is it an important NLP preprocessing step?",
        "Explain the attention mechanism and how transformers use it.",
        "What is the difference between word2vec and BERT embeddings?",
    ],
    "accessibility": [
        "What are WCAG guidelines and what compliance level is typically required?",
        "How do you ensure a React component is fully keyboard-navigable?",
        "What is ARIA and when should you use ARIA roles vs semantic HTML?",
    ],
    "next.js": [
        "What is the difference between SSR, SSG, and ISR in Next.js?",
        "How does Next.js file-based routing compare to React Router?",
        "What is the purpose of getServerSideProps vs getStaticProps?",
    ],
    "fastapi": [
        "What makes FastAPI faster than Django or Flask for API development?",
        "How does FastAPI handle request validation using Pydantic?",
        "How do you implement dependency injection in FastAPI?",
    ],
    "langchain": [
        "What is LangChain and what problem does it solve for LLM applications?",
        "Explain the concept of chains and agents in LangChain.",
        "How would you build a RAG (Retrieval Augmented Generation) pipeline with LangChain?",
    ],
    "rag": [
        "What is RAG (Retrieval Augmented Generation) and why is it used?",
        "Explain the difference between fine-tuning an LLM and using RAG.",
        "What vector databases would you use for a RAG pipeline and why?",
    ],
    "r programming": [
        "What are the main data structures in R and when would you use each?",
        "How does R differ from Python for statistical analysis?",
        "Explain how you would perform regression analysis in R.",
    ],
}

MAX_UPLOAD_BYTES = 10 * 1024 * 1024  # 10 MB
MIN_EVIDENCE_LENGTH = 18

SCORE_WEIGHTS = {
    "keyword": 0.40,
    "project": 0.20,
    "experience": 0.20,
    "education": 0.10,
    "formatting": 0.10,
}
