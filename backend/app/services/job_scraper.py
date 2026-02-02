"""
Mock Job Scraping Service
Safely generates realistic job postings without actual web scraping
"""
from datetime import datetime, timedelta
import random
from typing import List, Dict, Optional

class JobScraper:
    """Mock job scraper that generates realistic job postings"""
    
    # Mock data for generating realistic jobs
    COMPANIES = [
        {'name': 'Google', 'logo': 'https://logo.clearbit.com/google.com'},
        {'name': 'Microsoft', 'logo': 'https://logo.clearbit.com/microsoft.com'},
        {'name': 'Amazon', 'logo': 'https://logo.clearbit.com/amazon.com'},
        {'name': 'Meta', 'logo': 'https://logo.clearbit.com/meta.com'},
        {'name': 'Apple', 'logo': 'https://logo.clearbit.com/apple.com'},
        {'name': 'Netflix', 'logo': 'https://logo.clearbit.com/netflix.com'},
        {'name': 'Tesla', 'logo': 'https://logo.clearbit.com/tesla.com'},
        {'name': 'Spotify', 'logo': 'https://logo.clearbit.com/spotify.com'},
        {'name': 'Airbnb', 'logo': 'https://logo.clearbit.com/airbnb.com'},
        {'name': 'Uber', 'logo': 'https://logo.clearbit.com/uber.com'},
        {'name': 'LinkedIn', 'logo': 'https://logo.clearbit.com/linkedin.com'},
        {'name': 'Salesforce', 'logo': 'https://logo.clearbit.com/salesforce.com'},
        {'name': 'Adobe', 'logo': 'https://logo.clearbit.com/adobe.com'},
        {'name': 'IBM', 'logo': 'https://logo.clearbit.com/ibm.com'},
        {'name': 'Oracle', 'logo': 'https://logo.clearbit.com/oracle.com'},
        {'name': 'Nvidia', 'logo': 'https://logo.clearbit.com/nvidia.com'},
        {'name': 'Intel', 'logo': 'https://logo.clearbit.com/intel.com'},
        {'name': 'Cisco', 'logo': 'https://logo.clearbit.com/cisco.com'},
        {'name': 'Shopify', 'logo': 'https://logo.clearbit.com/shopify.com'},
        {'name': 'Stripe', 'logo': 'https://logo.clearbit.com/stripe.com'}
    ]
    
    LOCATIONS = [
        'San Francisco, CA', 'New York, NY', 'Seattle, WA', 'Austin, TX',
        'Boston, MA', 'Chicago, IL', 'Los Angeles, CA', 'Denver, CO',
        'Remote', 'Hybrid - San Francisco', 'Hybrid - New York'
    ]
    
    JOB_TITLES = {
        'software_engineer': [
            'Software Engineer', 'Senior Software Engineer', 'Staff Software Engineer',
            'Backend Engineer', 'Frontend Engineer', 'Full Stack Engineer'
        ],
        'data_science': [
            'Data Scientist', 'Senior Data Scientist', 'Machine Learning Engineer',
            'AI Engineer', 'Data Analyst', 'ML Research Scientist'
        ],
        'product': [
            'Product Manager', 'Senior Product Manager', 'Product Designer',
            'UX Designer', 'UI/UX Designer', 'Product Lead'
        ],
        'devops': [
            'DevOps Engineer', 'Site Reliability Engineer', 'Cloud Engineer',
            'Infrastructure Engineer', 'Platform Engineer'
        ],
        'security': [
            'Security Engineer', 'Security Analyst', 'Cybersecurity Specialist',
            'Application Security Engineer', 'Security Architect'
        ]
    }
    
    SKILLS_BY_ROLE = {
        'software_engineer': ['Python', 'Java', 'JavaScript', 'TypeScript', 'React', 'Node.js', 'SQL', 'Git', 'AWS', 'Docker'],
        'data_science': ['Python', 'R', 'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch', 'SQL', 'Pandas', 'NumPy', 'Statistics'],
        'product': ['Product Strategy', 'User Research', 'Agile', 'Jira', 'Roadmapping', 'Analytics', 'Figma', 'Stakeholder Management'],
        'devops': ['Kubernetes', 'Docker', 'AWS', 'Azure', 'Terraform', 'CI/CD', 'Jenkins', 'Monitoring', 'Linux', 'Python'],
        'security': ['Security Analysis', 'Penetration Testing', 'SIEM', 'Vulnerability Assessment', 'Cloud Security', 'Python', 'Networking']
    }
    
    @staticmethod
    def generate_mock_jobs(count: int = 50, role_filter: Optional[str] = None) -> List[Dict]:
        """
        Generate mock job postings
        Args:
            count: Number of jobs to generate
            role_filter: Optional role filter (software_engineer, data_science, etc.)
        Returns:
            List of job dictionaries
        """
        jobs = []
        
        # Determine which roles to generate
        if role_filter and role_filter in JobScraper.JOB_TITLES:
            role_types = [role_filter]
        else:
            role_types = list(JobScraper.JOB_TITLES.keys())
        
        for i in range(count):
            role_type = random.choice(role_types)
            company = random.choice(JobScraper.COMPANIES)
            title = random.choice(JobScraper.JOB_TITLES[role_type])
            location = random.choice(JobScraper.LOCATIONS)
            
            # Generate realistic job data
            job = {
                'title': title,
                'company': company['name'],
                'company_logo': company['logo'],
                'location': location,
                'work_type': 'Remote' if 'Remote' in location else ('Hybrid' if 'Hybrid' in location else 'On-site'),
                'job_type': random.choice(['Full-time', 'Full-time', 'Full-time', 'Contract']),
                'experience_level': random.choice(['Entry', 'Mid', 'Senior', 'Lead']),
                'salary_min': random.randint(80, 150) * 1000,
                'salary_max': random.randint(150, 250) * 1000,
                'description': JobScraper._generate_description(title, company['name'], role_type),
                'requirements': JobScraper._generate_requirements(role_type),
                'responsibilities': JobScraper._generate_responsibilities(role_type),
                'skills_required': random.sample(JobScraper.SKILLS_BY_ROLE[role_type], k=min(6, len(JobScraper.SKILLS_BY_ROLE[role_type]))),
                'benefits': [
                    'Health insurance',
                    '401(k) matching',
                    'Flexible PTO',
                    'Remote work options',
                    'Professional development budget',
                    'Stock options'
                ],
                'source': 'LinkedIn',
                'source_url': f'https://linkedin.com/jobs/{random.randint(1000000, 9999999)}',
                'posted_date': datetime.utcnow() - timedelta(days=random.randint(0, 30)),
                'application_deadline': datetime.utcnow() + timedelta(days=random.randint(14, 60)),
                'is_active': True
            }
            
            jobs.append(job)
        
        return jobs
    
    @staticmethod
    def _generate_description(title: str, company: str, role_type: str) -> str:
        """Generate realistic job description"""
        descriptions = {
            'software_engineer': f"""
{company} is seeking a talented {title} to join our growing engineering team. You will work on building scalable systems that serve millions of users worldwide.

We're looking for someone passionate about clean code, system design, and delivering high-quality software. You'll collaborate with cross-functional teams to ship features that make a real impact.

This is an excellent opportunity to work with cutting-edge technologies and grow your skills in a supportive, innovative environment.
            """,
            'data_science': f"""
Join {company} as a {title} and help us leverage data to drive business decisions. You'll build machine learning models, analyze complex datasets, and create insights that shape product strategy.

We're looking for someone with strong analytical skills and a passion for solving challenging problems with data. You'll work with large-scale datasets and state-of-the-art ML tools.

This role offers the opportunity to work on impactful projects and collaborate with talented data scientists and engineers.
            """,
            'product': f"""
{company} is looking for an experienced {title} to lead product initiatives and drive strategy. You'll work closely with engineering, design, and business teams to build products users love.

We need someone who can balance user needs with business goals, make data-driven decisions, and communicate effectively with stakeholders at all levels.

This is a high-impact role where you'll shape the future of our products and mentor junior team members.
            """,
            'devops': f"""
As a {title} at {company}, you'll build and maintain the infrastructure that powers our services. You'll work on automation, monitoring, and ensuring our systems are reliable and scalable.

We're looking for someone with strong technical skills and a passion for improving developer productivity. You'll implement CI/CD pipelines, manage cloud infrastructure, and respond to incidents.

This role offers the opportunity to work with modern DevOps tools and practices in a fast-paced environment.
            """,
            'security': f"""
{company} is hiring a {title} to help protect our systems and data. You'll identify vulnerabilities, implement security controls, and ensure we follow best practices.

We need someone with deep security knowledge and the ability to think like an attacker. You'll conduct security assessments, respond to incidents, and work with teams across the company.

This is a critical role where you'll help keep our users' data safe and secure.
            """
        }
        
        return descriptions.get(role_type, f"Join {company} as a {title}.").strip()
    
    @staticmethod
    def _generate_requirements(role_type: str) -> List[str]:
        """Generate job requirements"""
        requirements = {
            'software_engineer': [
                '3+ years of software development experience',
                'Strong programming skills in Python, Java, or JavaScript',
                'Experience with web frameworks and APIs',
                'Understanding of data structures and algorithms',
                'Experience with Git and version control',
                'Bachelor\'s degree in Computer Science or related field'
            ],
            'data_science': [
                '2+ years of data science or ML experience',
                'Strong programming skills in Python or R',
                'Experience with ML frameworks (TensorFlow, PyTorch, scikit-learn)',
                'Solid understanding of statistics and probability',
                'Experience with SQL and data manipulation',
                'Master\'s degree in Computer Science, Statistics, or related field'
            ],
            'product': [
                '4+ years of product management experience',
                'Track record of shipping successful products',
                'Strong analytical and problem-solving skills',
                'Excellent communication and stakeholder management',
                'Experience with Agile methodologies',
                'Bachelor\'s degree in relevant field'
            ],
            'devops': [
                '3+ years of DevOps or SRE experience',
                'Strong knowledge of cloud platforms (AWS, Azure, or GCP)',
                'Experience with containerization (Docker, Kubernetes)',
                'Proficiency in scripting (Python, Bash, or Go)',
                'Understanding of CI/CD pipelines and automation',
                'Experience with monitoring and logging tools'
            ],
            'security': [
                '3+ years of security engineering experience',
                'Strong understanding of security principles and best practices',
                'Experience with security tools and frameworks',
                'Knowledge of common vulnerabilities (OWASP Top 10)',
                'Experience with penetration testing or security assessments',
                'Relevant security certifications preferred (CISSP, CEH, etc.)'
            ]
        }
        
        return requirements.get(role_type, ['Experience in relevant field', 'Strong technical skills'])
    
    @staticmethod
    def _generate_responsibilities(role_type: str) -> List[str]:
        """Generate job responsibilities"""
        responsibilities = {
            'software_engineer': [
                'Design and implement scalable backend services',
                'Write clean, maintainable, and well-tested code',
                'Collaborate with product and design teams',
                'Participate in code reviews and technical discussions',
                'Debug and resolve production issues',
                'Contribute to technical documentation'
            ],
            'data_science': [
                'Build and deploy machine learning models',
                'Analyze complex datasets to extract insights',
                'Develop data pipelines and workflows',
                'Collaborate with engineering teams on model integration',
                'Present findings to stakeholders',
                'Stay current with latest ML research and techniques'
            ],
            'product': [
                'Define product vision and strategy',
                'Prioritize features and manage roadmap',
                'Work with design to create user-centric solutions',
                'Analyze metrics and user feedback',
                'Communicate with stakeholders and executives',
                'Lead cross-functional product initiatives'
            ],
            'devops': [
                'Manage cloud infrastructure and services',
                'Implement CI/CD pipelines and automation',
                'Monitor system performance and reliability',
                'Respond to incidents and outages',
                'Optimize infrastructure costs and performance',
                'Collaborate with development teams'
            ],
            'security': [
                'Conduct security assessments and penetration tests',
                'Implement security controls and best practices',
                'Monitor for security threats and incidents',
                'Respond to security incidents and vulnerabilities',
                'Develop security policies and procedures',
                'Train teams on security awareness'
            ]
        }
        
        return responsibilities.get(role_type, ['Perform job duties as assigned'])
    
    @staticmethod
    def search_jobs(query: Optional[str] = None, 
                   location: Optional[str] = None,
                   role_type: Optional[str] = None,
                   experience_level: Optional[str] = None,
                   work_type: Optional[str] = None) -> List[Dict]:
        """
        Mock job search with filters
        Args:
            query: Search query
            location: Location filter
            role_type: Role type filter
            experience_level: Experience level filter
            work_type: Work type filter
        Returns:
            Filtered list of jobs
        """
        # Generate jobs based on role type
        jobs = JobScraper.generate_mock_jobs(count=100, role_filter=role_type)
        
        # Apply filters
        filtered_jobs = jobs
        
        if query:
            query_lower = query.lower()
            filtered_jobs = [
                job for job in filtered_jobs
                if query_lower in job['title'].lower() or 
                   query_lower in job['description'].lower() or
                   any(query_lower in skill.lower() for skill in job['skills_required'])
            ]
        
        if location and location.lower() != 'any':
            filtered_jobs = [
                job for job in filtered_jobs
                if location.lower() in job['location'].lower()
            ]
        
        if experience_level:
            filtered_jobs = [
                job for job in filtered_jobs
                if job['experience_level'] == experience_level
            ]
        
        if work_type:
            filtered_jobs = [
                job for job in filtered_jobs
                if job['work_type'] == work_type
            ]
        
        return filtered_jobs
