"""Test resume generation"""
from app import create_app, db
from app.controllers import DocumentController

app = create_app()

with app.app_context():
    print("Testing resume generation...")
    success, result, status = DocumentController.generate_resume(
        user_id=1,
        target_role="Software Engineer",
        template="professional"
    )
    
    print(f"\nSuccess: {success}")
    print(f"Status: {status}")
    if success:
        print(f"Result: {result}")
    else:
        print(f"Error: {result}")
