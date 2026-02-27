"""
Document Views (API Routes)
Endpoints for resume and cover letter generation
"""

from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers import DocumentController
from app.utils.responses import success_response, error_response
from app import limiter, cache

document_bp = Blueprint('document', __name__)


# =============== RESUME ENDPOINTS ===============

@document_bp.route('/resume/generate', methods=['POST'])
@jwt_required()
@limiter.limit(lambda: current_app.config.get('RATELIMIT_AI_GENERATION', "5 per minute"))
@cache.cached(timeout=300, key_prefix=lambda: f"resume_generate_{get_jwt_identity()}")
def generate_resume():
    """
    Generate a new ATS-compliant resume
    ---
    Request Body:
    {
        "target_role": "Software Engineer" (optional),
        "job_description": "Full job description text..." (optional),
        "template": "ats_professional" (optional, default: ats_professional)
    }
    """
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json() or {}
        
        target_role = data.get('target_role')
        job_description = data.get('job_description')
        template = data.get('template', 'ats_professional')
        
        success, result, status = DocumentController.generate_resume(
            user_id=user_id,
            target_role=target_role,
            job_description=job_description,
            template=template
        )
        
        if success:
            return success_response(result, result.get('message', 'Success'), status)
        else:
            return error_response(result, status)
            
    except Exception as e:
        return error_response(f'Server error: {str(e)}', 500)


@document_bp.route('/resume', methods=['GET'])
@jwt_required()
def get_resumes():
    """
    Get all resumes for current user
    ---
    Query Parameters:
    - current_only: boolean (default: false)
    """
    try:
        user_id = int(get_jwt_identity())
        current_only = request.args.get('current_only', 'false').lower() == 'true'
        
        success, result, status = DocumentController.get_user_resumes(
            user_id=user_id,
            current_only=current_only
        )
        
        if success:
            return success_response(result, 'Resumes retrieved successfully', status)
        else:
            return error_response(result, status)
            
    except Exception as e:
        return error_response(f'Server error: {str(e)}', 500)


@document_bp.route('/resume/<int:resume_id>', methods=['GET'])
@jwt_required()
def get_resume(resume_id):
    """Get specific resume"""
    try:
        user_id = int(get_jwt_identity())
        
        success, result, status = DocumentController.get_resume(
            resume_id=resume_id,
            user_id=user_id
        )
        
        if success:
            return success_response(result, 'Resume retrieved successfully', status)
        else:
            return error_response(result, status)
            
    except Exception as e:
        return error_response(f'Server error: {str(e)}', 500)


@document_bp.route('/resume/<int:resume_id>', methods=['PUT'])
@jwt_required()
def update_resume(resume_id):
    """
    Update resume (creates new version)
    ---
    Request Body:
    {
        "summary": "Updated summary text",
        "skills": {...},
        ...
    }
    """
    try:
        user_id = int(get_jwt_identity())
        updates = request.get_json() or {}
        
        if not updates:
            return error_response('No updates provided', 400)
        
        success, result, status = DocumentController.update_resume(
            resume_id=resume_id,
            user_id=user_id,
            updates=updates
        )
        
        if success:
            return success_response(result, result.get('message', 'Success'), status)
        else:
            return error_response(result, status)
            
    except Exception as e:
        return error_response(f'Server error: {str(e)}', 500)


@document_bp.route('/resume/<int:resume_id>', methods=['DELETE'])
@jwt_required()
def delete_resume(resume_id):
    """Delete resume"""
    try:
        user_id = int(get_jwt_identity())
        
        success, result, status = DocumentController.delete_resume(
            resume_id=resume_id,
            user_id=user_id
        )
        
        if success:
            return success_response(result, result['message'], status)
        else:
            return error_response(result, status)
            
    except Exception as e:
        return error_response(f'Server error: {str(e)}', 500)


# =============== COVER LETTER ENDPOINTS ===============

