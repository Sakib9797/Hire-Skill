"""
ATS Resume Checker Service
Analyzes a resume for ATS compatibility, scores it, and provides role-specific advice.
"""
import re
from typing import Dict, List, Optional


ROLE_KEYWORDS = {
    "software engineer":     ["python", "java", "javascript", "react", "node", "sql", "api", "git",
                               "aws", "docker", "kubernetes", "ci/cd", "algorithm", "data structure",
                               "agile", "scrum", "microservices", "rest", "oop"],
    "data scientist":        ["python", "machine learning", "deep learning", "tensorflow", "pytorch",
                               "pandas", "numpy", "sql", "statistics", "nlp", "data analysis",
                               "scikit-learn", "visualization", "tableau", "r", "hypothesis testing"],
    "ai engineer":           ["python", "machine learning", "deep learning", "nlp", "tensorflow",
                               "pytorch", "llm", "transformers", "computer vision", "mlops",
                               "model deployment", "feature engineering", "neural network", "bert", "gpt"],
    "product manager":       ["roadmap", "stakeholder", "agile", "scrum", "jira", "kpis", "user research",
                               "product strategy", "a/b testing", "analytics", "prioritization",
                               "wireframe", "go-to-market", "backlog", "mvp"],
    "ux designer":           ["figma", "sketch", "wireframe", "prototype", "user research", "usability",
                               "design system", "ui", "ux", "accessibility", "a/b testing",
                               "information architecture", "user journey", "adobe xd"],
    "devops engineer":       ["docker", "kubernetes", "aws", "azure", "gcp", "terraform", "ansible",
                               "ci/cd", "jenkins", "linux", "bash", "monitoring", "prometheus",
                               "grafana", "infrastructure", "helm", "git"],
    "data analyst":          ["sql", "excel", "python", "r", "tableau", "power bi", "data visualization",
                               "statistics", "reporting", "dashboard", "kpis", "etl", "pandas", "looker"],
    "frontend developer":    ["html", "css", "javascript", "react", "vue", "angular", "typescript",
                               "responsive", "webpack", "accessibility", "rest api", "git", "sass",
                               "performance optimization", "cross-browser"],
    "backend developer":     ["python", "java", "node.js", "sql", "nosql", "api", "rest", "graphql",
                               "microservices", "docker", "aws", "caching", "authentication",
                               "database", "orm", "git"],
    "cybersecurity analyst": ["penetration testing", "vulnerability", "siem", "firewalls", "encryption",
                               "owasp", "incident response", "compliance", "python", "network security",
                               "risk assessment", "ethical hacking", "cloud security"],
}

ROLE_ADDITIONS = {
    "software engineer":     ["Add measurable achievements (e.g., 'Reduced API response time by 40%')",
                               "Include GitHub/portfolio link",
                               "List system design experience",
                               "Mention team size you worked with",
                               "Add programming languages with proficiency levels"],
    "data scientist":        ["Quantify model performance (accuracy, F1, AUC)",
                               "Add links to published notebooks or Kaggle profile",
                               "Include dataset sizes you worked with",
                               "Mention cloud ML platforms used (SageMaker, Vertex AI)",
                               "Add any publications or research papers"],
    "ai engineer":           ["Include LLM fine-tuning or RAG experience if applicable",
                               "Mention model deployment tools (TorchServe, Triton, FastAPI)",
                               "Add MLOps tools (MLflow, Weights & Biases)",
                               "Quantify model improvements you delivered",
                               "List hardware used (GPU types, distributed training)"],
    "product manager":       ["Add product metrics you owned (MAU, retention, revenue)",
                               "Mention specific frameworks like OKRs or RICE scoring",
                               "Include cross-functional team leadership examples",
                               "Show impact on business outcomes",
                               "Add any certifications (CSPO, CPM)"],
    "ux designer":           ["Add a portfolio URL",
                               "Mention number of users your designs served",
                               "Include design process description (Discovery → Delivery)",
                               "Add usability testing methodology",
                               "List design system contributions"],
    "devops engineer":       ["Include cloud cost savings achieved",
                               "Mention uptime/SLA metrics maintained",
                               "Add disaster recovery or on-call experience",
                               "List infrastructure scale (servers, requests/sec)",
                               "Include security hardening experience"],
    "data analyst":          ["Quantify insights that drove business decisions",
                               "Add BI tool dashboard examples",
                               "Include stakeholder presentation experience",
                               "Mention SQL query optimization",
                               "Add any automation work (Python scripts, ETL pipelines)"],
    "frontend developer":    ["Include Lighthouse/performance scores achieved",
                               "Add accessibility (WCAG) compliance experience",
                               "Mention user count or traffic for built apps",
                               "List design-to-code workflow tools",
                               "Add mobile/responsive design specifics"],
    "backend developer":     ["Quantify API throughput/latency improvements",
                               "Include database design and optimization work",
                               "Add security practices (auth, OWASP)",
                               "Mention concurrent user load handled",
                               "List third-party integrations built"],
    "cybersecurity analyst": ["Add certifications (CEH, CISSP, Security+, OSCP)",
                               "Include CVE findings or bug bounty wins",
                               "Mention compliance frameworks (SOC 2, ISO 27001)",
                               "Quantify vulnerabilities discovered and remediated",
                               "Add incident response case outcomes"],
}

