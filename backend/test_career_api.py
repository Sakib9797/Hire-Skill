"""
Test script for Career Recommendation API
Run this to verify all endpoints are working
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def print_response(response, title):
    """Print formatted response"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        data = response.json()
        print(json.dumps(data, indent=2))
    except:
        print(response.text)
    print()

def test_health():
    """Test health check endpoint"""
    url = f"{BASE_URL}/api/career/health"
    response = requests.get(url)
    print_response(response, "1. Health Check")
    return response.status_code == 200

def test_get_all_careers():
    """Test get all careers endpoint"""
    url = f"{BASE_URL}/api/career/careers"
    response = requests.get(url)
    print_response(response, "2. Get All Careers")
    return response.status_code == 200

def test_get_career_details():
    """Test get specific career details"""
    url = f"{BASE_URL}/api/career/careers/Full Stack Developer"
    response = requests.get(url)
    print_response(response, "3. Get Career Details - Full Stack Developer")
    return response.status_code == 200

def test_get_skills():
    """Test get all skills endpoint"""
    url = f"{BASE_URL}/api/career/skills"
    response = requests.get(url)
    data = response.json()
    print(f"\n{'='*60}")
    print("4. Get All Skills")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    print(f"Total Skills: {data['data']['total_skills']}")
    print(f"Sample Skills: {', '.join(data['data']['skills'][:10])}")
    print()
    return response.status_code == 200

def test_recommendations_without_auth():
    """Test recommendations endpoint without authentication"""
    url = f"{BASE_URL}/api/career/recommend"
    response = requests.get(url)
    print_response(response, "5. Get Recommendations (No Auth - Should Fail)")
    return response.status_code == 401

def test_skill_gap_without_auth():
    """Test skill gap endpoint without authentication"""
    url = f"{BASE_URL}/api/career/skill-gap/Data Scientist"
    response = requests.get(url)
    print_response(response, "6. Skill Gap Analysis (No Auth - Should Fail)")
    return response.status_code == 401

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("AI CAREER RECOMMENDATION API - TEST SUITE")
    print("="*60)
    
    tests = [
        ("Health Check", test_health),
        ("Get All Careers", test_get_all_careers),
        ("Get Career Details", test_get_career_details),
        ("Get All Skills", test_get_skills),
        ("Recommendations Without Auth", test_recommendations_without_auth),
        ("Skill Gap Without Auth", test_skill_gap_without_auth),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"\nERROR in {name}: {str(e)}")
            results.append((name, False))
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("="*60)
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Career Recommendation API is working perfectly!")
    else:
        print("\n⚠️ Some tests failed. Please check the backend logs.")
    
    print("\n" + "="*60)
    print("FOR AUTHENTICATED ENDPOINTS:")
    print("="*60)
    print("1. Login at: http://localhost:3000/login")
    print("2. Get access token from browser DevTools → Application → Local Storage")
    print("3. Use token in Authorization header:")
    print("   curl -H 'Authorization: Bearer YOUR_TOKEN' \\")
    print("        'http://localhost:5000/api/career/recommend'")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        run_all_tests()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to backend server!")
        print("Please make sure the backend is running:")
        print("  cd d:\\Github\\Hire-Skill\\backend")
        print("  python run.py")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