@document_bp.route('/cover-letter/generate', methods=['POST'])
@jwt_required()
@limiter.limit(lambda: current_app.config.get('RATELIMIT_AI_GENERATION', "5 per minute"))
@cache.cached(timeout=300, key_prefix=lambda: f"cover_letter_generate_{get_jwt_identity()}")
def generate_cover_letter():
    """
    Generate a new cover letter
    ---
    Request Body:
    {
        "company_name": "Company Name" (required),
        "job_title": "Job Title" (required),
        "job_description": "Description" (optional),
        "requirements": ["req1", "req2"] (optional),
        "tone": "professional" (optional: professional, friendly, formal, enthusiastic),
        "resume_id": 1 (optional)
    }
    """
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json() or {}
        
        # Validate required fields
        if not data.get('company_name') or not data.get('job_title'):
            return error_response('Company name and job title are required', 400)
        
        job_details = {
            'company_name': data['company_name'],
            'job_title': data['job_title'],
            'job_description': data.get('job_description', ''),
            'requirements': data.get('requirements', [])
        }
        
        tone = data.get('tone', 'professional')
        resume_id = data.get('resume_id')
        
        # Validate tone
        valid_tones = ['professional', 'friendly', 'formal', 'enthusiastic']
        if tone not in valid_tones:
            return error_response(f'Invalid tone. Choose from: {", ".join(valid_tones)}', 400)
        
        success, result, status = DocumentController.generate_cover_letter(
            user_id=user_id,
            job_details=job_details,
            tone=tone,
            resume_id=resume_id
        )
        
        if success:
            return success_response(result, result.get('message', 'Success'), status)
        else:
            return error_response(result, status)
            
    except Exception as e:
        return error_response(f'Server error: {str(e)}', 500)


@document_bp.route('/cover-letter/generate-custom', methods=['POST'])
@jwt_required()
@limiter.limit(lambda: current_app.config.get('RATELIMIT_AI_GENERATION', "5 per minute"))
@cache.cached(timeout=300, key_prefix=lambda: f"cover_letter_custom_{get_jwt_identity()}")
def generate_custom_cover_letter():
    """
    Generate cover letter with custom prompt
    ---
    Request Body:
    {
        "custom_prompt": "Emphasize my Python skills and leadership experience" (required),
        "company_name": "Company Name" (optional),
        "job_title": "Job Title" (optional),
        "tone": "professional" (optional)
    }
    """
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json() or {}
        
        custom_prompt = data.get('custom_prompt')
        if not custom_prompt:
            return error_response('Custom prompt is required', 400)
        
        job_details = None
        if data.get('company_name') and data.get('job_title'):
            job_details = {
                'company_name': data['company_name'],
                'job_title': data['job_title'],
                'job_description': data.get('job_description', ''),
                'requirements': data.get('requirements', [])
            }
        
        tone = data.get('tone', 'professional')
        
        success, result, status = DocumentController.generate_custom_cover_letter(
            user_id=user_id,
            custom_prompt=custom_prompt,
            job_details=job_details,
            tone=tone
        )
        
        if success:
            return success_response(result, result.get('message', 'Success'), status)
        else:
            return error_response(result, status)
            
    except Exception as e:
        return error_response(f'Server error: {str(e)}', 500)


@document_bp.route('/cover-letter', methods=['GET'])
@jwt_required()
def get_cover_letters():
    """
    Get all cover letters for current user
    ---
    Query Parameters:
    - current_only: boolean (default: false)
    """
    try:
        user_id = int(get_jwt_identity())
        current_only = request.args.get('current_only', 'false').lower() == 'true'
        
        success, result, status = DocumentController.get_user_cover_letters(
            user_id=user_id,
            current_only=current_only
        )
        
        if success:
            return success_response(result, 'Cover letters retrieved successfully', status)
        else:
            return error_response(result, status)
            
    except Exception as e:
        return error_response(f'Server error: {str(e)}', 500)