GENERIC_ADDITIONS = [
    "Add measurable achievements with numbers (%, $, time saved)",
    "Include a LinkedIn profile URL",
    "Add a professional summary/objective tailored to the role",
    "List relevant certifications or online courses",
    "Include a GitHub or portfolio link if applicable",
]


class ATSChecker:

    # ── ATS format checks ──────────────────────────────────────────────────────

    FORMAT_CHECKS = [
        ("has_email",          r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}",
         "Contact email address", 8),
        ("has_phone",          r"[\+\(]?[\d\s\-\(\)]{7,}",
         "Contact phone number", 5),
        ("has_linkedin",       r"linkedin\.com",
         "LinkedIn profile URL", 5),
        ("has_github_or_port", r"github\.com|portfolio|behance|dribbble",
         "GitHub / portfolio link", 4),
        ("has_summary",        r"(summary|profile|objective|about me|professional summary)",
         "Professional summary section", 8),
        ("has_experience",     r"(experience|employment|work history)",
         "Work experience section", 10),
        ("has_education",      r"(education|university|college|bachelor|master|degree)",
         "Education section", 8),
        ("has_skills",         r"(skills|technical skills|competencies|technologies)",
         "Skills section", 10),
        ("has_bullets",        r"[•\-\*▪▸►]",
         "Bullet points in descriptions", 5),
        ("has_dates",          r"\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|\d{4})\b",
         "Employment dates", 5),
        ("has_certifications", r"(certif|certificate|license|credential)",
         "Certifications section", 4),
        ("has_projects",       r"(project|portfolio|case study)",
         "Projects section", 4),
        ("no_tables",          None,
         "No complex tables (ATS may mis-parse them)", 3),
        ("no_images",          None,
         "No images / graphics (ATS cannot read them)", 3),
        ("reasonable_length",  None,
         "Resume length (1-3 pages recommended)", 4),
        ("has_action_verbs",
         r"\b(developed|designed|implemented|led|managed|created|built|optimized|improved|"
         r"delivered|collaborated|achieved|increased|reduced|launched|analyzed|automated)\b",
         "Action verbs in experience", 6),
        ("has_numbers",        r"\b\d+[\%\$kK]?\b",
         "Quantified achievements", 7),
    ]

    @classmethod
    def check(cls, pdf_text: str, target_role: Optional[str] = None) -> Dict:
        """
        Full ATS check pipeline.
        Returns a dict with score, passed/failed checks, problems, and recommendations.
        """
        text_lower = pdf_text.lower()
        word_count = len(pdf_text.split())

        passed_checks: List[Dict] = []
        failed_checks: List[Dict] = []
        problems:      List[str]  = []
        total_possible = 0

        for key, pattern, label, weight in cls.FORMAT_CHECKS:
            total_possible += weight
            ok = cls._run_check(key, pattern, text_lower, word_count)
            entry = {"key": key, "label": label, "weight": weight}
            if ok:
                passed_checks.append(entry)
            else:
                failed_checks.append(entry)
                problems.append(cls._problem_text(key, label))

        # Keyword density analysis (only when role given)
        keyword_score = 0
        matched_kws:  List[str] = []
        missing_kws:  List[str] = []
        role_key = target_role.lower().strip() if target_role else None
        role_kw_list: List[str] = []

        if role_key:
            best_role, role_kw_list = cls._best_role_match(role_key)
            for kw in role_kw_list:
                if kw in text_lower:
                    matched_kws.append(kw)
                else:
                    missing_kws.append(kw)

            if role_kw_list:
                kw_pct = len(matched_kws) / len(role_kw_list)
                keyword_score = round(kw_pct * 25)   # up to 25 bonus points
                total_possible += 25

                if kw_pct < 0.4:
                    problems.append(
                        f"Low keyword density for '{target_role}': "
                        f"only {len(matched_kws)}/{len(role_kw_list)} relevant keywords found"
                    )

        # Base score from format checks
        base_earned = sum(c["weight"] for c in passed_checks)
        raw_score   = base_earned + keyword_score
        pct_score   = min(100, round((raw_score / total_possible) * 100)) if total_possible else 0

        # Role-specific additions advice
        role_additions: List[str] = []
        if role_key:
            best_role, _ = cls._best_role_match(role_key)
            role_additions = ROLE_ADDITIONS.get(best_role, GENERIC_ADDITIONS)
        else:
            role_additions = GENERIC_ADDITIONS

        # Build recommendations list
        recommendations = cls._build_recommendations(
            failed_checks, missing_kws, role_additions, target_role
        )

        return {
            "score":             pct_score,
            "passed_checks":     passed_checks,
            "failed_checks":     failed_checks,
            "problems":          problems,
            "recommendations":   recommendations,
            "keyword_analysis":  {
                "role":          target_role,
                "matched":       matched_kws,
                "missing":       missing_kws,
                "total_role_kws": len(role_kw_list),
            },
            "role_additions":    role_additions,
            "word_count":        word_count,
        }

    # ── Internal helpers ───────────────────────────────────────────────────────

    @staticmethod
    def _run_check(key: str, pattern: Optional[str], text_lower: str, word_count: int) -> bool:
        if key == "no_tables":
            return True          # PDF text extraction strips tables; treat as pass
        if key == "no_images":
            return True          # same reason
        if key == "reasonable_length":
            return 150 <= word_count <= 1400
        if pattern:
            return bool(re.search(pattern, text_lower, re.IGNORECASE))
        return False

    @staticmethod
    def _problem_text(key: str, label: str) -> str:
        custom = {
            "has_email":          "Missing contact email – recruiters cannot reach you.",
            "has_phone":          "Missing phone number.",
            "has_linkedin":       "No LinkedIn URL – reduces credibility and searchability.",
            "has_github_or_port": "No GitHub/portfolio link found.",
            "has_summary":        "Missing professional summary – ATS and recruiters expect one.",
            "has_experience":     "Work experience section not detected.",
            "has_education":      "Education section not detected.",
            "has_skills":         "Skills section not found – ATS keyword matching will fail.",
            "has_bullets":        "No bullet points detected – use bullets for scannability.",
            "has_dates":          "Employment dates missing – ATS cannot calculate tenure.",
            "has_certifications": "No certifications listed.",
            "has_projects":       "No projects section found.",
            "reasonable_length":  "Resume length is outside the ideal 1-3 page range.",
            "has_action_verbs":   "Weak language – use strong action verbs (Built, Led, Delivered...).",
            "has_numbers":        "No quantified achievements found – add metrics (%, $, users, time).",
        }
        return custom.get(key, f"Missing: {label}")

    @staticmethod
    def _best_role_match(role_key: str):
        """Return the best matching role and its keyword list."""
        for role, kws in ROLE_KEYWORDS.items():
            if role in role_key or role_key in role:
                return role, kws
        # Partial word match
        role_words = set(role_key.split())
        for role, kws in ROLE_KEYWORDS.items():
            if role_words & set(role.split()):
                return role, kws
        return "software engineer", ROLE_KEYWORDS["software engineer"]

    @staticmethod
    def _build_recommendations(failed_checks, missing_kws, role_additions, target_role):
        recs = []
        priority_map = {
            "has_summary":     "Add a 3-4 sentence professional summary at the top of your resume.",
            "has_skills":      "Create a dedicated 'Skills' section listing your technical competencies.",
            "has_bullets":     "Use bullet points (•) for every job description entry.",
            "has_action_verbs":"Start each bullet with a strong action verb (Built, Led, Delivered, Improved).",
            "has_numbers":     "Quantify at least 3 achievements with numbers, %, or $ values.",
            "has_linkedin":    "Add your LinkedIn URL in the contact header.",
            "has_dates":       "Add start – end dates (Month Year) for every job.",
            "has_certifications": "Add a Certifications section if you have any relevant credentials.",
            "has_projects":    "Add a Projects section showcasing relevant work.",
            "has_github_or_port": "Include a GitHub or portfolio link.",
        }
        for check in failed_checks:
            msg = priority_map.get(check["key"])
            if msg:
                recs.append({"priority": "high", "text": msg})

        if missing_kws and target_role:
            top_missing = missing_kws[:6]
            recs.append({
                "priority": "high",
                "text": f"Add these missing keywords for '{target_role}': "
                        + ", ".join(top_missing)
            })

        for addition in role_additions[:5]:
            recs.append({"priority": "medium", "text": addition})

        return recs
