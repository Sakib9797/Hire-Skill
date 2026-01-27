"""
Career paths dataset with required skills and descriptions
This serves as our pretrained knowledge base for career recommendations
"""

CAREER_PATHS = [
    {
        'role': 'Full Stack Developer',
        'category': 'Software Development',
        'required_skills': [
            'JavaScript', 'React', 'Node.js', 'Python', 'Flask', 'Express',
            'MongoDB', 'PostgreSQL', 'REST API', 'Git', 'HTML', 'CSS',
            'TypeScript', 'Redux', 'Docker'
        ],
        'optional_skills': ['AWS', 'GraphQL', 'Kubernetes', 'CI/CD', 'Testing'],
        'description': 'Develops both frontend and backend of web applications',
        'average_salary': '$85,000 - $130,000',
        'growth_rate': 'High'
    },
    {
        'role': 'Frontend Developer',
        'category': 'Software Development',
        'required_skills': [
            'JavaScript', 'React', 'HTML', 'CSS', 'TypeScript',
            'Redux', 'Webpack', 'Git', 'REST API', 'Responsive Design'
        ],
        'optional_skills': ['Vue.js', 'Angular', 'Next.js', 'SASS', 'Testing'],
        'description': 'Creates user interfaces and client-side functionality',
        'average_salary': '$70,000 - $120,000',
        'growth_rate': 'High'
    },
    {
        'role': 'Backend Developer',
        'category': 'Software Development',
        'required_skills': [
            'Python', 'Java', 'Node.js', 'SQL', 'PostgreSQL', 'MongoDB',
            'REST API', 'GraphQL', 'Git', 'Docker', 'Microservices'
        ],
        'optional_skills': ['Kubernetes', 'AWS', 'Redis', 'RabbitMQ', 'gRPC'],
        'description': 'Builds server-side logic and database architecture',
        'average_salary': '$80,000 - $140,000',
        'growth_rate': 'High'
    },
    {
        'role': 'Data Scientist',
        'category': 'Data Science',
        'required_skills': [
            'Python', 'Machine Learning', 'Statistics', 'Pandas', 'NumPy',
            'Scikit-learn', 'TensorFlow', 'SQL', 'Data Visualization',
            'Jupyter', 'Mathematics'
        ],
        'optional_skills': ['PyTorch', 'Deep Learning', 'NLP', 'Big Data', 'Spark'],
        'description': 'Analyzes data and builds predictive models',
        'average_salary': '$95,000 - $150,000',
        'growth_rate': 'Very High'
    },
    {
        'role': 'Machine Learning Engineer',
        'category': 'AI/ML',
        'required_skills': [
            'Python', 'Machine Learning', 'Deep Learning', 'TensorFlow',
            'PyTorch', 'Scikit-learn', 'Docker', 'Kubernetes', 'MLOps',
            'Statistics', 'Linear Algebra'
        ],
        'optional_skills': ['NLP', 'Computer Vision', 'AWS SageMaker', 'Azure ML'],
        'description': 'Deploys and maintains ML models in production',
        'average_salary': '$110,000 - $170,000',
        'growth_rate': 'Very High'
    },
    {
        'role': 'DevOps Engineer',
        'category': 'Infrastructure',
        'required_skills': [
            'Docker', 'Kubernetes', 'AWS', 'CI/CD', 'Jenkins', 'Git',
            'Linux', 'Bash', 'Python', 'Terraform', 'Monitoring'
        ],
        'optional_skills': ['Azure', 'GCP', 'Ansible', 'Prometheus', 'Grafana'],
        'description': 'Manages infrastructure and deployment pipelines',
        'average_salary': '$90,000 - $145,000',
        'growth_rate': 'High'
    },
    {
        'role': 'Mobile Developer',
        'category': 'Mobile Development',
        'required_skills': [
            'React Native', 'Swift', 'Kotlin', 'Java', 'JavaScript',
            'iOS', 'Android', 'REST API', 'Git', 'Mobile UI/UX'
        ],
        'optional_skills': ['Flutter', 'Firebase', 'Redux', 'GraphQL'],
        'description': 'Creates mobile applications for iOS and Android',
        'average_salary': '$75,000 - $130,000',
        'growth_rate': 'High'
    },
    {
        'role': 'Cloud Architect',
        'category': 'Cloud Computing',
        'required_skills': [
            'AWS', 'Azure', 'GCP', 'Cloud Security', 'Microservices',
            'Docker', 'Kubernetes', 'Networking', 'Serverless', 'IAM'
        ],
        'optional_skills': ['Terraform', 'CloudFormation', 'Cost Optimization'],
        'description': 'Designs and implements cloud infrastructure solutions',
        'average_salary': '$120,000 - $180,000',
        'growth_rate': 'Very High'
    },
    {
        'role': 'Data Engineer',
        'category': 'Data Engineering',
        'required_skills': [
            'Python', 'SQL', 'ETL', 'Apache Spark', 'Airflow', 'Kafka',
            'Data Warehousing', 'PostgreSQL', 'MongoDB', 'AWS', 'Big Data'
        ],
        'optional_skills': ['Snowflake', 'Redshift', 'dbt', 'Docker'],
        'description': 'Builds and maintains data pipelines and infrastructure',
        'average_salary': '$100,000 - $155,000',
        'growth_rate': 'Very High'
    },
    {
        'role': 'Cybersecurity Analyst',
        'category': 'Security',
        'required_skills': [
            'Network Security', 'Penetration Testing', 'Encryption',
            'Firewalls', 'SIEM', 'Incident Response', 'Linux', 'Python',
            'Security Protocols', 'Risk Assessment'
        ],
        'optional_skills': ['CISSP', 'CEH', 'Malware Analysis', 'Cloud Security'],
        'description': 'Protects systems and networks from cyber threats',
        'average_salary': '$85,000 - $140,000',
        'growth_rate': 'Very High'
    },
    {
        'role': 'UI/UX Designer',
        'category': 'Design',
        'required_skills': [
            'Figma', 'Adobe XD', 'Sketch', 'User Research', 'Wireframing',
            'Prototyping', 'HTML', 'CSS', 'Design Systems', 'Usability Testing'
        ],
        'optional_skills': ['JavaScript', 'Animation', 'Illustration', 'Branding'],
        'description': 'Designs user interfaces and experiences',
        'average_salary': '$65,000 - $115,000',
        'growth_rate': 'Medium'
    },
    {
        'role': 'Product Manager',
        'category': 'Product Management',
        'required_skills': [
            'Product Strategy', 'Agile', 'Roadmapping', 'User Research',
            'Data Analysis', 'Stakeholder Management', 'Communication',
            'Market Research', 'MVP Development', 'SQL'
        ],
        'optional_skills': ['Python', 'Jira', 'Analytics Tools', 'A/B Testing'],
        'description': 'Defines product vision and manages development lifecycle',
        'average_salary': '$95,000 - $155,000',
        'growth_rate': 'High'
    },
    {
        'role': 'QA Engineer',
        'category': 'Quality Assurance',
        'required_skills': [
            'Testing', 'Selenium', 'Jest', 'Cypress', 'Test Automation',
            'Manual Testing', 'Bug Tracking', 'Git', 'CI/CD', 'API Testing'
        ],
        'optional_skills': ['Python', 'Java', 'Performance Testing', 'Security Testing'],
        'description': 'Ensures software quality through testing',
        'average_salary': '$60,000 - $105,000',
        'growth_rate': 'Medium'
    },
    {
        'role': 'Blockchain Developer',
        'category': 'Blockchain',
        'required_skills': [
            'Solidity', 'Ethereum', 'Smart Contracts', 'Web3', 'Cryptography',
            'JavaScript', 'Node.js', 'Blockchain Architecture', 'Git'
        ],
        'optional_skills': ['Rust', 'Hyperledger', 'DeFi', 'NFTs', 'Hardhat'],
        'description': 'Develops decentralized applications and smart contracts',
        'average_salary': '$100,000 - $180,000',
        'growth_rate': 'Very High'
    },
    {
        'role': 'Business Analyst',
        'category': 'Business',
        'required_skills': [
            'Data Analysis', 'SQL', 'Excel', 'Requirements Gathering',
            'Process Modeling', 'Stakeholder Management', 'Documentation',
            'Agile', 'Business Intelligence', 'Communication'
        ],
        'optional_skills': ['Python', 'Tableau', 'Power BI', 'JIRA'],
        'description': 'Bridges gap between business needs and technical solutions',
        'average_salary': '$70,000 - $120,000',
        'growth_rate': 'Medium'
    }
]

# All unique skills across all careers
ALL_SKILLS = sorted(list(set(
    skill 
    for career in CAREER_PATHS 
    for skill in career['required_skills'] + career['optional_skills']
)))
