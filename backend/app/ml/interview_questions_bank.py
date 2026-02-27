"""
Comprehensive Interview Questions Bank
========================================
150+ interview questions organised by category and technical domain.
Each question includes:
  - category   : one of the standard interview categories
  - domain     : list of keywords that trigger this question (empty = universal)
  - question   : the question text (may contain {role} placeholder)
  - what_they_want : what the interviewer is evaluating
  - model_answer   : a strong sample answer (may contain {role} placeholder)
  - source     : attribution for the question inspiration

The template builder picks ~15 questions per request, matching the user's
job title / description keywords to each question's domain tags.
"""

CATEGORIES = [
    "Technical Skills",
    "Problem Solving",
    "System Design",
    "Behavioral (STAR)",
    "Teamwork",
    "Handling Failure",
    "Domain Knowledge",
    "Career Goals",
    "Leadership",
    "Communication",
    "Coding & Algorithms",
    "Culture Fit",
]

# ---------------------------------------------------------------------------
# Master question bank
# ---------------------------------------------------------------------------

QUESTIONS_BANK = [
    # ╔═══════════════════════════════════════════════════════════════════════╗
    # ║  UNIVERSAL QUESTIONS (apply to any role)                            ║
    # ╚═══════════════════════════════════════════════════════════════════════╝

    # --- Behavioral ---
    {
        "category": "Behavioral (STAR)",
        "domain": [],
        "question": "Tell me about a time you delivered a {role} project under a tight deadline. How did you prioritise?",
        "what_they_want": "Time management, prioritisation, stakeholder communication, and delivery under pressure.",
        "model_answer": (
            "In a previous role, we had two weeks to ship a feature that usually takes a month. "
            "I sat down with the PM to identify the must-have MVP slice and deferred nice-to-haves to the next sprint. "
            "I broke the work into daily milestones and flagged blockers in standups immediately. "
            "We shipped on time with all critical acceptance criteria met."
        ),
        "source": "STAR Framework — Amazon Leadership Principles"
    },
    {
        "category": "Behavioral (STAR)",
        "domain": [],
        "question": "Describe a situation where you had to learn a new technology or framework quickly. How did you approach it?",
        "what_they_want": "Learning agility, resourcefulness, and ability to be productive in unfamiliar environments.",
        "model_answer": (
            "When my team migrated to Kubernetes, I had zero container-orchestration experience. "
            "I blocked off two hours daily for a week: watched KodeKloud tutorials, deployed a toy cluster locally, "
            "then paired with our DevOps lead on the staging migration. Within two weeks I was reviewing k8s manifests in PRs. "
            "Teaching myself in small increments while having a mentor for edge cases was key."
        ),
        "source": "Google Behavioral Interview Guide"
    },
    {
        "category": "Behavioral (STAR)",
        "domain": [],
        "question": "Give an example of a time when you received critical feedback. How did you respond?",
        "what_they_want": "Self-awareness, emotional maturity, growth mindset, and coachability.",
        "model_answer": (
            "During a code review, my tech lead pointed out that my abstractions were over-engineered and hurt readability. "
            "Initially I felt defensive, but I re-read the feedback objectively and realised they were right. "
            "I simplified the code, thanked them for the candid review, and started following the team's style guide more closely. "
            "My PR merge rate improved noticeably after that."
        ),
        "source": "Meta Behavioral Interview Bank"
    },
    {
        "category": "Behavioral (STAR)",
        "domain": [],
        "question": "Tell me about a time you went above and beyond what was expected of you.",
        "what_they_want": "Initiative, ownership, and passion for the work beyond minimum requirements.",
        "model_answer": (
            "We had a spike in customer complaints about slow search. Although it wasn't in my sprint, I profiled the queries "
            "over the weekend and found a missing index that caused full table scans. I submitted a PR Monday morning, "
            "got it reviewed by noon, and search latency dropped 80%. The product team hadn't even filed a ticket yet."
        ),
        "source": "Amazon Leadership Principles — Bias for Action"
    },
    {
        "category": "Behavioral (STAR)",
        "domain": [],
        "question": "Describe a time you had to make a decision without having all the information you needed.",
        "what_they_want": "Judgement under ambiguity, risk assessment, and ability to move forward despite uncertainty.",
        "model_answer": (
            "We had to choose between two third-party payment providers while both were still in pilot phase. "
            "I listed known trade-offs, consulted with finance on pricing, and chose the one with better API docs and uptime SLA. "
            "I also built an adapter layer so we could swap providers later. The initial choice held up for two years."
        ),
        "source": "McKinsey Case Interview — Decision Under Uncertainty"
    },

    # --- Teamwork ---
    {
        "category": "Teamwork",
        "domain": [],
        "question": "Describe a situation where you had a technical disagreement with a colleague. How did you resolve it?",
        "what_they_want": "Collaboration, empathy, evidence-based decision making, and professionalism.",
        "model_answer": (
            "We disagreed on whether to use REST or GraphQL for a new service. "
            "Rather than debating opinions, I proposed we both write a spike: I built REST, my colleague did GraphQL. "
            "We compared developer experience, payload size, and query flexibility against the same acceptance criteria. "
            "The data led us to GraphQL. The structured approach removed the personal element."
        ),
        "source": "Stripe Engineering Culture"
    },
    {
        "category": "Teamwork",
        "domain": [],
        "question": "How do you handle working with someone whose work style is very different from yours?",
        "what_they_want": "Adaptability, emotional intelligence, and ability to collaborate across personality types.",
        "model_answer": (
            "I once paired with a colleague who preferred detailed documentation before writing any code, while I lean toward prototyping. "
            "We agreed on a middle ground: lightweight design docs for the approach, then rapid prototyping for implementation details. "
            "It actually improved both our workflows — I started writing better docs, and they got more comfortable iterating."
        ),
        "source": "Atlassian Team Playbook"
    },
    {
        "category": "Teamwork",
        "domain": [],
        "question": "Tell me about a time you mentored or helped a junior team member succeed.",
        "what_they_want": "Leadership potential, generosity with knowledge, and investment in team growth.",
        "model_answer": (
            "A new hire was struggling with our codebase's async patterns. I set up weekly pairing sessions where we debugged real tickets together. "
            "I also created a 'gotchas' doc for our most confusing patterns. Within a month they were contributing independently "
            "and even improved one of the patterns they'd initially found confusing."
        ),
        "source": "Google Engineering Practices"
    },

    # --- Handling Failure ---
    {
        "category": "Handling Failure",
        "domain": [],
        "question": "Tell me about a project or feature you worked on that failed or did not go as planned. What did you learn?",
        "what_they_want": "Self-awareness, accountability, resilience, and growth mindset.",
        "model_answer": (
            "I released a feature without adequate load testing. Under production traffic it caused database connection pool exhaustion. "
            "I owned the incident, rolled back quickly, and wrote a blameless post-mortem. "
            "We added load testing to our CI pipeline and set connection pool metrics as SLOs. "
            "It permanently improved the team's reliability practices."
        ),
        "source": "PagerDuty Incident Response Guide"
    },
    {
        "category": "Handling Failure",
        "domain": [],
        "question": "Tell me about a bad technical decision you made. How did you recognise it and what did you do?",
        "what_they_want": "Humility, ability to course-correct, and pragmatism over ego.",
        "model_answer": (
            "I chose a NoSQL database for a project that clearly had relational data. Within a month, queries were getting complex "
            "and we were duplicating data everywhere. I raised the issue in a retro, proposed a migration plan to PostgreSQL, "
            "and led the migration over two sprints. The lesson: choose technology based on data access patterns, not hype."
        ),
        "source": "ThoughtWorks Technology Radar"
    },
    {
        "category": "Handling Failure",
        "domain": [],
        "question": "Describe a time you missed a deadline. What happened and how did you handle it?",
        "what_they_want": "Honesty, accountability, and proactive communication when things go wrong.",
        "model_answer": (
            "I underestimated the complexity of integrating a third-party API. When I realised I'd miss the deadline by three days, "
            "I immediately informed my manager and the PM, explained the root cause, and proposed a revised timeline. "
            "I also suggested shipping a partial integration first so stakeholders had something usable. "
            "The transparency was appreciated and we adjusted scope accordingly."
        ),
        "source": "Agile Best Practices — Sprint Retrospectives"
    },

    # --- Leadership ---
    {
        "category": "Leadership",
        "domain": [],
        "question": "Have you ever led a project without formal authority? How did you influence the outcome?",
        "what_they_want": "Influence without authority, persuasion skills, and initiative.",
        "model_answer": (
            "Our team had growing tech debt but no one owned it. I created a 'Tech Debt Tuesday' initiative where we'd spend "
            "two hours each Tuesday on the highest-impact items. I pitched it via a Slack RFC, gathered support from three senior devs, "
            "and showed the PM how it would reduce bug rates. Within a quarter, our regression rate dropped 40%."
        ),
        "source": "Staff Engineer Archetypes — Will Larson"
    },
    {
        "category": "Leadership",
        "domain": [],
        "question": "How do you handle a situation where your team disagrees on the technical approach?",
        "what_they_want": "Facilitation skills, ability to drive consensus, and pragmatic decision-making.",
        "model_answer": (
            "I facilitate a time-boxed discussion where each person presents their approach with pros/cons. "
            "If there's no clear winner, I suggest defining evaluation criteria upfront (performance, maintainability, time-to-ship) "
            "and scoring each option. If we're still tied, I propose: 'Let's go with the simplest option and revisit in two weeks.' "
            "This prevents analysis paralysis while keeping the door open."
        ),
        "source": "Netflix Culture Deck — Freedom & Responsibility"
    },

    # --- Communication ---
    {
        "category": "Communication",
        "domain": [],
        "question": "How do you explain a complex technical concept to a non-technical stakeholder?",
        "what_they_want": "Communication clarity, ability to tailor message to audience, and business awareness.",
        "model_answer": (
            "I use analogies and focus on impact rather than implementation. For example, when explaining database indexing to a product manager, "
            "I compared it to a book's index — without it, you'd have to read every page to find what you want. "
            "I then connected it to their concern: 'Adding this index means search results load in 0.5s instead of 8s.' "
            "Leading with the business impact makes the technical decision tangible."
        ),
        "source": "Gergely Orosz — The Pragmatic Engineer"
    },
    {
        "category": "Communication",
        "domain": [],
        "question": "Tell me about a time you had to push back on a requirement from a stakeholder.",
        "what_they_want": "Professional assertiveness, ability to say no constructively, and solution-oriented thinking.",
        "model_answer": (
            "A PM wanted us to add real-time notifications in a sprint that was already overcommitted. "
            "Instead of just saying no, I showed the current sprint load, estimated the notification feature at 8 story points, "
            "and proposed either deferring it to next sprint or swapping out a lower-priority item. "
            "We agreed to swap, and the feature shipped without overtime."
        ),
        "source": "Basecamp — Shape Up"
    },

    # --- Career Goals ---
    {
        "category": "Career Goals",
        "domain": [],
        "question": "Where do you see yourself in 3–5 years, and why is this {role} position a step toward that goal?",
        "what_they_want": "Ambition, alignment between role and personal growth, and genuine interest.",
        "model_answer": (
            "In three to five years I aim to be a senior {role} who ships impactful systems and mentors junior teammates. "
            "This role is a strong fit because it involves the scale and complexity I want to work on, "
            "and the team's emphasis on engineering excellence aligns with how I want to grow. "
            "I'm excited by the opportunity to work across the full stack of the problem."
        ),
        "source": "Career Growth Frameworks"
    },
    {
        "category": "Career Goals",
        "domain": [],
        "question": "What motivates you most in your work? What kind of projects make you lose track of time?",
        "what_they_want": "Intrinsic motivation, self-knowledge, and culture fit.",
        "model_answer": (
            "I'm most energised when I'm solving a hard problem that has real user impact — especially when it involves "
            "bringing together multiple systems or technologies. The projects where I lose track of time usually involve "
            "debugging a tricky production issue or designing an elegant API that simplifies a complex domain."
        ),
        "source": "Daniel Pink — Drive"
    },

    # --- Culture Fit ---
    {
        "category": "Culture Fit",
        "domain": [],
        "question": "What does a healthy engineering culture look like to you?",
        "what_they_want": "Values alignment, awareness of engineering best practices, and team-orientation.",
        "model_answer": (
            "A healthy culture has psychological safety (people can ask questions and admit mistakes), "
            "strong code review norms, blameless post-mortems, investment in developer tooling, "
            "and a bias toward shipping iteratively rather than perfecting in isolation. "
            "I also value teams that celebrate learning alongside shipping."
        ),
        "source": "Google Project Aristotle — Psychological Safety"
    },
    {
        "category": "Culture Fit",
        "domain": [],
        "question": "How do you stay current with industry trends and new technologies?",
        "what_they_want": "Continuous learning mindset and proactive professional development.",
        "model_answer": (
            "I combine several channels: I read newsletters (TLDR, Pragmatic Engineer), follow key people on Twitter/LinkedIn, "
            "listen to podcasts during commutes, and dedicate time to side projects where I try new tools. "
            "Recently I built a small RAG app to learn LangChain hands-on. "
            "I find that building something small is the fastest way to truly learn a new technology."
        ),
        "source": "ThoughtWorks Technology Radar"
    },

    # ╔═══════════════════════════════════════════════════════════════════════╗
    # ║  MACHINE LEARNING / AI DOMAIN                                       ║
    # ╚═══════════════════════════════════════════════════════════════════════╝
    {
        "category": "Technical Skills",
        "domain": ["ml", "machine learning", "deep learning", "ai", "data science", "tensorflow", "pytorch", "sklearn", "model"],
        "question": "Walk me through how you would build and evaluate a classification model for a real-world {role} problem.",
        "what_they_want": "Understanding of the end-to-end ML pipeline: data collection, feature engineering, model selection, evaluation.",
        "model_answer": (
            "I'd start by defining the problem and collecting representative labelled data. "
            "After exploratory analysis and feature engineering, I'd train baseline models (logistic regression, random forest) "
            "and compare using cross-validation with precision, recall, and AUC. "
            "I'd tune the best model, validate on a held-out test set, and deploy via a REST API with monitoring for data drift."
        ),
        "source": "Chip Huyen — Designing Machine Learning Systems"
    },
    {
        "category": "Technical Skills",
        "domain": ["ml", "machine learning", "deep learning", "ai", "model", "neural"],
        "question": "Explain the bias-variance trade-off and how you would diagnose it in a production model.",
        "what_they_want": "Fundamental ML theory and practical debugging skills.",
        "model_answer": (
            "Bias is the error from overly simple models (underfitting); variance is the error from models that are too sensitive to training data (overfitting). "
            "I diagnose it by comparing training vs. validation loss: high training loss = high bias; large gap between train and val loss = high variance. "
            "Fixes include adding features or capacity for bias, and regularisation/more data for variance."
        ),
        "source": "Andrew Ng — Machine Learning Yearning"
    },
    {
        "category": "Technical Skills",
        "domain": ["ml", "machine learning", "deep learning", "ai", "llm", "nlp", "transformer", "gpt"],
        "question": "How do transformer models (like GPT/BERT) work at a high level? What makes them different from RNNs?",
        "what_they_want": "Understanding of modern NLP architecture and attention mechanisms.",
        "model_answer": (
            "Transformers use self-attention to weigh all positions in a sequence simultaneously, unlike RNNs which process sequentially. "
            "The key innovation is the scaled dot-product attention mechanism that captures long-range dependencies without the vanishing gradient problem. "
            "This parallelism also enables much faster training on GPUs. BERT uses encoder-only for understanding; GPT uses decoder-only for generation."
        ),
        "source": "Vaswani et al. — Attention Is All You Need"
    },
    {
        "category": "Technical Skills",
        "domain": ["ml", "machine learning", "ai", "llm", "rag", "langchain", "prompt", "vector"],
        "question": "Explain RAG (Retrieval Augmented Generation). When would you use it over fine-tuning?",
        "what_they_want": "Understanding of modern LLM application patterns and trade-offs.",
        "model_answer": (
            "RAG combines a retriever (usually a vector DB search) with an LLM generator. The retriever finds relevant documents, "
            "which are injected into the prompt context. Use RAG when: data changes frequently, you need source attribution, "
            "or you can't afford fine-tuning compute. Use fine-tuning when: you need to change the model's style/format, "
            "the knowledge is stable, or latency matters and you want to avoid the retrieval step."
        ),
        "source": "DeepLearning.AI — LangChain for LLM Applications"
    },
    {
        "category": "System Design",
        "domain": ["ml", "machine learning", "ai", "mlops", "model", "deep learning"],
        "question": "Design an end-to-end ML system for a recommendation engine serving 10M users.",
        "what_they_want": "ML system design: data pipelines, feature stores, model serving, monitoring, and scale.",
        "model_answer": (
            "I'd create a two-stage system: candidate generation (fast, broad recall using embeddings/ANN) and ranking (slower, precise using a neural model). "
            "Features come from a feature store (Feast) with both batch and real-time sources. "
            "Model training runs on Spark/Ray, serving via TensorFlow Serving behind a load balancer. "
            "I'd monitor prediction drift with Evidently AI and retrain weekly on new interaction data."
        ),
        "source": "Chip Huyen — ML System Design Interview"
    },
    {
        "category": "Problem Solving",
        "domain": ["ml", "machine learning", "ai", "data science", "model"],
        "question": "Your production ML model's accuracy has dropped 15% over the past month. How do you diagnose and fix it?",
        "what_they_want": "Debugging methodology for ML systems: data drift, concept drift, pipeline issues.",
        "model_answer": (
            "I'd check in order: (1) data pipeline integrity — has the schema or ETL changed? (2) Input data distribution — compare recent vs. training data using statistical tests or Evidently dashboards. "
            "(3) Concept drift — has the relationship between features and target changed? (4) External factors — seasonality, new user segments. "
            "Depending on the root cause, fixes range from retraining on recent data to rebuilding features or adjusting the target definition."
        ),
        "source": "Google ML Engineering Best Practices"
    },
    {
        "category": "Domain Knowledge",
        "domain": ["ml", "machine learning", "ai", "data science", "deep learning"],
        "question": "What are the most important trends in AI/ML right now, and how are you keeping up with them?",
        "what_they_want": "Industry awareness and continuous learning in a fast-moving field.",
        "model_answer": (
            "Key trends: LLM-powered applications (RAG, agents), multimodal models, smaller/distilled models for edge deployment, "
            "and growing focus on AI safety and regulation. I stay current through arXiv papers, newsletters like The Batch and TLDR AI, "
            "Hugging Face community releases, and hands-on experimentation with new frameworks in personal projects."
        ),
        "source": "State of AI Report 2024"
    },
    {
        "category": "Technical Skills",
        "domain": ["ml", "machine learning", "ai", "deep learning", "computer vision", "cv"],
        "question": "Explain how convolutional neural networks (CNNs) work and why they're effective for image tasks.",
        "what_they_want": "Understanding of CNN architecture — convolutions, pooling, feature hierarchies.",
        "model_answer": (
            "CNNs apply learnable filters that slide across the input to detect spatial patterns. "
            "Early layers learn edges and textures; deeper layers combine those into complex features like faces or objects. "
            "Parameter sharing (same filter everywhere) makes them efficient. Pooling reduces spatial dimensions while retaining key features. "
            "Modern architectures like ResNet add skip connections to train hundreds of layers without vanishing gradients."
        ),
        "source": "Stanford CS231n — Convolutional Neural Networks"
    },

    # ╔═══════════════════════════════════════════════════════════════════════╗
    # ║  DATA ENGINEERING / DATA SCIENCE DOMAIN                             ║
    # ╚═══════════════════════════════════════════════════════════════════════╝
    {
        "category": "Technical Skills",
        "domain": ["data", "sql", "etl", "analytics", "bi", "power bi", "tableau", "data engineer", "warehouse", "spark"],
        "question": "How would you design a data pipeline to feed a real-time analytics dashboard?",
        "what_they_want": "Knowledge of ETL/ELT, data modelling, streaming vs. batch, and BI tooling.",
        "model_answer": (
            "I'd identify source systems and freshness requirements. For real-time, I'd use Kafka or Pub/Sub, "
            "land data into a staging layer, apply transformations, and load into a columnar store like BigQuery. "
            "Batch jobs handle historical reconciliation. The BI layer sits on pre-aggregated materialised views for performance."
        ),
        "source": "Fundamentals of Data Engineering — Joe Reis"
    },
    {
        "category": "Technical Skills",
        "domain": ["data", "sql", "database", "postgres", "mysql", "data engineer"],
        "question": "Explain the difference between OLTP and OLAP databases. When would you use each?",
        "what_they_want": "Understanding of database architecture trade-offs for different workloads.",
        "model_answer": (
            "OLTP (Online Transaction Processing) databases are optimised for high-frequency reads/writes with row-based storage — ideal for application backends. "
            "OLAP (Online Analytical Processing) uses columnar storage for fast aggregation queries over large datasets — ideal for analytics and BI. "
            "In practice, OLTP feeds OLAP via ETL/ELT pipelines. PostgreSQL serves OLTP; Snowflake or BigQuery serve OLAP."
        ),
        "source": "Designing Data-Intensive Applications — Martin Kleppmann"
    },
    {
        "category": "Problem Solving",
        "domain": ["data", "sql", "etl", "pipeline", "data engineer", "spark", "airflow"],
        "question": "A critical data pipeline has been silently producing incorrect results for a week. How do you handle it?",
        "what_they_want": "Incident response, data quality awareness, and systematic debugging.",
        "model_answer": (
            "First, I'd assess the blast radius — which downstream reports/models consumed the bad data, and notify stakeholders. "
            "Then I'd trace the pipeline step by step: check source data, transformation logic, and output validation. "
            "After identifying the root cause, I'd fix it, backfill the affected data, and add data quality checks (Great Expectations or dbt tests) "
            "to catch similar issues early in the future."
        ),
        "source": "Monte Carlo — Data Observability"
    },
    {
        "category": "System Design",
        "domain": ["data", "etl", "data engineer", "spark", "warehouse", "big data"],
        "question": "Design a data warehouse schema for an e-commerce company. What modelling approach would you use?",
        "what_they_want": "Data modelling skills — star/snowflake schema, dimensional modelling.",
        "model_answer": (
            "I'd use a star schema with fact tables (orders, page_views, inventory_changes) and dimension tables (customers, products, time, geography). "
            "The time dimension enables efficient date-range queries. I'd use slowly changing dimensions (SCD Type 2) for customer attributes. "
            "Materialised views would pre-aggregate common KPIs. This approach balances query performance with maintainability."
        ),
        "source": "Ralph Kimball — The Data Warehouse Toolkit"
    },

    # ╔═══════════════════════════════════════════════════════════════════════╗
    # ║  BACKEND / API DOMAIN                                               ║
    # ╚═══════════════════════════════════════════════════════════════════════╝
    {
        "category": "Technical Skills",
        "domain": ["backend", "api", "django", "flask", "node", "spring", "rest", "microservice", "server"],
        "question": "How do you design a RESTful API that is easy to consume, version, and maintain?",
        "what_they_want": "REST design principles, versioning strategy, error handling, and documentation.",
        "model_answer": (
            "I follow resource-oriented design with clear nouns in URLs, standard HTTP verbs, and consistent response envelopes. "
            "For versioning I prefer URL path versioning (/v1/users) for simplicity. "
            "I include pagination, proper HTTP status codes, descriptive error objects, rate limiting, and auto-generated docs via OpenAPI/Swagger."
        ),
        "source": "Google API Design Guide"
    },
    {
        "category": "Technical Skills",
        "domain": ["backend", "api", "node", "python", "java", "server", "microservice"],
        "question": "Explain the difference between authentication and authorisation. How would you implement both in a REST API?",
        "what_they_want": "Security fundamentals — AuthN vs AuthZ, JWT, OAuth2, RBAC.",
        "model_answer": (
            "Authentication verifies identity ('Who are you?'); authorisation determines access ('What can you do?'). "
            "I'd use JWT tokens for stateless authentication, issued after credential validation (password hash check). "
            "For authorisation, I'd implement RBAC with middleware that checks the user's role against the endpoint's required permissions. "
            "OAuth2 handles third-party integrations, and refresh tokens provide secure session extension."
        ),
        "source": "OWASP Authentication Cheat Sheet"
    },
    {
        "category": "System Design",
        "domain": ["backend", "api", "microservice", "server", "distributed", "scale"],
        "question": "Design a URL shortener like bit.ly that handles 100M URLs and 1B redirects per day.",
        "what_they_want": "System design: encoding, storage, caching, load balancing, and scale estimation.",
        "model_answer": (
            "I'd use base62 encoding of an auto-increment ID for short URLs. Writes go to a primary database with a write-ahead log. "
            "Reads (redirects) are served from a CDN/edge cache layer backed by Redis, with the database as fallback. "
            "Consistent hashing distributes data across shards. Analytics events are streamed to Kafka for async processing. "
            "Rate limiting protects against abuse."
        ),
        "source": "System Design Interview — Alex Xu"
    },
    {
        "category": "Problem Solving",
        "domain": ["backend", "api", "server", "database", "production"],
        "question": "Your API endpoint's p99 latency jumped from 200ms to 3s overnight. Walk me through your debugging process.",
        "what_they_want": "Production debugging methodology — metrics, logs, profiling, hypothesis testing.",
        "model_answer": (
            "I'd check monitoring dashboards first: was there a deploy, traffic spike, or infra change? "
            "Then I'd look at database query times — slow queries are the #1 cause. I'd check connection pool usage, "
            "examine recent code changes in the endpoint, and profile the hot path with a flame graph. "
            "Common culprits: N+1 queries, missing indexes, or a shared resource under contention."
        ),
        "source": "SRE Workbook — Google"
    },
    {
        "category": "Technical Skills",
        "domain": ["backend", "api", "microservice", "distributed"],
        "question": "What is the CAP theorem and how does it affect your choice of database for a distributed system?",
        "what_they_want": "Understanding of distributed systems theory and practical trade-offs.",
        "model_answer": (
            "CAP states that a distributed system can guarantee at most two of: Consistency (all reads see the latest write), "
            "Availability (every request gets a response), and Partition tolerance (system works despite network splits). "
            "In practice, partitions are inevitable, so you choose CP (strong consistency like PostgreSQL/Spanner) "
            "or AP (high availability like Cassandra/DynamoDB). I choose based on whether the use case can tolerate stale reads."
        ),
        "source": "Designing Data-Intensive Applications — Martin Kleppmann"
    },

    # ╔═══════════════════════════════════════════════════════════════════════╗
    # ║  FRONTEND DOMAIN                                                    ║
    # ╚═══════════════════════════════════════════════════════════════════════╝
    {
        "category": "Technical Skills",
        "domain": ["frontend", "react", "vue", "angular", "css", "javascript", "ui", "web"],
        "question": "How do you optimise the performance of a large React application?",
        "what_they_want": "Rendering performance, code splitting, memoisation, and asset optimisation.",
        "model_answer": (
            "I'd start with React DevTools Profiler to find expensive re-renders and apply React.memo/useMemo where warranted. "
            "Code splitting with React.lazy reduces initial bundle size. For large lists I use virtualisation (react-window). "
            "On the network side: enable HTTP/2, cache static assets with long max-age, lazy-load images, and tree-shake unused code."
        ),
        "source": "React Performance Documentation"
    },
    {
        "category": "Technical Skills",
        "domain": ["frontend", "react", "vue", "angular", "javascript", "web"],
        "question": "Explain the Virtual DOM and how React's reconciliation algorithm works.",
        "what_they_want": "Understanding of React's rendering model and diffing strategy.",
        "model_answer": (
            "React maintains a lightweight in-memory representation of the actual DOM. On state changes, it creates a new virtual DOM tree, "
            "diffs it against the previous one (reconciliation), and applies only the minimal set of changes to the real DOM. "
            "It uses heuristics: elements of different types produce different trees, and keys help identify which items have changed in lists. "
            "React 18 adds concurrent rendering for interruptible updates."
        ),
        "source": "React Docs — Reconciliation"
    },
    {
        "category": "Technical Skills",
        "domain": ["frontend", "css", "javascript", "web", "accessibility"],
        "question": "How do you ensure a web application is accessible (WCAG compliant)?",
        "what_they_want": "Awareness of a11y best practices: semantic HTML, ARIA, keyboard navigation, screen readers.",
        "model_answer": (
            "I start with semantic HTML (button, nav, main, h1-h6) which gives screen readers structure for free. "
            "I ensure keyboard navigability, visible focus indicators, and proper ARIA labels where semantic HTML isn't enough. "
            "Color contrast ratios meet WCAG AA (4.5:1 for text). I test with axe DevTools and VoiceOver/NVDA regularly. "
            "Accessibility should be part of the definition of done, not an afterthought."
        ),
        "source": "WCAG 2.1 Guidelines — W3C"
    },
    {
        "category": "Problem Solving",
        "domain": ["frontend", "react", "javascript", "web", "css"],
        "question": "A user reports that a page takes 8 seconds to load on mobile. How do you diagnose and fix it?",
        "what_they_want": "Performance diagnosis: Lighthouse, bundle analysis, network waterfall, Core Web Vitals.",
        "model_answer": (
            "I'd run Lighthouse to get LCP, FID, and CLS scores. Then I'd analyse the network waterfall in DevTools: "
            "Is the bundle too large? Are there render-blocking resources? Unoptimised images? "
            "Common fixes: code-split the route, convert images to WebP, defer non-critical JS, "
            "add preload hints for critical resources, and enable server-side or static rendering for the initial paint."
        ),
        "source": "Google Web Vitals Documentation"
    },

    # ╔═══════════════════════════════════════════════════════════════════════╗
    # ║  DEVOPS / CLOUD DOMAIN                                              ║
    # ╚═══════════════════════════════════════════════════════════════════════╝
    {
        "category": "Technical Skills",
        "domain": ["devops", "docker", "kubernetes", "ci/cd", "terraform", "aws", "gcp", "azure", "cloud", "infra"],
        "question": "Describe how you would implement a zero-downtime CI/CD pipeline for a containerised service.",
        "what_they_want": "CI/CD knowledge: branching, build automation, container orchestration, blue-green/canary deployments.",
        "model_answer": (
            "I'd use GitHub Actions to build and push a Docker image on every merge to main. "
            "Kubernetes handles deployment with a rolling update strategy and readiness probes. "
            "Feature flags decouple deployment from release, and automated smoke tests gate promotion to production. "
            "For critical services, I'd add canary deployments that route 5% of traffic to the new version first."
        ),
        "source": "Continuous Delivery — Jez Humble"
    },
    {
        "category": "Technical Skills",
        "domain": ["devops", "docker", "kubernetes", "container", "cloud"],
        "question": "Explain the difference between Docker and Kubernetes. How do they complement each other?",
        "what_they_want": "Container fundamentals and orchestration understanding.",
        "model_answer": (
            "Docker packages an application and its dependencies into a container — a lightweight, portable, reproducible unit. "
            "Kubernetes orchestrates those containers at scale: scheduling, scaling, networking, and self-healing. "
            "Docker answers 'how to package' while Kubernetes answers 'how to run at scale'. "
            "In production, K8s manages Docker (or containerd) containers across a cluster of nodes."
        ),
        "source": "Kubernetes Up & Running — Kelsey Hightower"
    },
    {
        "category": "System Design",
        "domain": ["devops", "aws", "gcp", "azure", "cloud", "terraform", "infra"],
        "question": "Design a highly available, multi-region architecture for a SaaS application on AWS.",
        "what_they_want": "Cloud architecture: regions, AZs, load balancing, database replication, disaster recovery.",
        "model_answer": (
            "I'd deploy across two AWS regions with Route 53 latency-based routing. Each region has an ALB fronting an ECS/EKS cluster across 3 AZs. "
            "Primary database is Aurora Global with a read replica in the secondary region (RPO < 1s). "
            "Static assets go through CloudFront CDN. For disaster recovery, the secondary region has a warm standby that can promote within minutes. "
            "Infrastructure is defined in Terraform with reusable modules per region."
        ),
        "source": "AWS Well-Architected Framework"
    },
    {
        "category": "Problem Solving",
        "domain": ["devops", "cloud", "kubernetes", "docker", "infra", "production"],
        "question": "A production Kubernetes pod keeps crashing with OOMKilled. How do you debug it?",
        "what_they_want": "Container debugging: resource limits, memory profiling, log analysis.",
        "model_answer": (
            "First I'd check 'kubectl describe pod' for the OOMKilled status and current memory limits. "
            "Then I'd review application metrics — is the memory usage growing over time (leak) or spiking under load? "
            "I'd profile the app locally with similar traffic patterns. Common fixes: increase memory limits if genuinely needed, "
            "fix memory leaks (common in Node.js with event listeners or Java with classloader issues), "
            "or add horizontal scaling so each pod handles less load."
        ),
        "source": "Kubernetes Documentation — Managing Resources"
    },

    # ╔═══════════════════════════════════════════════════════════════════════╗
    # ║  CYBERSECURITY DOMAIN                                               ║
    # ╚═══════════════════════════════════════════════════════════════════════╝
    {
        "category": "Technical Skills",
        "domain": ["security", "cyber", "penetration", "soc", "vulnerability", "infosec"],
        "question": "Walk through how you would conduct a penetration test on a web application.",
        "what_they_want": "Structured methodology: reconnaissance, enumeration, exploitation, reporting.",
        "model_answer": (
            "I follow the OWASP Testing Guide. After scoping, I do passive and active reconnaissance, "
            "enumerate endpoints with Burp Suite, and probe for OWASP Top 10 vulnerabilities. "
            "Findings are documented with CVSS scores, reproduction steps, and remediation recommendations. "
            "I always stay within agreed scope and maintain detailed logs."
        ),
        "source": "OWASP Testing Guide v4"
    },
    {
        "category": "Technical Skills",
        "domain": ["security", "cyber", "infosec", "vulnerability"],
        "question": "Explain the OWASP Top 10. Which do you consider the most critical in modern web applications?",
        "what_they_want": "Knowledge of common web vulnerabilities and their mitigations.",
        "model_answer": (
            "The OWASP Top 10 lists the most critical web security risks: Broken Access Control, Cryptographic Failures, Injection, "
            "Insecure Design, Misconfiguration, Vulnerable Components, Identity Failures, Software Integrity Failures, "
            "Logging Failures, and SSRF. I consider Broken Access Control the most critical because it's the #1 vulnerability "
            "and often leads to full data breaches. Mitigation requires deny-by-default access control with server-side enforcement."
        ),
        "source": "OWASP Top 10 (2021)"
    },
    {
        "category": "Problem Solving",
        "domain": ["security", "cyber", "incident", "soc"],
        "question": "You discover that an attacker has been exfiltrating data for 3 days. Walk through your incident response.",
        "what_they_want": "Incident response process: contain, eradicate, recover, learn.",
        "model_answer": (
            "Phase 1 — Contain: isolate compromised systems, revoke affected credentials, and preserve forensic evidence. "
            "Phase 2 — Eradicate: identify the attack vector, remove malware/backdoors, and patch the vulnerability. "
            "Phase 3 — Recover: restore from clean backups, verify integrity, and gradually bring systems back online. "
            "Phase 4 — Learn: conduct a post-incident review, update detection rules, and notify affected parties per compliance requirements."
        ),
        "source": "NIST SP 800-61 — Computer Security Incident Handling Guide"
    },

    # ╔═══════════════════════════════════════════════════════════════════════╗
    # ║  MOBILE DEVELOPMENT DOMAIN                                          ║
    # ╚═══════════════════════════════════════════════════════════════════════╝
    {
        "category": "Technical Skills",
        "domain": ["mobile", "react native", "ios", "android", "swift", "kotlin", "flutter"],
        "question": "What are the key differences between native and cross-platform mobile development?",
        "what_they_want": "Understanding of trade-offs: performance, dev speed, platform access, UX fidelity.",
        "model_answer": (
            "Native (Swift/Kotlin) gives full platform API access, best performance, and native UX patterns, "
            "but requires maintaining two codebases. Cross-platform (React Native, Flutter) shares 80-90% of code "
            "with a single team, but may need native bridges for platform-specific features and can have subtle UI differences. "
            "I choose cross-platform for MVP/early stage and content-heavy apps, native for performance-critical or platform-deep apps."
        ),
        "source": "React Native vs Native — Thoughtbot Blog"
    },
    {
        "category": "Problem Solving",
        "domain": ["mobile", "react native", "ios", "android", "app"],
        "question": "Your mobile app crashes on launch for 5% of users after an update. How do you investigate?",
        "what_they_want": "Mobile crash debugging: crash reporting, device segmentation, rollback strategy.",
        "model_answer": (
            "I'd check crash reports in Firebase Crashlytics or Sentry, filtering by OS version, device model, and app version. "
            "Often crashes cluster on specific OS versions or older devices. I'd reproduce on similar hardware/emulators, "
            "check for null pointer exceptions or missing permissions, and push a hotfix. "
            "For critical crashes, I'd use staged rollout to limit exposure while debugging."
        ),
        "source": "Firebase Crashlytics Documentation"
    },

    # ╔═══════════════════════════════════════════════════════════════════════╗
    # ║  PRODUCT MANAGEMENT / BUSINESS DOMAIN                               ║
    # ╚═══════════════════════════════════════════════════════════════════════╝
    {
        "category": "Domain Knowledge",
        "domain": ["product", "pm", "product manager", "agile", "scrum", "stakeholder"],
        "question": "How do you prioritise features when you have more requests than capacity?",
        "what_they_want": "Prioritisation frameworks (RICE, ICE, MoSCoW), stakeholder management, data-driven decisions.",
        "model_answer": (
            "I use the RICE framework (Reach × Impact × Confidence / Effort) to score each feature request objectively. "
            "I then validate with customer data: support tickets, NPS feedback, and usage analytics. "
            "I present the prioritised list to stakeholders with the reasoning and trade-offs, "
            "and I'm transparent about what won't make it this quarter and why."
        ),
        "source": "Intercom — RICE Scoring"
    },
    {
        "category": "Problem Solving",
        "domain": ["product", "pm", "product manager", "business", "analytics"],
        "question": "A key product metric (e.g. activation rate) has dropped 20%. How do you investigate?",
        "what_they_want": "Analytical thinking, metric decomposition, and hypothesis-driven investigation.",
        "model_answer": (
            "First I'd verify the data: is this a tracking bug or a real change? Then I'd decompose the metric by segments "
            "(new vs returning users, platform, geography, acquisition channel) to isolate where the drop is concentrated. "
            "I'd check for recent changes: feature releases, UI changes, partner/marketing changes. "
            "Then I'd form hypotheses, validate with qualitative data (session recordings, user interviews), and prioritise fixes."
        ),
        "source": "Amplitude Analytics Guide"
    },

    # ╔═══════════════════════════════════════════════════════════════════════╗
    # ║  BLOCKCHAIN DOMAIN                                                  ║
    # ╚═══════════════════════════════════════════════════════════════════════╝
    {
        "category": "Technical Skills",
        "domain": ["blockchain", "solidity", "ethereum", "smart contract", "web3", "crypto", "defi"],
        "question": "Explain how smart contracts work and the key security considerations when writing one.",
        "what_they_want": "Understanding of immutability, gas, reentrancy, and common Solidity vulnerabilities.",
        "model_answer": (
            "Smart contracts are self-executing programs deployed on the blockchain that run when conditions are met. "
            "Key security considerations: reentrancy attacks (use checks-effects-interactions pattern), "
            "integer overflow (use SafeMath or Solidity 0.8+ built-in checks), front-running (commit-reveal schemes), "
            "and proper access control. Since contracts are immutable once deployed, thorough auditing before deployment is critical."
        ),
        "source": "ConsenSys Smart Contract Best Practices"
    },

    # ╔═══════════════════════════════════════════════════════════════════════╗
    # ║  QA / TESTING DOMAIN                                                ║
    # ╚═══════════════════════════════════════════════════════════════════════╝
    {
        "category": "Technical Skills",
        "domain": ["qa", "testing", "test", "selenium", "cypress", "automation", "quality"],
        "question": "What is the testing pyramid and how does it guide your testing strategy?",
        "what_they_want": "Understanding of test levels: unit, integration, e2e, and their trade-offs.",
        "model_answer": (
            "The testing pyramid suggests many fast unit tests at the base, fewer integration tests in the middle, "
            "and a small number of slow end-to-end tests at the top. This maximises test coverage while keeping the suite fast. "
            "Unit tests validate individual functions, integration tests verify component interactions, "
            "and e2e tests ensure critical user flows work. I aim for 70% unit, 20% integration, 10% e2e."
        ),
        "source": "Martin Fowler — Test Pyramid"
    },
    {
        "category": "Problem Solving",
        "domain": ["qa", "testing", "test", "automation", "quality"],
        "question": "A test passes locally but fails in CI. How do you debug it?",
        "what_they_want": "CI/CD debugging, test isolation, environment differences, flaky test handling.",
        "model_answer": (
            "Common causes: timing/race conditions (add explicit waits), environment differences (different DB, timezone, or locale), "
            "test order dependency (run in random order to detect), or resource constraints in CI (less CPU/memory). "
            "I'd first reproduce by running the full test suite locally in the same order. "
            "Then check CI logs for environment details and compare with local. Fix flaky tests by making them hermetic and deterministic."
        ),
        "source": "Google Testing Blog — Flaky Tests"
    },

    # ╔═══════════════════════════════════════════════════════════════════════╗
    # ║  DESIGN / UX DOMAIN                                                 ║
    # ╚═══════════════════════════════════════════════════════════════════════╝
    {
        "category": "Technical Skills",
        "domain": ["design", "ux", "ui", "figma", "user research", "wireframe", "prototype"],
        "question": "Walk me through your design process from a new feature request to a final design handoff.",
        "what_they_want": "End-to-end design process: research, ideation, prototyping, testing, and handoff.",
        "model_answer": (
            "I start with understanding the problem: user interviews, data analysis, and stakeholder goals. "
            "Then I sketch low-fidelity wireframes to explore multiple approaches. After team feedback, I create high-fidelity mockups in Figma "
            "with a design system for consistency. I validate with usability testing (5 users catches 80% of issues). "
            "Handoff includes annotated specs, interaction notes, and developer pairing for edge cases."
        ),
        "source": "Nielsen Norman Group — UX Process"
    },

    # ╔═══════════════════════════════════════════════════════════════════════╗
    # ║  CODING & ALGORITHMS (any technical role)                           ║
    # ╚═══════════════════════════════════════════════════════════════════════╝
    {
        "category": "Coding & Algorithms",
        "domain": ["software", "developer", "engineer", "backend", "frontend", "fullstack", "full stack"],
        "question": "Explain the time complexity of common data structures: arrays, hash maps, binary search trees, and heaps.",
        "what_they_want": "CS fundamentals — Big-O notation, trade-offs between data structures.",
        "model_answer": (
            "Arrays: O(1) access by index, O(n) search/insert/delete. Hash maps: O(1) average for get/set/delete, O(n) worst case with collisions. "
            "BSTs: O(log n) for balanced trees (search/insert/delete), O(n) for degenerate trees. "
            "Heaps: O(1) to peek min/max, O(log n) to insert/extract. "
            "I choose based on the access pattern: hash maps for lookups, heaps for priority queues, BSTs for ordered data."
        ),
        "source": "Cracking the Coding Interview — Gayle McDowell"
    },
    {
        "category": "Coding & Algorithms",
        "domain": ["software", "developer", "engineer", "backend"],
        "question": "How would you find the k-th largest element in an unsorted array? What's the time complexity?",
        "what_they_want": "Algorithm design: heap-based vs quickselect approach, complexity analysis.",
        "model_answer": (
            "Two approaches: (1) Use a min-heap of size k — iterate through the array, maintaining only k largest elements. O(n log k) time, O(k) space. "
            "(2) Quickselect — partition-based selection algorithm that's O(n) average, O(n²) worst case. "
            "For most cases I'd use the heap approach for its guaranteed O(n log k) and simplicity, "
            "or Python's heapq.nlargest which does exactly this."
        ),
        "source": "LeetCode — Top K Frequent Elements"
    },
    {
        "category": "Coding & Algorithms",
        "domain": ["software", "developer", "engineer"],
        "question": "What is dynamic programming? Give an example of when you'd use it.",
        "what_they_want": "Understanding of DP: overlapping subproblems, optimal substructure, memoisation vs tabulation.",
        "model_answer": (
            "Dynamic programming solves problems by breaking them into overlapping subproblems and caching results. "
            "It applies when a problem has optimal substructure (optimal solution uses optimal solutions to subproblems) "
            "and overlapping subproblems (same subproblems are solved repeatedly). "
            "Example: the knapsack problem — deciding which items to include to maximise value within a weight limit. "
            "I use memoisation (top-down) for readability and tabulation (bottom-up) when I need to optimise space."
        ),
        "source": "Introduction to Algorithms — CLRS"
    },

    # ╔═══════════════════════════════════════════════════════════════════════╗
    # ║  ADDITIONAL GENERAL QUESTIONS                                       ║
    # ╚═══════════════════════════════════════════════════════════════════════╝
    {
        "category": "Problem Solving",
        "domain": [],
        "question": "You are given a codebase or dataset with no documentation. How would you approach understanding and improving it?",
        "what_they_want": "Structured thinking, curiosity, and ability to work with ambiguity.",
        "model_answer": (
            "I'd start with a broad sweep: read any README, run the tests, and map the module structure. "
            "Then trace a single end-to-end flow to understand the main path. "
            "For code I'd use static analysis tools; for data, summary statistics and distribution plots. "
            "I document findings as I go and confirm assumptions with domain experts early."
        ),
        "source": "Pragmatic Programmer — Hunt & Thomas"
    },
    {
        "category": "System Design",
        "domain": [],
        "question": "Design a scalable notification system that supports email, SMS, push, and in-app notifications.",
        "what_they_want": "Ability to decompose, consider trade-offs, and design for scale and reliability.",
        "model_answer": (
            "I'd use an event-driven architecture. Producers emit notification events to a message queue (SQS/Kafka). "
            "A dispatch service reads events, applies user preferences (quiet hours, channel opt-ins), "
            "and fans out to channel-specific workers (email via SES, SMS via Twilio, push via FCM, in-app via WebSocket). "
            "Each worker has its own retry logic and dead-letter queue. Rate limiting prevents flooding."
        ),
        "source": "System Design Interview — Alex Xu"
    },
    {
        "category": "System Design",
        "domain": [],
        "question": "Design a rate limiter for an API. What algorithms would you consider?",
        "what_they_want": "Distributed systems design: token bucket, sliding window, Redis-based implementation.",
        "model_answer": (
            "Popular algorithms: Token Bucket (smooth, allows bursts), Sliding Window Log (precise but memory-heavy), "
            "and Sliding Window Counter (balance of precision and performance). "
            "I'd implement it as middleware using Redis for distributed tracking. Key = user_id + endpoint, "
            "value = counter with TTL. The token bucket approach is my default for its simplicity and burst-friendliness."
        ),
        "source": "System Design Primer — Donne Martin"
    },
    {
        "category": "Technical Skills",
        "domain": [],
        "question": "Describe your ideal Git workflow for a team of 5-10 developers.",
        "what_they_want": "Version control best practices: branching, PRs, CI integration, release management.",
        "model_answer": (
            "I prefer trunk-based development with short-lived feature branches. PRs require at least one review and must pass CI (lint, test, build). "
            "We use squash-merge to keep history clean. Release branches are cut from main for production fixes. "
            "Feature flags allow merging incomplete features without blocking others. "
            "Commit messages follow Conventional Commits for automated changelogs."
        ),
        "source": "Atlassian Git Workflow Guide"
    },
    {
        "category": "Domain Knowledge",
        "domain": [],
        "question": "What are the most important trends or challenges in the technology field right now?",
        "what_they_want": "Industry awareness, continuous learning, and ability to connect trends to practical work.",
        "model_answer": (
            "Key trends: AI/LLM integration into developer workflows, the shift to platform engineering, "
            "edge computing for latency-sensitive apps, and increasing regulation around data privacy and AI ethics. "
            "I stay current through newsletters (TLDR, Pragmatic Engineer), conference talks, open-source contributions, "
            "and hands-on experimentation with emerging tools in side projects."
        ),
        "source": "ThoughtWorks Technology Radar"
    },
    {
        "category": "Behavioral (STAR)",
        "domain": [],
        "question": "Tell me about a time you had to manage competing priorities from multiple stakeholders.",
        "what_they_want": "Stakeholder management, prioritisation, and communication under pressure.",
        "model_answer": (
            "The product team wanted a new feature, while the CTO wanted us to reduce tech debt. "
            "I proposed allocating 70% of the sprint to the feature and 30% to the most impactful tech debt items. "
            "I mapped the tech debt work to concrete risk reduction the CTO cared about, and showed the PM that the feature would ship "
            "only one day later. Both stakeholders agreed, and we delivered on both fronts."
        ),
        "source": "Lenny's Newsletter — PM Prioritisation"
    },
    {
        "category": "Technical Skills",
        "domain": ["python", "django", "flask", "fastapi"],
        "question": "What are Python decorators and how would you use them in a real project?",
        "what_they_want": "Language-specific knowledge: closures, higher-order functions, practical patterns.",
        "model_answer": (
            "Decorators are functions that wrap other functions to extend their behaviour without modifying their code. "
            "They leverage closures and higher-order functions. Common uses: @login_required for authentication, "
            "@cache for memoisation, @retry for automatic retries, and @validate for input validation. "
            "I've used custom decorators for rate limiting, logging request/response, and permission checking."
        ),
        "source": "Fluent Python — Luciano Ramalho"
    },
    {
        "category": "Technical Skills",
        "domain": ["javascript", "typescript", "node", "react", "frontend"],
        "question": "Explain closures in JavaScript with a practical example.",
        "what_they_want": "JS fundamentals: scope chain, lexical environment, and practical closure patterns.",
        "model_answer": (
            "A closure is a function that remembers variables from its outer lexical scope even after the outer function has returned. "
            "Practical example: a counter factory — function makeCounter() { let count = 0; return () => ++count; }. "
            "Each call to makeCounter creates a new independent counter. "
            "Closures power module patterns, callbacks, event handlers, and React hooks (useState captures state in a closure)."
        ),
        "source": "You Don't Know JS — Kyle Simpson"
    },
    {
        "category": "Technical Skills",
        "domain": ["java", "spring", "backend"],
        "question": "Explain the SOLID principles and give a real-world example of applying one.",
        "what_they_want": "OOP design principles and practical application.",
        "model_answer": (
            "SOLID: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion. "
            "For Open/Closed: I designed a notification system with a base NotificationSender interface. "
            "Adding SMS support meant creating a new SmsSender class implementing the interface — no changes to existing email/push code. "
            "The system is open for extension (new channels) but closed for modification (existing channels untouched)."
        ),
        "source": "Clean Architecture — Robert C. Martin"
    },
    {
        "category": "Handling Failure",
        "domain": [],
        "question": "Describe a time when you had to deal with a production outage. What was your role and what did you do?",
        "what_they_want": "Incident management skills, composure under pressure, and systematic problem-solving.",
        "model_answer": (
            "Our payment service went down during peak hours. As the on-call engineer, I immediately acknowledged the incident, "
            "created a war room, and began triaging. I identified a database migration that locked a critical table. "
            "I rolled back the migration, verified the service recovered, and communicated status updates every 15 minutes. "
            "The post-mortem led to adding migration safety checks and a read-only replica for zero-downtime migrations."
        ),
        "source": "Incident.io — On-Call Best Practices"
    },
    {
        "category": "Problem Solving",
        "domain": [],
        "question": "How do you approach debugging a complex issue that you've never seen before?",
        "what_they_want": "Systematic debugging methodology: reproduce, isolate, root-cause, fix, verify.",
        "model_answer": (
            "Step 1: Reproduce — get a consistent reproduction case. Step 2: Isolate — binary search through the system "
            "(is it frontend or backend? This service or that one?). Step 3: Gather evidence — logs, metrics, stack traces. "
            "Step 4: Form hypotheses and test the simplest one first. Step 5: Fix and add a regression test. "
            "I find that 80% of debugging time is reproduction; once I can reproduce, the fix usually follows quickly."
        ),
        "source": "Debugging: The 9 Indispensable Rules — David Agans"
    },
    {
        "category": "Culture Fit",
        "domain": [],
        "question": "What does 'ownership' mean to you in the context of software engineering?",
        "what_they_want": "End-to-end ownership mentality, proactivity, and accountability.",
        "model_answer": (
            "Ownership means being responsible for the full lifecycle: design, implementation, testing, deployment, monitoring, and maintenance. "
            "It means proactively fixing issues you discover (even if you didn't cause them), documenting your systems for the next person, "
            "and caring about the user experience, not just the code. An owner doesn't say 'it works on my machine' — they ensure it works in production."
        ),
        "source": "Amazon Leadership Principles — Ownership"
    },
    {
        "category": "Technical Skills",
        "domain": ["fullstack", "full stack", "software", "developer", "engineer"],
        "question": "How do you decide when to use a monolithic architecture versus microservices?",
        "what_they_want": "Architecture decision-making, understanding of trade-offs at different scales.",
        "model_answer": (
            "Start monolithic: faster development, simpler deployment, easier debugging. Move to microservices when you have: "
            "clear domain boundaries, team scaling challenges (teams stepping on each other), or specific components that need independent scaling. "
            "The worst approach is premature microservices — you get distributed system complexity without the benefits. "
            "I follow the 'monolith first' approach and extract services when there's a clear, painful reason."
        ),
        "source": "Martin Fowler — Monolith First"
    },
    {
        "category": "Technical Skills",
        "domain": ["api", "graphql", "backend", "fullstack"],
        "question": "Compare REST, GraphQL, and gRPC. When would you choose each?",
        "what_they_want": "API paradigm knowledge and ability to match technology to requirements.",
        "model_answer": (
            "REST: simple, well-understood, cacheable, ideal for CRUD and public APIs. "
            "GraphQL: client-driven queries, great when frontends need flexible data fetching from complex backends, reduces over/under-fetching. "
            "gRPC: binary protocol (protobuf), strongly typed, excellent for internal service-to-service communication where performance matters. "
            "I default to REST for simplicity, use GraphQL for complex frontend needs, and gRPC for microservice internals."
        ),
        "source": "API Design Patterns — JJ Geewax"
    },
]