@document_bp.route('/cover-letter/<int:cover_letter_id>', methods=['GET'])
@jwt_required()
def get_cover_letter(cover_letter_id):
    """Get specific cover letter"""
    try:
        user_id = int(get_jwt_identity())
        
        success, result, status = DocumentController.get_cover_letter(
            cover_letter_id=cover_letter_id,
            user_id=user_id
        )
        
        if success:
            return success_response(result, 'Cover letter retrieved successfully', status)
        else:
            return error_response(result, status)
            
    except Exception as e:
        return error_response(f'Server error: {str(e)}', 500)


@document_bp.route('/cover-letter/<int:cover_letter_id>', methods=['DELETE'])
@jwt_required()
def delete_cover_letter(cover_letter_id):
    """Delete cover letter"""
    try:
        user_id = int(get_jwt_identity())
        
        success, result, status = DocumentController.delete_cover_letter(
            cover_letter_id=cover_letter_id,
            user_id=user_id
        )
        
        if success:
            return success_response(result, result['message'], status)
        else:
            return error_response(result, status)
            
    except Exception as e:
        return error_response(f'Server error: {str(e)}', 500)


# =============== UTILITY ENDPOINTS ===============

@document_bp.route('/templates', methods=['GET'])
def get_templates():
    """Get available resume templates"""
    from app.generators import ResumeGenerator
    
    templates = {
        name: {
            'name': name,
            'sections': config['sections'],
            'style': config['style']
        }
        for name, config in ResumeGenerator.TEMPLATES.items()
    }
    
    return success_response({'templates': templates}, 'Templates retrieved successfully', 200)


@document_bp.route('/tones', methods=['GET'])
def get_tones():
    """Get available cover letter tones"""
    from app.generators import CoverLetterGenerator
    
    tones = {
        name: {
            'name': name,
            'style': config['style'],
            'greeting': config['greeting'],
            'closing': config['closing']
        }
        for name, config in CoverLetterGenerator.TONES.items()
    }
    
    return success_response({'tones': tones}, 'Tones retrieved successfully', 200)


@document_bp.route('/parse-cv', methods=['POST'])
@jwt_required()
def parse_cv():
    """
    Parse uploaded CV PDF file
    ---
    Request: multipart/form-data with 'cv_file' field
    """
    try:
        # Check if file is present
        if 'cv_file' not in request.files:
            return error_response('No CV file uploaded', 400)
        
        cv_file = request.files['cv_file']
        
        if cv_file.filename == '':
            return error_response('No file selected', 400)
        
        # Check file type
        if not cv_file.filename.lower().endswith('.pdf'):
            return error_response('Only PDF files are supported', 400)
        
        # Parse the CV
        success, result, status = DocumentController.parse_cv_file(cv_file)
        
        if success:
            return success_response(result, result.get('message', 'Success'), status)
        else:
            return error_response(result, status)
            
    except Exception as e:
        return error_response(f'Server error: {str(e)}', 500)


@document_bp.route('/resume/generate-ats', methods=['POST'])
@jwt_required()
@limiter.limit(lambda: current_app.config.get('RATELIMIT_AI_GENERATION', "5 per minute"))
@cache.cached(timeout=300, key_prefix=lambda: f"ats_resume_{get_jwt_identity()}")
def generate_ats_resume():
    """
    Generate ATS-optimized resume
    ---
    Request: multipart/form-data (optional) or JSON
    - target_role: Target job role (optional)
    - cv_file: PDF file (optional)
    """
    try:
        user_id = int(get_jwt_identity())
        
        # Check if it's a file upload or JSON request
        cv_file = None
        target_role = None
        
        if request.content_type and 'multipart/form-data' in request.content_type:
            # File upload with form data
            cv_file = request.files.get('cv_file')
            target_role = request.form.get('target_role')
        else:
            # JSON request
            data = request.get_json() or {}
            target_role = data.get('target_role')
        
        # Generate ATS resume
        success, result, status = DocumentController.generate_ats_resume(
            user_id=user_id,
            target_role=target_role,
            cv_file=cv_file
        )
        
        if success:
            return success_response(result, result.get('message', 'Success'), status)
        else:
            return error_response(result, status)
            
    except Exception as e:
        return error_response(f'Server error: {str(e)}', 500)


