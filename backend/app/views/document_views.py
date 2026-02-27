"""
Document Views (API Routes)
Endpoints for resume and cover letter generation
"""

import logging
from flask import Blueprint, request, current_app

logger = logging.getLogger(__name__)
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
        logger.exception('Error generating PDF: %s', e)
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
        logger.exception('Error analysing resume: %s', e)
        return error_response(f'Error analysing resume: {str(e)}', 500)


def _build_template_questions(job_title: str, job_description: str, resume_text: str) -> list:
    """
    Generate high-quality, role-aware interview questions from our 150+ question bank.
    Detects keywords from job_title / job_description / resume_text to return the
    most relevant questions across multiple categories and sources.
    """
    from app.ml.interview_questions_bank import get_questions_for_role
    return get_questions_for_role(
        job_title=job_title,
        job_description=job_description,
        resume_text=resume_text,
        count=15,
    )


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

            prompt = f"""You are an expert technical interviewer. Generate exactly 15 interview questions for:

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
      "model_answer": "...",
      "source": "..."
    }}
  ]
}}

Cover these categories: Technical Skills, Problem Solving, System Design, Behavioral (STAR), Teamwork, Handling Failure, Domain Knowledge, Career Goals, Leadership, Communication, Coding & Algorithms, Culture Fit.
Include a "source" field with the inspiration source (e.g. "STAR Framework", "System Design Interview", "OWASP Guide", etc.)."""

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
            {"questions": questions, "job_title": job_title, "source": "llm" if len(questions) > 8 else "template", "total_count": len(questions)},
            'Interview questions generated',
            200
        )

    except Exception as exc:
        logger.exception('Error generating questions: %s', exc)
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
