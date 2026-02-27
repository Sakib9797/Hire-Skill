"""
Salary Predictor — RandomForest ML Model
=========================================
Full ML pipeline: synthetic + rule-based training data
→ feature engineering → RandomForestRegressor → salary prediction.

Features used:
  - role_category  (encoded)
  - experience_level (encoded: entry=0, mid=1, senior=2, lead=3)
  - num_skills     (count of matching skills in user profile)
  - location_type  (remote=0, hybrid=1, onsite=2)
  - role_index     (ordinal of the specific role)
"""

import numpy as np
import joblib
import os
from typing import Dict, List, Tuple
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

# ─── Base salary ranges per role (USD annual) ─────────────────────────────────
_ROLE_SALARY = {
    "Full Stack Developer":      (75_000, 145_000),
    "Frontend Developer":        (65_000, 125_000),
    "Backend Developer":         (75_000, 145_000),
    "Data Scientist":            (90_000, 160_000),
    "Machine Learning Engineer": (105_000, 175_000),
    "AI Engineer":               (130_000, 200_000),
    "DevOps Engineer":           (85_000, 150_000),
    "Mobile Developer":          (75_000, 140_000),
    "Cloud Architect":           (115_000, 185_000),
    "Data Engineer":             (95_000, 160_000),
    "Cybersecurity Analyst":     (80_000, 145_000),
    "UI/UX Designer":            (60_000, 115_000),
    "Product Manager":           (90_000, 160_000),
    "QA Engineer":               (55_000, 105_000),
    "Blockchain Developer":      (95_000, 175_000),
    "Business Analyst":          (65_000, 120_000),
}

_EXPERIENCE_MULTIPLIER = {
    "entry":  0.75,
    "junior": 0.85,
    "mid":    1.00,
    "senior": 1.25,
    "lead":   1.45,
    "staff":  1.55,
    "principal": 1.65,
}

_LOCATION_BONUS = {
    "remote":  0.05,   # slight remote premium
    "hybrid":  0.02,
    "onsite":  0.00,
}

_SKILL_BONUS_PER_SKILL = 500   # $500 per additional matching skill (up to 20 skills)

ALL_ROLES = sorted(_ROLE_SALARY.keys())
ALL_CATEGORIES = ["AI/ML", "Blockchain", "Business", "Cloud Computing", "Data Engineering",
                  "Data Science", "Design", "Infrastructure", "Mobile Development",
                  "Product Management", "Quality Assurance", "Security", "Software Development"]

_ROLE_TO_CATEGORY = {
    "Full Stack Developer":      "Software Development",
    "Frontend Developer":        "Software Development",
    "Backend Developer":         "Software Development",
    "Data Scientist":            "Data Science",
    "Machine Learning Engineer": "AI/ML",
    "AI Engineer":               "AI/ML",
    "DevOps Engineer":           "Infrastructure",
    "Mobile Developer":          "Mobile Development",
    "Cloud Architect":           "Cloud Computing",
    "Data Engineer":             "Data Engineering",
    "Cybersecurity Analyst":     "Security",
    "UI/UX Designer":            "Design",
    "Product Manager":           "Product Management",
    "QA Engineer":               "Quality Assurance",
    "Blockchain Developer":      "Blockchain",
    "Business Analyst":          "Business",
}

_MODEL_PATH = os.path.join(os.path.dirname(__file__), "salary_model.joblib")


# ─── Training data generation ─────────────────────────────────────────────────
def _generate_training_data(n_samples: int = 3000) -> Tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(42)
    X, y = [], []

    for _ in range(n_samples):
        role = rng.choice(ALL_ROLES)
        role_idx = ALL_ROLES.index(role)
        cat_idx = ALL_CATEGORIES.index(_ROLE_TO_CATEGORY.get(role, "Software Development"))

        exp_key = rng.choice(list(_EXPERIENCE_MULTIPLIER.keys()))
        exp_idx = list(_EXPERIENCE_MULTIPLIER.keys()).index(exp_key)
        exp_years = {"entry": 0, "junior": 1, "mid": 3, "senior": 6, "lead": 9,
                     "staff": 11, "principal": 13}[exp_key] + rng.integers(0, 3)

        loc_key = rng.choice(list(_LOCATION_BONUS.keys()))
        loc_idx = list(_LOCATION_BONUS.keys()).index(loc_key)

        num_skills = int(rng.integers(3, 21))  # 3..20 skills

        base_lo, base_hi = _ROLE_SALARY[role]
        base = (base_lo + base_hi) / 2
        salary = (
            base
            * _EXPERIENCE_MULTIPLIER[exp_key]
            * (1 + _LOCATION_BONUS[loc_key])
            + num_skills * _SKILL_BONUS_PER_SKILL
            + exp_years * 1_500
            + rng.normal(0, 5_000)   # noise
        )
        salary = float(np.clip(salary, 30_000, 250_000))

        X.append([role_idx, cat_idx, exp_idx, exp_years, loc_idx, num_skills])
        y.append(salary)

    return np.array(X, dtype=np.float32), np.array(y, dtype=np.float32)


# ─── Train & save / load model ────────────────────────────────────────────────
def _train_and_save() -> RandomForestRegressor:
    X, y = _generate_training_data(4000)
    model = RandomForestRegressor(
        n_estimators=300,
        max_depth=12,
        min_samples_leaf=3,
        n_jobs=-1,
        random_state=42,
    )
    model.fit(X, y)
    joblib.dump(model, _MODEL_PATH)
    return model


_model: RandomForestRegressor = None