@document_bp.route('/role-recommendations', methods=['GET'])
@jwt_required()
def get_role_recommendations():
    """
    Get template recommendations for a specific role
    ---
    Query params:
    - role: Target job role
    """
    try:
        role = request.args.get('role', '')
        
        if not role:
            return error_response('Role parameter is required', 400)
        
        success, result, status = DocumentController.get_role_recommendations(role)
        
        if success:
            return success_response(result, result.get('message', 'Success'), status)
        else:
            return error_response(result, status)
            
    except Exception as e:
        return error_response(f'Server error: {str(e)}', 500)


@document_bp.route('/resume/<int:resume_id>/download', methods=['GET'])
@jwt_required()
def download_resume_pdf(resume_id):
    """
    Download resume as PDF
    ---
    Returns ATS-compliant PDF resume
    """
    try:
        from flask import send_file
        from app.utils.pdf_generator import PDFGenerator
        import io
        
        user_id = int(get_jwt_identity())
        
        # Get resume
        from app.models.document import Resume
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        
        if not resume:
            return error_response('Resume not found', 404)
        
        # Generate PDF
        pdf_bytes = PDFGenerator.generate_resume_pdf(resume.content)
        
        # Create filename
        filename = f"resume_{resume.target_role or 'general'}_{resume.id}.pdf".replace(' ', '_')
        
        # Return PDF file
        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        import traceback
        print(f"Error generating PDF: {str(e)}")
        print(traceback.format_exc())
        return error_response(f'Error generating PDF: {str(e)}', 500)


@document_bp.route('/resume/versions/<int:user_id>', methods=['GET'])
@jwt_required()
def get_resume_versions(user_id):
    """
    Get all resume versions for a user
    ---
    Returns all resume versions with metadata
    """
    try:
        current_user_id = int(get_jwt_identity())
        
        # Authorization: users can only access their own versions
        if current_user_id != user_id:
            return error_response('Unauthorized access', 403)
        
        success, result, status = DocumentController.get_user_resumes(
            user_id=user_id,
            current_only=False
        )
        
        if success:
            return success_response(result, 'Resume versions retrieved successfully', status)
        else:
            return error_response(result, status)
            
    except Exception as e:
        return error_response(f'Server error: {str(e)}', 500)


@document_bp.route('/resume/check-ats', methods=['POST'])
@jwt_required()
def check_ats_resume():
    """
    Analyse an uploaded resume PDF for ATS compatibility.
    Accepts multipart/form-data with:
      - resume_file : PDF binary
      - target_role : string (optional)
    """
    from app.utils.cv_parser import CVParser
    from app.services.ats_checker import ATSChecker

    try:
        user_id = int(get_jwt_identity())

        # -- get file --------------------------------------------------------
        if 'resume_file' not in request.files:
            return error_response('No resume_file provided', 400)

        resume_file = request.files['resume_file']
        if not resume_file.filename.lower().endswith('.pdf'):
            return error_response('Only PDF files are supported', 400)

        target_role = request.form.get('target_role', '').strip() or None

        # -- extract text ----------------------------------------------------
        pdf_bytes = resume_file.read()
        pdf_text  = CVParser.extract_text_from_pdf(pdf_bytes)

        if not pdf_text or len(pdf_text.strip()) < 50:
            return error_response(
                'Could not extract text from the PDF. '
                'Make sure the PDF is not scanned/image-only.', 422
            )

        # -- run ATS analysis ------------------------------------------------
        result = ATSChecker.check(pdf_text, target_role)
        result['filename'] = resume_file.filename

        return success_response(result, 'ATS analysis complete', 200)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return error_response(f'Error analysing resume: {str(e)}', 500)


