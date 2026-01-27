"""
Database initialization and migration script

This script helps set up the database tables and optionally creates a test admin user.
"""

from app import create_app, db
from app.models import User, UserProfile, UserRole
from app.utils import hash_password
import os

def init_db():
    """Initialize database tables"""
    app = create_app()
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✓ Database tables created successfully!")
        
        # Check if any users exist
        user_count = User.query.count()
        
        if user_count == 0:
            print("\nNo users found. Would you like to create an admin user?")
            create_admin = input("Create admin user? (y/n): ").lower()
            
            if create_admin == 'y':
                email = input("Admin email: ")
                password = input("Admin password: ")
                first_name = input("First name: ")
                last_name = input("Last name: ")
                
                try:
                    # Create admin user
                    admin = User(
                        email=email,
                        password_hash=hash_password(password),
                        first_name=first_name,
                        last_name=last_name,
                        role=UserRole.ADMIN.value
                    )
                    db.session.add(admin)
                    db.session.flush()
                    
                    # Create admin profile
                    profile = UserProfile(
                        user_id=admin.id,
                        theme_preference='light'
                    )
                    db.session.add(profile)
                    db.session.commit()
                    
                    print(f"\n✓ Admin user created successfully!")
                    print(f"  Email: {email}")
                    print(f"  Role: admin")
                    
                except Exception as e:
                    db.session.rollback()
                    print(f"\n✗ Error creating admin user: {str(e)}")
        else:
            print(f"\n✓ Database already contains {user_count} user(s)")

def reset_db():
    """Drop all tables and recreate them (WARNING: This deletes all data!)"""
    app = create_app()
    
    with app.app_context():
        print("⚠️  WARNING: This will delete all data in the database!")
        confirm = input("Are you sure you want to continue? (yes/no): ")
        
        if confirm.lower() == 'yes':
            print("\nDropping all tables...")
            db.drop_all()
            print("✓ All tables dropped")
            
            print("\nCreating new tables...")
            db.create_all()
            print("✓ Database reset successfully!")
        else:
            print("Database reset cancelled.")

def seed_test_data():
    """Create test users for development"""
    app = create_app()
    
    with app.app_context():
        print("Creating test users...")
        
        test_users = [
            {
                'email': 'admin@hireskill.com',
                'password': 'Admin123',
                'first_name': 'Admin',
                'last_name': 'User',
                'role': UserRole.ADMIN.value
            },
            {
                'email': 'candidate@hireskill.com',
                'password': 'Candidate123',
                'first_name': 'Jane',
                'last_name': 'Candidate',
                'role': UserRole.CANDIDATE.value
            },
            {
                'email': 'employer@hireskill.com',
                'password': 'Employer123',
                'first_name': 'Company',
                'last_name': 'Recruiter',
                'role': UserRole.EMPLOYER.value
            }
        ]
        
        created_count = 0
        
        for user_data in test_users:
            # Check if user already exists
            existing = User.query.filter_by(email=user_data['email']).first()
            if existing:
                print(f"  ⊘ User {user_data['email']} already exists")
                continue
            
            try:
                user = User(
                    email=user_data['email'],
                    password_hash=hash_password(user_data['password']),
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    role=user_data['role']
                )
                db.session.add(user)
                db.session.flush()
                
                # Create profile with sample data
                profile = UserProfile(
                    user_id=user.id,
                    bio=f"{user_data['first_name']} is a {user_data['role']} on HireSkill",
                    skills=['Python', 'JavaScript', 'SQL'],
                    interests=['Technology', 'Innovation'],
                    theme_preference='light'
                )
                db.session.add(profile)
                
                created_count += 1
                print(f"  ✓ Created {user_data['email']} ({user_data['role']})")
                
            except Exception as e:
                print(f"  ✗ Error creating {user_data['email']}: {str(e)}")
        
        db.session.commit()
        print(f"\n✓ Created {created_count} test user(s)")
        
        if created_count > 0:
            print("\nTest User Credentials:")
            for user_data in test_users:
                print(f"  • {user_data['email']} / {user_data['password']}")

if __name__ == '__main__':
    print("=" * 50)
    print("HireSkill Database Management")
    print("=" * 50)
    print("\nOptions:")
    print("1. Initialize database (create tables)")
    print("2. Reset database (drop and recreate all tables)")
    print("3. Seed test data (create test users)")
    print("4. Exit")
    
    choice = input("\nSelect an option (1-4): ")
    
    if choice == '1':
        init_db()
    elif choice == '2':
        reset_db()
    elif choice == '3':
        seed_test_data()
    elif choice == '4':
        print("Exiting...")
    else:
        print("Invalid option selected.")
