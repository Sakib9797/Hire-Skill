"""
Tests for core app health, auth flow, and interview question bank.
"""
import json


# ── Health ────────────────────────────────────────────────────────────────────

def test_health_endpoint(client):
    """GET /api/health should return 200 with status healthy."""
    resp = client.get('/api/health')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['status'] == 'healthy'


def test_security_headers(client):
    """Responses should include security headers."""
    resp = client.get('/api/health')
    assert resp.headers.get('X-Content-Type-Options') == 'nosniff'
    assert resp.headers.get('X-Frame-Options') == 'DENY'
    assert resp.headers.get('X-XSS-Protection') == '1; mode=block'


# ── Auth ──────────────────────────────────────────────────────────────────────

def test_register_and_login(client):
    """POST /api/auth/register then /api/auth/login should succeed."""
    # Register
    reg_payload = {
        'email': 'test_user@example.com',
        'password': 'StrongPass1!',
        'first_name': 'Test',
        'last_name': 'User',
        'role': 'user',
    }
    resp = client.post(
        '/api/auth/register',
        data=json.dumps(reg_payload),
        content_type='application/json',
    )
    # Accept 201 (created) or 200
    assert resp.status_code in (200, 201), resp.get_json()

    # Login
    login_payload = {'email': 'test_user@example.com', 'password': 'StrongPass1!'}
    resp = client.post(
        '/api/auth/login',
        data=json.dumps(login_payload),
        content_type='application/json',
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'access_token' in (data.get('data') or data)


def test_login_wrong_password(client):
    """Login with wrong password should fail."""
    payload = {'email': 'test_user@example.com', 'password': 'WrongPass9!'}
    resp = client.post(
        '/api/auth/login',
        data=json.dumps(payload),
        content_type='application/json',
    )
    assert resp.status_code in (401, 400)


# ── Interview Question Bank ───────────────────────────────────────────────────

def test_question_bank_returns_questions():
    """get_questions_for_role should return the requested number of questions."""
    from app.ml.interview_questions_bank import get_questions_for_role

    qs = get_questions_for_role('Backend Engineer', 'Python Flask REST API', '', count=10)
    assert len(qs) == 10
    for q in qs:
        assert 'question' in q
        assert 'category' in q
        assert 'model_answer' in q


def test_question_bank_domain_relevance():
    """Questions for an ML role should include ML-domain questions."""
    from app.ml.interview_questions_bank import get_questions_for_role

    qs = get_questions_for_role('ML Engineer', 'machine learning deep learning pytorch', '', count=15)
    categories = {q['category'] for q in qs}
    # Should have technical + behavioral spread
    assert len(categories) >= 4