def _get_model() -> RandomForestRegressor:
    global _model
    if _model is not None:
        return _model
    if os.path.exists(_MODEL_PATH):
        _model = joblib.load(_MODEL_PATH)
    else:
        _model = _train_and_save()
    return _model


# ─── Public API ───────────────────────────────────────────────────────────────
def predict_salary(
    role: str,
    experience_level: str,
    experience_years: int,
    skills: List[str],
    location_type: str = "remote",
) -> Dict:
    """
    Predict salary for given inputs and return a rich dict.

    Returns:
      {
        "predicted_salary": 115000,
        "salary_range":     {"min": 103000, "max": 127000},
        "role":             "Machine Learning Engineer",
        "experience_level": "senior",
        "location_type":    "remote",
        "num_skills_matched": 8,
        "market_percentile": 72,
        "insights": [...],
        "top_skills_for_raise": [...],
      }
    """
    model = _get_model()

    # Normalise inputs
    role = role.strip()
    if role not in ALL_ROLES:
        # fuzzy match — pick closest
        role = _closest_role(role)

    exp_key = _normalise_exp(experience_level)
    loc_key = _normalise_loc(location_type)
    exp_years = max(0, min(int(experience_years), 30))

    role_idx = ALL_ROLES.index(role)
    cat_idx  = ALL_CATEGORIES.index(_ROLE_TO_CATEGORY.get(role, "Software Development"))
    exp_idx  = list(_EXPERIENCE_MULTIPLIER.keys()).index(exp_key)
    loc_idx  = list(_LOCATION_BONUS.keys()).index(loc_key)
    num_skills = min(len(skills), 20)

    features = np.array([[role_idx, cat_idx, exp_idx, exp_years, loc_idx, num_skills]],
                        dtype=np.float32)

    # Predict with individual tree estimates for range
    tree_preds = np.array([tree.predict(features)[0] for tree in model.estimators_])
    predicted  = float(np.mean(tree_preds))
    p10        = float(np.percentile(tree_preds, 15))
    p90        = float(np.percentile(tree_preds, 85))

    # Market percentile within role range
    lo, hi = _ROLE_SALARY.get(role, (50_000, 200_000))
    percentile = int(np.clip((predicted - lo) / max(hi - lo, 1) * 100, 5, 95))

    # Skills that would boost salary for this role
    from app.ml.career_data import CAREER_PATHS
    role_data = next((c for c in CAREER_PATHS if c["role"] == role), {})
    all_role_skills = set(
        (role_data.get("required_skills") or []) +
        (role_data.get("optional_skills") or [])
    )
    user_skills_lower = {s.lower() for s in skills}
    missing = [s for s in all_role_skills if s.lower() not in user_skills_lower][:5]

    insights = _build_insights(role, exp_key, loc_key, num_skills, predicted, lo, hi)

    return {
        "predicted_salary":     round(predicted / 1000) * 1000,
        "salary_range":         {"min": round(p10 / 1000) * 1000,
                                  "max": round(p90 / 1000) * 1000},
        "role":                 role,
        "category":             _ROLE_TO_CATEGORY.get(role, ""),
        "experience_level":     exp_key,
        "experience_years":     exp_years,
        "location_type":        loc_key,
        "num_skills_matched":   num_skills,
        "market_percentile":    percentile,
        "market_range":         {"min": lo, "max": hi},
        "top_skills_for_raise": missing,
        "insights":             insights,
    }


# ─── Helpers ──────────────────────────────────────────────────────────────────
def _closest_role(query: str) -> str:
    q = query.lower()
    for role in ALL_ROLES:
        if any(w in role.lower() for w in q.split()):
            return role
    return ALL_ROLES[0]


def _normalise_exp(raw: str) -> str:
    raw = (raw or "mid").lower().strip()
    mapping = {
        "0": "entry", "1": "junior", "2": "mid", "3": "senior", "4": "lead",
        "entry level": "entry", "fresher": "entry", "intern": "entry",
        "junior": "junior", "associate": "junior",
        "mid": "mid", "mid-level": "mid", "intermediate": "mid",
        "senior": "senior", "sr": "senior",
        "lead": "lead", "tech lead": "lead", "team lead": "lead",
        "staff": "staff", "principal": "principal",
    }
    return mapping.get(raw, "mid" if raw not in _EXPERIENCE_MULTIPLIER else raw)


def _normalise_loc(raw: str) -> str:
    raw = (raw or "remote").lower().strip()
    if "remote" in raw:
        return "remote"
    if "hybrid" in raw:
        return "hybrid"
    return "onsite"


def _build_insights(role, exp, loc, n_skills, predicted, lo, hi) -> List[str]:
    tips = []
    mid_salary = (lo + hi) / 2
    if predicted < mid_salary * 0.9:
        tips.append(f"You're below the market median for {role}. Adding 3-5 more skills could increase earnings by ~${_SKILL_BONUS_PER_SKILL * 4:,}.")
    elif predicted > mid_salary * 1.1:
        tips.append(f"You're above the market median for {role} — great positioning!")
    if loc == "onsite":
        tips.append("Negotiating a remote or hybrid arrangement could add ~5% to your effective compensation.")
    if exp in ("entry", "junior"):
        tips.append("Every year of experience at this stage adds ~$3,000-$5,000 annually. Focus on delivering measurable impact.")
    if n_skills < 8:
        tips.append(f"Professionals with 10+ relevant skills earn ${_SKILL_BONUS_PER_SKILL * 5:,}+ more on average.")
    tips.append("Salaries vary by company size: startups pay 10-20% less but often offer equity.")
    return tips[:4]