def _build_template_questions(job_title: str, job_description: str, resume_text: str) -> list:
    """
    Generate high-quality, role-aware interview questions without needing an LLM.
    Detects keywords from job_title / job_description to tailor the questions.
    """
    import re as _re

    title_lower = job_title.lower()
    desc_lower  = (job_description + ' ' + resume_text).lower()
    combined    = title_lower + ' ' + desc_lower

    # Detect domain
    is_ml        = any(w in combined for w in ['ml', 'machine learning', 'deep learning', 'model', 'tensorflow', 'pytorch', 'sklearn'])
    is_data      = any(w in combined for w in ['data', 'sql', 'analytics', 'bi', 'power bi', 'tableau', 'etl'])
    is_backend   = any(w in combined for w in ['backend', 'api', 'django', 'flask', 'node', 'spring', 'rest', 'microservice'])
    is_frontend  = any(w in combined for w in ['frontend', 'react', 'vue', 'angular', 'css', 'javascript', 'ui'])
    is_devops    = any(w in combined for w in ['devops', 'docker', 'kubernetes', 'ci/cd', 'terraform', 'aws', 'gcp', 'azure'])
    is_security  = any(w in combined for w in ['security', 'cyber', 'penetration', 'soc', 'vulnerability'])

    role = job_title or 'Software Engineer'

    # --- Domain-specific technical question ---
    if is_ml:
        tech_q = f"Walk me through how you would build and evaluate a classification model for a real-world {role} problem."
        tech_w = "Understanding of the end-to-end ML pipeline: data collection, feature engineering, model selection, evaluation metrics, and deployment."
        tech_a = ("I would start by defining the problem clearly and collecting representative labelled data. "
                  "After exploratory analysis and feature engineering, I'd train several baseline models (logistic regression, random forest) and compare them using cross-validation with metrics like precision, recall, and AUC. "
                  "I'd then tune the best model, check for overfitting with a held-out test set, and deploy using a REST API with monitoring for data/model drift.")
    elif is_data:
        tech_q = f"How would you design a data pipeline to feed a real-time analytics dashboard for a {role} use-case?"
        tech_w = "Knowledge of ETL/ELT, data modelling, streaming vs. batch, and BI tooling."
        tech_a = ("I'd identify source systems and data freshness requirements first. For real-time needs I'd use a streaming platform like Kafka or Pub/Sub, land data into a staging layer, apply transformations, and load into a columnar store like BigQuery or Redshift. "
                  "Batch jobs handle historical reconciliation. The BI layer (Power BI / Tableau) would sit on top of pre-aggregated materialised views for performance.")
    elif is_devops:
        tech_q = f"Describe how you would implement a zero-downtime CI/CD pipeline for a containerised {role} service."
        tech_w = "Hands-on CI/CD knowledge: branching strategy, build automation, container orchestration, blue-green or canary deployments."
        tech_a = ("I'd use GitHub Actions or GitLab CI to build and push a Docker image on every merge to main. "
                  "Kubernetes handles deployment with a rolling update strategy and readiness probes to ensure no traffic hits unhealthy pods. "
                  "Feature flags let us decouple deployment from release, and automated smoke tests gate the promotion to production.")
    elif is_frontend:
        tech_q = f"How do you optimise the performance of a React application for a {role} project with a large dataset?"
        tech_w = "Awareness of rendering performance, code splitting, memoisation, and asset optimisation."
        tech_a = ("I'd start with React DevTools Profiler to find expensive re-renders and apply React.memo / useMemo where warranted. "
                  "Code splitting with React.lazy reduces initial bundle size. For large lists I use virtualisation (react-window). "
                  "On the network side I'd enable HTTP/2, cache static assets, and lazy-load images.")
    elif is_security:
        tech_q = f"How would you approach a penetration test on a web application as part of a {role} engagement?"
        tech_w = "Structured methodology: reconnaissance, enumeration, exploitation, reporting."
        tech_a = ("I follow the OWASP Testing Guide. After scoping I do passive and active reconnaissance, enumerate endpoints with tools like Burp Suite, and probe for OWASP Top 10 vulnerabilities. "
                  "Findings are documented with CVSS scores, reproduction steps, and remediation recommendations. I always stay within agreed scope and document all actions.")
    else:
        tech_q = f"Describe the most complex technical problem you solved in a previous {role} role."
        tech_w = "Depth of technical expertise, structured problem-solving, and communication skills."
        tech_a = ("In my last role I debugged a production memory leak in a Node.js service. "
                  "I used heap snapshots in Chrome DevTools to isolate retained closures in an event-emitter accumulating listeners. "
                  "After fixing the root cause and adding an integration test to catch regressions, memory usage dropped by 60% and p99 latency improved by 30%.")

    questions = [
        {
            "number": 1,
            "category": "Technical Skills",
            "question": tech_q,
            "what_they_want": tech_w,
            "model_answer": tech_a
        },
        {
            "number": 2,
            "category": "Problem Solving",
            "question": f"You are given a dataset (or codebase) for a {role} project that has no documentation. How would you approach understanding and improving it?",
            "what_they_want": "Structured thinking, curiosity, and the ability to work with ambiguity.",
            "model_answer": (
                f"I'd start with a broad sweep — reading any README, running the tests, and mapping the data schema or module structure. "
                "I'd then trace a single end-to-end flow to understand the main path before going deeper. "
                "For a codebase I'd use static analysis tools; for a dataset, summary statistics and distribution plots. "
                "I document findings as I go and confirm assumptions with subject-matter experts early to avoid wasted effort."
            )
        },
        {
            "number": 3,
            "category": "System Design",
            "question": f"Design a scalable system for a core feature of a {role} product (e.g. a recommendation engine, job-matching service, or real-time notification system).",
            "what_they_want": "Ability to decompose a problem, consider trade-offs, and design for scale, reliability, and maintainability.",
            "model_answer": (
                "I'd start by clarifying requirements: expected QPS, latency SLA, consistency needs, and growth projections. "
                "I'd decompose into an ingestion layer, a processing/ML layer, and a serving layer, choosing async queues for decoupling. "
                "A caching layer (Redis) handles hot data. I'd discuss trade-offs like SQL vs. NoSQL depending on the access patterns, "
                "and include monitoring, alerting, and graceful degradation from the start."
            )
        },
        {
            "number": 4,
            "category": "Behavioral (STAR)",
            "question": f"Tell me about a time you delivered a {role} project under a tight deadline. How did you prioritise?",
            "what_they_want": "Time management, prioritisation, stakeholder communication, and delivery under pressure.",
            "model_answer": (
                "In a previous role, we had two weeks to ship a feature that usually takes a month. "
                "I sat down with the PM to identify the must-have MVP slice and deferred nice-to-haves to the next sprint. "
                "I broke the work into daily milestones and flagged blockers in standups immediately. "
                "We shipped on time with all critical acceptance criteria met, and completed the remaining items in the next cycle with no quality debt."
            )
        },
        {
            "number": 5,
            "category": "Teamwork",
            "question": "Describe a situation where you had a technical disagreement with a colleague. How did you resolve it?",
            "what_they_want": "Collaboration, empathy, evidence-based decision making, and professionalism.",
            "model_answer": (
                "We disagreed on whether to use a REST or GraphQL API for a new service. "
                "Rather than debating opinions, I proposed we both write a spike: I implemented the REST version and my colleague did GraphQL — each against the same acceptance criteria. "
                "We compared developer experience, payload size, and query flexibility. The data led us to GraphQL for that use-case. "
                "The structured approach removed the personal element and we both learned something."
            )
        },
        {
            "number": 6,
            "category": "Handling Failure",
            "question": "Tell me about a project or feature you worked on that failed or did not go as planned. What did you learn?",
            "what_they_want": "Self-awareness, accountability, resilience, and growth mindset.",
            "model_answer": (
                "I once released a feature without adequate load testing. Under production traffic it caused database connection pool exhaustion. "
                "I owned the incident, rolled back quickly, and wrote a post-mortem with no blame. "
                "We added load testing to our CI pipeline and set connection pool metrics as SLOs. "
                "It was uncomfortable but it permanently improved the team's reliability practices."
            )
        },
        {
            "number": 7,
            "category": "Domain Knowledge",
            "question": f"What are the most important trends or challenges in the {job_title or 'technology'} field right now, and how are you keeping up with them?",
            "what_they_want": "Industry awareness, continuous learning, and ability to connect trends to practical work.",
            "model_answer": (
                f"In the {job_title or 'tech'} space, the biggest shifts I'm tracking are the rapid adoption of LLM-based tooling, "
                "the push toward platform engineering to reduce developer cognitive load, and increasing regulatory focus on AI fairness and data privacy. "
                "I stay current through a mix of reading papers (arXiv, Google Research blog), following practitioners on LinkedIn, "
                "contributing to open-source projects, and applying new techniques in personal projects before using them at work."
            )
        },
        {
            "number": 8,
            "category": "Career Goals",
            "question": f"Where do you see yourself in 3 years, and why is the {role} position a step toward that goal?",
            "what_they_want": "Ambition, alignment between role and personal growth, and genuine interest in the company.",
            "model_answer": (
                f"In three years I aim to be a senior {role} who ships impactful systems and mentors junior teammates. "
                "This role is a strong fit because it involves the scale and complexity I want to work on, and the team's emphasis on engineering excellence aligns with how I want to grow. "
                "I'm particularly excited by the opportunity to work across the full stack of the problem — from data to deployment — rather than a narrow slice."
            )
        },
    ]

    return questions


