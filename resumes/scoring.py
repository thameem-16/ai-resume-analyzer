import re

# Canonical skills whitelist — canonical (display) form of each term.
# Multi-word and symbol-containing terms (e.g. "CI/CD", "REST API") are
# matched via regex word-boundary patterns built at module load time.
SKILLS = [
    # Languages
    "Python", "Java", "JavaScript", "TypeScript", "C", "C++", "C#", "Go",
    "Rust", "Ruby", "PHP", "Swift", "Kotlin", "Scala", "Perl", "R",
    "Dart", "Lua", "Haskell", "Elixir", "Clojure", "Erlang", "Shell",
    "Bash", "PowerShell", "SQL", "HTML", "CSS", "SASS", "LESS",
    # Frontend frameworks & libraries
    "React", "Angular", "Vue", "Svelte", "Next.js", "Nuxt.js", "Gatsby",
    "jQuery", "Bootstrap", "Tailwind CSS", "Material UI", "Redux",
    "Webpack", "Vite", "Babel",
    # Backend frameworks
    "Django", "Flask", "FastAPI", "Spring", "Spring Boot", "Express",
    "NestJS", "Rails", "Laravel", "ASP.NET", "Gin", "Fiber", "Phoenix",
    # Databases
    "PostgreSQL", "MySQL", "SQLite", "MongoDB", "Redis", "Cassandra",
    "DynamoDB", "Elasticsearch", "Neo4j", "CouchDB", "MariaDB",
    "Oracle", "SQL Server", "Firebase",
    # Cloud & infrastructure
    "AWS", "Azure", "GCP", "Google Cloud", "Heroku", "DigitalOcean",
    "Vercel", "Netlify", "Cloudflare",
    # DevOps & CI/CD
    "Docker", "Kubernetes", "Terraform", "Ansible", "Jenkins", "GitHub Actions",
    "GitLab CI", "CircleCI", "Travis CI", "CI/CD", "Helm", "Vagrant",
    "Prometheus", "Grafana", "Datadog", "New Relic", "Nginx", "Apache",
    # Version control
    "Git", "GitHub", "GitLab", "Bitbucket", "SVN",
    # APIs & protocols
    "REST API", "GraphQL", "gRPC", "WebSocket", "OAuth", "JWT", "SOAP",
    # Data & ML
    "Pandas", "NumPy", "SciPy", "Scikit-learn", "TensorFlow", "PyTorch",
    "Keras", "Spark", "Hadoop", "Kafka", "Airflow", "dbt",
    "Machine Learning", "Deep Learning", "NLP", "Computer Vision",
    # Testing
    "Jest", "Mocha", "Pytest", "Selenium", "Cypress", "Playwright",
    "JUnit", "TestNG", "RSpec",
    # Task queues & messaging
    "Celery", "RabbitMQ", "SQS", "Pub/Sub",
    # Methodologies & practices
    "Agile", "Scrum", "Kanban", "TDD", "BDD", "DevOps", "SRE",
    "Microservices", "Monolith", "MVC", "MVVM", "OOP",
    "Design Patterns", "System Design", "Data Structures", "Algorithms",
    # Misc tools & platforms
    "Linux", "Unix", "Windows", "macOS", "Jira", "Confluence", "Slack",
    "Figma", "Postman", "Swagger", "OpenAPI", "Storybook",
    "Webpack", "ESLint", "Prettier", "SonarQube",
    "Node.js", "Deno", "Bun",
    "Electron", "React Native", "Flutter", "Ionic",
    "WordPress", "Shopify", "Magento",
    "Tableau", "Power BI", "Looker",
    "Snowflake", "Redshift", "BigQuery",
    "Vault", "Consul", "Istio", "Envoy",
    "Lambda", "CloudFormation", "CDK",
    "S3", "EC2", "ECS", "EKS", "Fargate", "RDS",
]

# Build a mapping from lowercase pattern → canonical display name, and a
# single compiled regex that matches any skill via word boundaries.
_skill_map: dict[str, str] = {}
_patterns: list[str] = []

for _skill in SKILLS:
    _escaped = re.escape(_skill)
    _pattern = rf"(?i)\b{_escaped}\b"
    _skill_map[_skill.lower()] = _skill
    _patterns.append(_escaped)

# Sort longest-first so multi-word terms match before their sub-terms.
_patterns.sort(key=len, reverse=True)
_SKILL_RE = re.compile(r"(?i)\b(?:" + "|".join(_patterns) + r")\b")


def _find_skills(text):
    """Return the set of canonical skill names found in *text*."""
    return {_skill_map[m.group().lower()] for m in _SKILL_RE.finditer(text)}


def calculate_match_score(resume_text, jd_text):
    """Score a resume against a job description based on skill overlap.

    Returns (score, missing_keywords) where *score* is 0–100 and
    *missing_keywords* lists JD skills absent from the resume.
    """
    jd_skills = _find_skills(jd_text)
    if not jd_skills:
        return 100, []

    resume_skills = _find_skills(resume_text)
    missing = sorted(jd_skills - resume_skills)
    found = len(jd_skills) - len(missing)
    score = round(found / len(jd_skills) * 100)

    return score, missing
