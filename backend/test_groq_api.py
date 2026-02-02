"""
Test Groq API Integration
Quick test to verify Groq API is working correctly
"""

import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

LLM_API_URL = os.getenv('LLM_API_URL')
LLM_MODEL = os.getenv('LLM_MODEL')
LLM_API_KEY = os.getenv('LLM_API_KEY')

print("=" * 60)
print("Testing Groq API Configuration")
print("=" * 60)
print(f"API URL: {LLM_API_URL}")
print(f"Model: {LLM_MODEL}")
print(f"API Key: {LLM_API_KEY[:20]}..." if LLM_API_KEY else "No API Key")
print()

def test_groq_api():
    """Test basic Groq API call"""
    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {LLM_API_KEY}'
        }
        
        data = {
            'model': LLM_MODEL,
            'messages': [
                {
                    'role': 'user',
                    'content': 'Say "Hello from Groq API!" and nothing else.'
                }
            ],
            'temperature': 0.7,
            'max_tokens': 50
        }
        
        print("Sending test request to Groq API...")
        response = requests.post(
            LLM_API_URL,
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            message = result['choices'][0]['message']['content']
            print("✅ SUCCESS! Groq API is working!")
            print(f"Response: {message}")
            print(f"Model used: {result.get('model', 'N/A')}")
            print(f"Tokens used: {result.get('usage', {}).get('total_tokens', 'N/A')}")
            return True
        else:
            print(f"❌ ERROR: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_resume_generation():
    """Test resume generation prompt"""
    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {LLM_API_KEY}'
        }
        
        prompt = """Generate a simple ATS-friendly resume in JSON format for a software engineer.
Return ONLY valid JSON with this structure:
{
  "personal_info": {"full_name": "John Doe", "email": "john@email.com", "phone": "555-0100"},
  "summary": "Software engineer with 3 years of experience",
  "skills": {"technical": ["Python", "JavaScript"], "soft": ["Communication"], "tools": ["Git"]}
}"""
        
        data = {
            'model': LLM_MODEL,
            'messages': [
                {
                    'role': 'system',
                    'content': 'You are a professional resume generator. Always respond with valid JSON only.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'temperature': 0.5,
            'max_tokens': 500
        }
        
        print("\n" + "=" * 60)
        print("Testing Resume Generation")
        print("=" * 60)
        print("Generating test resume...")
        
        response = requests.post(
            LLM_API_URL,
            headers=headers,
            json=data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # Try to parse as JSON
            try:
                resume_json = json.loads(content)
                print("✅ SUCCESS! Resume generated successfully!")
                print(f"Resume preview: {json.dumps(resume_json, indent=2)[:200]}...")
                return True
            except json.JSONDecodeError:
                print("⚠️ WARNING: Response is not valid JSON")
                print(f"Response: {content[:200]}...")
                return False
        else:
            print(f"❌ ERROR: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    # Test 1: Basic API connectivity
    test1_passed = test_groq_api()
    
    # Test 2: Resume generation
    test2_passed = test_resume_generation()
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Basic API Test: {'✅ PASS' if test1_passed else '❌ FAIL'}")
    print(f"Resume Generation Test: {'✅ PASS' if test2_passed else '❌ FAIL'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 All tests passed! Groq API is ready to use!")
    else:
        print("\n⚠️ Some tests failed. Please check the configuration.")