@document_bp.route('/interview-prep', methods=['POST'])
@jwt_required()
@limiter.limit("10 per minute")
def generate_interview_questions():
    """
    Generate tailored interview questions + model answers.
    Tries LLM first; falls back to smart templates if LLM is unavailable.
    Body: { "job_title": "...", "job_description": "...", "resume_text": "..." }
    """
    try:
        int(get_jwt_identity())
        data = request.get_json() or {}

        job_title       = data.get('job_title', '').strip()
        job_description = data.get('job_description', '').strip()
        resume_text     = data.get('resume_text', '').strip()

        if not job_title and not job_description:
            return error_response('job_title or job_description is required', 400)

        questions = []

        # --- Try LLM first ---
        try:
            from app.generators.cover_letter_generator import CoverLetterGenerator
            import json, re

            resume_context = (
                f"\n\nCandidate Resume Summary:\n{resume_text[:1500]}" if resume_text else ""
            )

            prompt = f"""You are an expert technical interviewer. Generate exactly 8 interview questions for:

Job Title: {job_title or 'Software Engineer'}
Job Description: {job_description[:1000] if job_description else 'A technical role.'}
{resume_context}

Return ONLY valid JSON in this exact format:
{{
  "questions": [
    {{
      "number": 1,
      "category": "Technical Skills",
      "question": "...",
      "what_they_want": "...",
      "model_answer": "..."
    }}
  ]
}}

Cover: Technical Skills, Problem Solving, System Design, Behavioral (STAR), Teamwork, Handling Failure, Domain Knowledge, Career Goals."""

            raw = CoverLetterGenerator._call_llm(prompt)
            if raw:
                json_match = re.search(r'\{[\s\S]*\}', raw)
                if json_match:
                    try:
                        parsed = json.loads(json_match.group())
                        questions = parsed.get('questions', [])
                    except json.JSONDecodeError:
                        pass
        except Exception:
            pass  # LLM unavailable — fall through to template

        # --- Template fallback ---
        if not questions:
            questions = _build_template_questions(job_title, job_description, resume_text)

        return success_response(
            {"questions": questions, "job_title": job_title, "source": "llm" if questions and len(questions) > 1 else "template"},
            'Interview questions generated',
            200
        )

    except Exception as exc:
        import traceback; traceback.print_exc()
        return error_response(f'Error generating questions: {str(exc)}', 500)


@document_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return success_response({
        'service': 'ATS Document Generation Service',
        'status': 'healthy',
        'features': [
            'ATS-compliant resume checking with LLM',
            'Keyword-optimized cover letter generation',
            'Interview question generation',
            'Versioned document storage',
            'JSON schema validation',
            'PDF export (ATS-friendly format)',
            'Resume version tracking',
            'Keyword matching analysis'
        ]
    }, 'Document service is operational', 200)
