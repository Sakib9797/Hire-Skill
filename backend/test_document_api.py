"""
Test script for Document Generation API (Module 3)
Tests resume and cover letter generation endpoints
"""

import requests
import json
from datetime import datetime

BASE_URL = 'http://localhost:5000/api'

# Test credentials (use your existing test user)
TEST_EMAIL = 'sak11@gmail.com'  # Change this to your actual test account
TEST_PASSWORD = 'password123'  # Change this to your actual password

def print_section(title):
    """Print formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

def print_result(test_name, response):
    """Print test result"""
    status_icon = '✓' if response.status_code < 400 else '✗'
    print(f"\n{status_icon} {test_name}")
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")

def get_auth_token():
    """Login and get JWT token"""
    print_section("Authentication")
    
    response = requests.post(f'{BASE_URL}/auth/login', json={
        'email': TEST_EMAIL,
        'password': TEST_PASSWORD
    })
    
    if response.status_code == 200:
        token = response.json()['data']['access_token']
        print(f"✓ Logged in successfully")
        return token
    else:
        print(f"✗ Login failed: {response.json()}")
        return None

def test_health_check():
    """Test document service health check"""
    print_section("Health Check")
    
    response = requests.get(f'{BASE_URL}/documents/health')
    print_result("Document Service Health", response)
    return response.status_code == 200

def test_get_templates():
    """Test get resume templates"""
    print_section("Get Resume Templates")
    
    response = requests.get(f'{BASE_URL}/documents/templates')
    print_result("Get Templates", response)
    return response.status_code == 200

def test_get_tones():
    """Test get cover letter tones"""
    print_section("Get Cover Letter Tones")
    
    response = requests.get(f'{BASE_URL}/documents/tones')
    print_result("Get Tones", response)
    return response.status_code == 200

def test_generate_resume(token):
    """Test resume generation"""
    print_section("Resume Generation")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Test 1: Generate professional resume
    response = requests.post(
        f'{BASE_URL}/documents/resume/generate',
        headers=headers,
        json={
            'target_role': 'Software Engineer',
            'template': 'professional'
        }
    )
    print_result("Generate Professional Resume", response)
    
    if response.status_code == 201:
        resume_id = response.json()['data']['resume']['id']
        
        # Test 2: Generate modern resume
        response2 = requests.post(
            f'{BASE_URL}/documents/resume/generate',
            headers=headers,
            json={
                'target_role': 'Data Scientist',
                'template': 'modern'
            }
        )
        print_result("Generate Modern Resume", response2)
        
        return resume_id
    
    return None

def test_get_resumes(token):
    """Test get all resumes"""
    print_section("Get Resumes")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Get all resumes
    response = requests.get(f'{BASE_URL}/documents/resume', headers=headers)
    print_result("Get All Resumes", response)
    
    # Get current resumes only
    response2 = requests.get(
        f'{BASE_URL}/documents/resume?current_only=true',
        headers=headers
    )
    print_result("Get Current Resumes Only", response2)

def test_get_specific_resume(token, resume_id):
    """Test get specific resume"""
    print_section("Get Specific Resume")
    
    if not resume_id:
        print("Skipping - no resume ID available")
        return
    
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.get(
        f'{BASE_URL}/documents/resume/{resume_id}',
        headers=headers
    )
    print_result(f"Get Resume ID {resume_id}", response)

def test_update_resume(token, resume_id):
    """Test resume update (versioning)"""
    print_section("Update Resume (Create New Version)")
    
    if not resume_id:
        print("Skipping - no resume ID available")
        return
    
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.put(
        f'{BASE_URL}/documents/resume/{resume_id}',
        headers=headers,
        json={
            'summary': 'Updated professional summary with more achievements'
        }
    )
    print_result("Update Resume", response)

def test_generate_cover_letter(token, resume_id=None):
    """Test cover letter generation"""
    print_section("Cover Letter Generation")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Test 1: Generate professional cover letter
    response = requests.post(
        f'{BASE_URL}/documents/cover-letter/generate',
        headers=headers,
        json={
            'company_name': 'Google',
            'job_title': 'Software Engineer',
            'job_description': 'Build scalable systems',
            'requirements': ['Python', 'Distributed Systems', 'Cloud'],
            'tone': 'professional',
            'resume_id': resume_id
        }
    )
    print_result("Generate Professional Cover Letter", response)
    
    if response.status_code == 201:
        cover_letter_id = response.json()['data']['cover_letter']['id']
        
        # Test 2: Generate enthusiastic cover letter
        response2 = requests.post(
            f'{BASE_URL}/documents/cover-letter/generate',
            headers=headers,
            json={
                'company_name': 'Microsoft',
                'job_title': 'Cloud Engineer',
                'tone': 'enthusiastic'
            }
        )
        print_result("Generate Enthusiastic Cover Letter", response2)
        
        return cover_letter_id
    
    return None

def test_generate_custom_cover_letter(token):
    """Test custom cover letter generation"""
    print_section("Custom Cover Letter Generation")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.post(
        f'{BASE_URL}/documents/cover-letter/generate-custom',
        headers=headers,
        json={
            'custom_prompt': 'Emphasize my Python and Machine Learning skills, and highlight my leadership experience',
            'company_name': 'Amazon',
            'job_title': 'ML Engineer',
            'tone': 'professional'
        }
    )
    print_result("Generate Custom Cover Letter", response)

def test_get_cover_letters(token):
    """Test get all cover letters"""
    print_section("Get Cover Letters")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.get(f'{BASE_URL}/documents/cover-letter', headers=headers)
    print_result("Get All Cover Letters", response)

def test_get_specific_cover_letter(token, cover_letter_id):
    """Test get specific cover letter"""
    print_section("Get Specific Cover Letter")
    
    if not cover_letter_id:
        print("Skipping - no cover letter ID available")
        return
    
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.get(
        f'{BASE_URL}/documents/cover-letter/{cover_letter_id}',
        headers=headers
    )
    print_result(f"Get Cover Letter ID {cover_letter_id}", response)

def run_all_tests():
    """Run all document generation tests"""
    print("\n" + "="*60)
    print("  MODULE 3: DOCUMENT GENERATION API TESTS")
    print("  Started at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("="*60)
    
    # Get auth token
    token = get_auth_token()
    if not token:
        print("\n✗ Cannot proceed without authentication token")
        return
    
    # Run tests
    test_health_check()
    test_get_templates()
    test_get_tones()
    
    resume_id = test_generate_resume(token)
    test_get_resumes(token)
    test_get_specific_resume(token, resume_id)
    test_update_resume(token, resume_id)
    
    cover_letter_id = test_generate_cover_letter(token, resume_id)
    test_generate_custom_cover_letter(token)
    test_get_cover_letters(token)
    test_get_specific_cover_letter(token, cover_letter_id)
    
    # Summary
    print_section("TEST SUMMARY")
    print("\n✓ All tests completed!")
    print(f"\nIMPORTANT: Check responses above for any errors")
    print(f"Expected success codes:")
    print(f"  - 200 for GET requests")
    print(f"  - 201 for POST (create) requests")
    print(f"  - 400/404/500 indicate errors")

if __name__ == '__main__':
    try:
        run_all_tests()
    except Exception as e:
        print(f"\n✗ Test suite failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