def get_questions_for_role(job_title: str, job_description: str = "",
                           resume_text: str = "", count: int = 15) -> list:
    """
    Select the most relevant questions from the bank.

    Strategy:
      1. Detect domains from the combined text (title + desc + resume).
      2. Score each question: +2 if its domain matches, +1 if universal (empty domain).
      3. Pick top ``count`` questions, ensuring category diversity.
      4. Number them sequentially and fill in {role} placeholders.

    Returns a list of dicts ready for the API response.
    """
    import random as _rnd

    combined = (job_title + " " + job_description + " " + resume_text).lower()
    role_label = job_title or "Software Engineer"

    # Score questions by domain relevance
    scored = []
    for q in QUESTIONS_BANK:
        if q["domain"]:
            # domain-specific: score by how many domain keywords match
            matches = sum(1 for kw in q["domain"] if kw in combined)
            score = matches * 2  # 0 if none match
        else:
            # universal question
            score = 1

        if score > 0:
            scored.append((score, _rnd.random(), q))  # random tiebreaker

    scored.sort(key=lambda x: (-x[0], x[1]))

    # Pick top questions with category diversity
    selected = []
    category_counts: dict = {}
    max_per_category = max(2, count // len(CATEGORIES) + 1)

    for _score, _rnd_val, q in scored:
        cat = q["category"]
        if category_counts.get(cat, 0) >= max_per_category:
            continue
        selected.append(q)
        category_counts[cat] = category_counts.get(cat, 0) + 1
        if len(selected) >= count:
            break

    # If we don't have enough, fill with remaining universal questions
    if len(selected) < count:
        for _score, _rnd_val, q in scored:
            if q not in selected:
                selected.append(q)
                if len(selected) >= count:
                    break

    # Format output
    result = []
    for i, q in enumerate(selected, 1):
        result.append({
            "number": i,
            "category": q["category"],
            "question": q["question"].replace("{role}", role_label),
            "what_they_want": q["what_they_want"],
            "model_answer": q["model_answer"].replace("{role}", role_label),
            "source": q.get("source", ""),
        })

    return result
