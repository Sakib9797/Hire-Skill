"""
Pytest configuration — shared fixtures for the HireSkillz test suite.
"""
import os
import pytest

# Force testing config before anything imports create_app
os.environ['FLASK_ENV'] = 'testing'

from app import create_app, db as _db


@pytest.fixture(scope='session')
def app():
    """Create application for testing."""
    app = create_app('testing')
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture()
def client(app):
    """Flask test client."""
    return app.test_client()


@pytest.fixture()
def db(app):
    """Database session for a test — rolled back after each test."""
    with app.app_context():
        yield _db
