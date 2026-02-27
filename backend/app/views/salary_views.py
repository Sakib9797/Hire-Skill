"""
Salary Prediction API Views
Endpoints for the ML-powered salary estimator
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.responses import success_response, error_response
from app import limiter
from app.ml.career_data import CAREER_PATHS, ALL_SKILLS

salary_bp = Blueprint('salary', __name__)


@salary_bp.route('/predict', methods=['POST'])
@limiter.limit("20 per minute")
def predict_salary():
    """
    Predict salary based on role, experience, skills, location.
    Public endpoint — no auth required so guests can try the tool.

    Body:
      {
        "role":               "Machine Learning Engineer",
        "experience_level":   "senior",          // entry|junior|mid|senior|lead
        "experience_years":   5,
        "skills":             ["Python", "TensorFlow", "Docker"],
        "location_type":      "remote"            // remote|hybrid|onsite
      }
    """
    try:
        from app.ml.salary_predictor import predict_salary as _predict
        data = request.get_json() or {}

        role             = data.get('role', '').strip()
        experience_level = data.get('experience_level', 'mid')
        experience_years = int(data.get('experience_years', 3))
        skills           = data.get('skills', [])
        location_type    = data.get('location_type', 'remote')

        if not role:
            return error_response('role is required', 400)
        if not isinstance(skills, list):
            skills = []

        result = _predict(
            role=role,
            experience_level=experience_level,
            experience_years=experience_years,
            skills=skills,
            location_type=location_type,
        )
        return success_response(result, 'Salary prediction complete', 200)

    except Exception as exc:
        import traceback; traceback.print_exc()
        return error_response(f'Prediction failed: {str(exc)}', 500)


@salary_bp.route('/roles', methods=['GET'])
@limiter.limit("60 per minute")
def get_roles():
    """Return all roles available for salary prediction."""
    from app.ml.salary_predictor import ALL_ROLES, _ROLE_SALARY, _ROLE_TO_CATEGORY
    roles = [
        {
            "role":     r,
            "category": _ROLE_TO_CATEGORY.get(r, ""),
            "range":    {"min": _ROLE_SALARY[r][0], "max": _ROLE_SALARY[r][1]},
        }
        for r in ALL_ROLES
    ]
    return success_response({"roles": roles}, "Roles fetched", 200)


@salary_bp.route('/skills', methods=['GET'])
@limiter.limit("60 per minute")
def get_skills():
    """Return all known skills for autocomplete."""
    return success_response({"skills": ALL_SKILLS}, "Skills fetched", 200)
