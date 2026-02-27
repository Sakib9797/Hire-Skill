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
        'growth_rate': 'High',
        'courses': [
            {'name': 'The Web Developer Bootcamp 2024', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/the-web-developer-bootcamp/', 'level': 'Beginner'},
            {'name': 'Full-Stack Web Development with React', 'platform': 'Coursera', 'url': 'https://www.coursera.org/specializations/full-stack-react', 'level': 'Intermediate'},
            {'name': 'CS50 Web Programming with Python and JavaScript', 'platform': 'edX', 'url': 'https://www.edx.org/course/cs50s-web-programming-with-python-and-javascript', 'level': 'Intermediate'},
            {'name': 'The Odin Project - Full Stack JavaScript', 'platform': 'The Odin Project', 'url': 'https://www.theodinproject.com/paths/full-stack-javascript', 'level': 'Beginner'},
            {'name': 'Meta Back-End Developer Professional Certificate', 'platform': 'Coursera', 'url': 'https://www.coursera.org/professional-certificates/meta-back-end-developer', 'level': 'Intermediate'},
            {'name': 'Docker & Kubernetes: The Practical Guide', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/docker-kubernetes-the-practical-guide/', 'level': 'Intermediate'},
        ]
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
        'growth_rate': 'High',
        'courses': [
            {'name': 'React - The Complete Guide', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/react-the-complete-guide-incl-redux/', 'level': 'Beginner'},
            {'name': 'Meta Front-End Developer Professional Certificate', 'platform': 'Coursera', 'url': 'https://www.coursera.org/professional-certificates/meta-front-end-developer', 'level': 'Beginner'},
            {'name': 'JavaScript: Understanding the Weird Parts', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/understand-javascript/', 'level': 'Intermediate'},
            {'name': 'CSS for JavaScript Developers', 'platform': 'Josh W Comeau', 'url': 'https://css-for-js.dev/', 'level': 'Intermediate'},
            {'name': 'Frontend Masters - Complete Intro to React', 'platform': 'Frontend Masters', 'url': 'https://frontendmasters.com/courses/complete-react-v8/', 'level': 'Beginner'},
            {'name': 'Advanced React Patterns', 'platform': 'Frontend Masters', 'url': 'https://frontendmasters.com/courses/advanced-react-patterns/', 'level': 'Advanced'},
        ]
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
        'growth_rate': 'High',
        'courses': [
            {'name': 'Python for Everybody', 'platform': 'Coursera', 'url': 'https://www.coursera.org/specializations/python', 'level': 'Beginner'},
            {'name': 'Node.js, Express, MongoDB & More: The Complete Bootcamp', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/nodejs-express-mongodb-bootcamp/', 'level': 'Intermediate'},
            {'name': 'Designing RESTful APIs', 'platform': 'Udacity', 'url': 'https://www.udacity.com/course/designing-restful-apis--ud388', 'level': 'Intermediate'},
            {'name': 'The Complete SQL Bootcamp', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/the-complete-sql-bootcamp/', 'level': 'Beginner'},
            {'name': 'Microservices with Node JS and React', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/microservices-with-node-js-and-react/', 'level': 'Advanced'},
            {'name': 'System Design for Beginners', 'platform': 'NeetCode', 'url': 'https://neetcode.io/courses/system-design-for-beginners/0', 'level': 'Intermediate'},
        ]
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
        'growth_rate': 'Very High',
        'courses': [
            {'name': 'IBM Data Science Professional Certificate', 'platform': 'Coursera', 'url': 'https://www.coursera.org/professional-certificates/ibm-data-science', 'level': 'Beginner'},
            {'name': 'Machine Learning Specialization', 'platform': 'Coursera', 'url': 'https://www.coursera.org/specializations/machine-learning-introduction', 'level': 'Intermediate'},
            {'name': 'Python for Data Science and Machine Learning Bootcamp', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/python-for-data-science-and-machine-learning-bootcamp/', 'level': 'Beginner'},
            {'name': 'Statistics and Probability (Khan Academy)', 'platform': 'Khan Academy', 'url': 'https://www.khanacademy.org/math/statistics-probability', 'level': 'Beginner'},
            {'name': 'Deep Learning Specialization', 'platform': 'Coursera', 'url': 'https://www.coursera.org/specializations/deep-learning', 'level': 'Advanced'},
            {'name': 'fast.ai Practical Deep Learning for Coders', 'platform': 'fast.ai', 'url': 'https://course.fast.ai/', 'level': 'Intermediate'},
        ]
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
        'growth_rate': 'Very High',
        'courses': [
            {'name': 'Machine Learning Engineering for Production (MLOps)', 'platform': 'Coursera', 'url': 'https://www.coursera.org/specializations/machine-learning-engineering-for-production-mlops', 'level': 'Advanced'},
            {'name': 'Deep Learning with PyTorch: Zero to GANs', 'platform': 'Jovian', 'url': 'https://jovian.ai/learn/deep-learning-with-pytorch-zero-to-gans', 'level': 'Intermediate'},
            {'name': 'Made With ML - MLOps Course', 'platform': 'Made With ML', 'url': 'https://madewithml.com/', 'level': 'Intermediate'},
            {'name': 'Full Stack Deep Learning', 'platform': 'FSDL', 'url': 'https://fullstackdeeplearning.com/', 'level': 'Advanced'},
            {'name': 'Hands-On Machine Learning (O\'Reilly)', 'platform': 'O\'Reilly', 'url': 'https://www.oreilly.com/library/view/hands-on-machine-learning/9781098125967/', 'level': 'Intermediate'},
            {'name': 'AWS Machine Learning Specialty', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/aws-machine-learning/', 'level': 'Advanced'},
        ]
    },
    {
        'role': 'AI Engineer',
        'category': 'AI/ML',
        'required_skills': [
            'Python', 'LLMs', 'Prompt Engineering', 'LangChain', 'RAG',
            'TensorFlow', 'PyTorch', 'NLP', 'Transformers', 'Vector Databases',
            'FastAPI', 'Machine Learning'
        ],
        'optional_skills': ['Fine-tuning', 'Computer Vision', 'MLOps', 'AWS Bedrock', 'OpenAI API', 'HuggingFace'],
        'description': 'Builds intelligent AI-powered applications and pipelines using large language models',
        'average_salary': '$130,000 - $200,000',
        'growth_rate': 'Very High',
        'courses': [
            {'name': 'ChatGPT Prompt Engineering for Developers', 'platform': 'DeepLearning.AI', 'url': 'https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/', 'level': 'Beginner'},
            {'name': 'LangChain for LLM Application Development', 'platform': 'DeepLearning.AI', 'url': 'https://www.deeplearning.ai/short-courses/langchain-for-llm-application-development/', 'level': 'Intermediate'},
            {'name': 'Building RAG Agents with LLMs', 'platform': 'NVIDIA DLI', 'url': 'https://www.nvidia.com/en-us/training/', 'level': 'Intermediate'},
            {'name': 'Generative AI with Large Language Models', 'platform': 'Coursera', 'url': 'https://www.coursera.org/learn/generative-ai-with-llms', 'level': 'Intermediate'},
            {'name': 'LLM University by Cohere', 'platform': 'Cohere', 'url': 'https://docs.cohere.com/docs/llmu', 'level': 'Beginner'},
            {'name': 'Hugging Face NLP Course', 'platform': 'Hugging Face', 'url': 'https://huggingface.co/learn/nlp-course', 'level': 'Intermediate'},
            {'name': 'Building AI Applications with LangChain & GPT', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/langchain/', 'level': 'Intermediate'},
            {'name': 'Stanford CS224N: NLP with Deep Learning', 'platform': 'Stanford', 'url': 'https://web.stanford.edu/class/cs224n/', 'level': 'Advanced'},
            {'name': 'Fine-Tuning Large Language Models', 'platform': 'DeepLearning.AI', 'url': 'https://www.deeplearning.ai/short-courses/finetuning-large-language-models/', 'level': 'Advanced'},
            {'name': 'Vector Databases: from Embeddings to Applications', 'platform': 'DeepLearning.AI', 'url': 'https://www.deeplearning.ai/short-courses/vector-databases-embeddings-applications/', 'level': 'Intermediate'},
        ]
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
        'growth_rate': 'High',
        'courses': [
            {'name': 'Docker and Kubernetes: The Complete Guide', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/docker-and-kubernetes-the-complete-guide/', 'level': 'Beginner'},
            {'name': 'AWS Certified Solutions Architect', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/aws-certified-solutions-architect-associate-saa-c03/', 'level': 'Intermediate'},
            {'name': 'HashiCorp Terraform Associate Certification', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/terraform-beginner-to-advanced/', 'level': 'Intermediate'},
            {'name': 'Linux Administration Bootcamp', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/linux-administration-bootcamp/', 'level': 'Beginner'},
            {'name': 'Google IT Automation with Python', 'platform': 'Coursera', 'url': 'https://www.coursera.org/professional-certificates/google-it-automation', 'level': 'Beginner'},
            {'name': 'CI/CD with Jenkins, Ansible, Docker, Kubernetes', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/valaxy-devops/', 'level': 'Advanced'},
        ]
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
        'growth_rate': 'High',
        'courses': [
            {'name': 'React Native - The Practical Guide', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/react-native-the-practical-guide/', 'level': 'Beginner'},
            {'name': 'iOS & Swift - The Complete iOS App Development Bootcamp', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/ios-13-app-development-bootcamp/', 'level': 'Beginner'},
            {'name': 'Android Development with Kotlin', 'platform': 'Coursera', 'url': 'https://www.coursera.org/specializations/android-app-development', 'level': 'Beginner'},
            {'name': 'Flutter & Dart - The Complete Guide', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/learn-flutter-dart-to-build-ios-android-apps/', 'level': 'Beginner'},
            {'name': 'Meta React Native Specialization', 'platform': 'Coursera', 'url': 'https://www.coursera.org/professional-certificates/meta-react-native', 'level': 'Intermediate'},
            {'name': 'CS193p - Developing Apps for iOS (Stanford)', 'platform': 'Stanford', 'url': 'https://cs193p.sites.stanford.edu/', 'level': 'Intermediate'},
        ]
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
        'growth_rate': 'Very High',
        'courses': [
            {'name': 'AWS Certified Solutions Architect - Professional', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/aws-solutions-architect-professional/', 'level': 'Advanced'},
            {'name': 'Google Cloud Professional Cloud Architect', 'platform': 'Coursera', 'url': 'https://www.coursera.org/professional-certificates/gcp-cloud-architect', 'level': 'Advanced'},
            {'name': 'Microsoft Azure Fundamentals AZ-900', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/az900-azure/', 'level': 'Beginner'},
            {'name': 'Cloud Computing Specialization', 'platform': 'Coursera', 'url': 'https://www.coursera.org/specializations/cloud-computing', 'level': 'Intermediate'},
            {'name': 'Kubernetes for the Absolute Beginners', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/learn-kubernetes/', 'level': 'Beginner'},
            {'name': 'AWS Serverless Applications Lens', 'platform': 'AWS Training', 'url': 'https://aws.amazon.com/training/', 'level': 'Intermediate'},
        ]
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
        'growth_rate': 'Very High',
        'courses': [
            {'name': 'Data Engineering Zoomcamp', 'platform': 'DataTalks.Club', 'url': 'https://github.com/DataTalksClub/data-engineering-zoomcamp', 'level': 'Beginner'},
            {'name': 'Apache Spark with Scala - Hands On', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/apache-spark-with-scala-hands-on-with-big-data/', 'level': 'Intermediate'},
            {'name': 'The Complete dbt Bootcamp', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/complete-dbt-data-build-tool-bootcamp-zero-to-hero/', 'level': 'Intermediate'},
            {'name': 'IBM Data Engineering Professional Certificate', 'platform': 'Coursera', 'url': 'https://www.coursera.org/professional-certificates/ibm-data-engineer', 'level': 'Beginner'},
            {'name': 'Streaming Data with Apache Kafka', 'platform': 'Confluent', 'url': 'https://developer.confluent.io/learn-kafka/', 'level': 'Intermediate'},
            {'name': 'Apache Airflow: The Hands-On Guide', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/the-complete-hands-on-course-to-master-apache-airflow/', 'level': 'Intermediate'},
        ]
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
        'growth_rate': 'Very High',
        'courses': [
            {'name': 'Google Cybersecurity Professional Certificate', 'platform': 'Coursera', 'url': 'https://www.coursera.org/professional-certificates/google-cybersecurity', 'level': 'Beginner'},
            {'name': 'CompTIA Security+ Certification', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/securityplus/', 'level': 'Beginner'},
            {'name': 'Practical Ethical Hacking', 'platform': 'TCM Security', 'url': 'https://academy.tcm-sec.com/p/practical-ethical-hacking-the-complete-course', 'level': 'Intermediate'},
            {'name': 'Introduction to Cyber Security', 'platform': 'Coursera', 'url': 'https://www.coursera.org/specializations/intro-cyber-security', 'level': 'Beginner'},
            {'name': 'Penetration Testing with Kali Linux (PEN-200)', 'platform': 'Offensive Security', 'url': 'https://www.offsec.com/courses/pen-200/', 'level': 'Advanced'},
            {'name': 'TryHackMe Complete Beginner Path', 'platform': 'TryHackMe', 'url': 'https://tryhackme.com/path/outline/beginner', 'level': 'Beginner'},
        ]
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
        'growth_rate': 'Medium',
        'courses': [
            {'name': 'Google UX Design Professional Certificate', 'platform': 'Coursera', 'url': 'https://www.coursera.org/professional-certificates/google-ux-design', 'level': 'Beginner'},
            {'name': 'UI/UX Design Specialization', 'platform': 'Coursera', 'url': 'https://www.coursera.org/specializations/ui-ux-design', 'level': 'Beginner'},
            {'name': 'Figma UI UX Design Essentials', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/figma-ux-ui-design-user-experience-tutorial-course/', 'level': 'Beginner'},
            {'name': 'Interaction Design Specialization', 'platform': 'Coursera', 'url': 'https://www.coursera.org/specializations/interaction-design', 'level': 'Intermediate'},
            {'name': 'Design for Developers', 'platform': 'Frontend Masters', 'url': 'https://frontendmasters.com/courses/design-for-developers/', 'level': 'Beginner'},
            {'name': 'UX Research and Design by University of Michigan', 'platform': 'Coursera', 'url': 'https://www.coursera.org/specializations/michiganux', 'level': 'Intermediate'},
        ]
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
        'growth_rate': 'High',
        'courses': [
            {'name': 'Digital Product Management Specialization', 'platform': 'Coursera', 'url': 'https://www.coursera.org/specializations/uva-darden-digital-product-management', 'level': 'Beginner'},
            {'name': 'Become a Product Manager', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/become-a-product-manager-learn-the-skills-get-a-job/', 'level': 'Beginner'},
            {'name': 'Product Management by Pendo', 'platform': 'Product School', 'url': 'https://productschool.com/free-product-management-resources', 'level': 'Intermediate'},
            {'name': 'Agile with Atlassian Jira', 'platform': 'Coursera', 'url': 'https://www.coursera.org/learn/agile-atlassian-jira', 'level': 'Beginner'},
            {'name': 'SQL for Data Analysis', 'platform': 'Udacity', 'url': 'https://www.udacity.com/course/sql-for-data-analysis--ud198', 'level': 'Beginner'},
            {'name': 'Product Analytics Micro-Certification', 'platform': 'Product School', 'url': 'https://productschool.com/product-analytics-certification', 'level': 'Intermediate'},
        ]
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
        'growth_rate': 'Medium',
        'courses': [
            {'name': 'ISTQB Foundation Level Certification', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/istqb-foundation-level-training/', 'level': 'Beginner'},
            {'name': 'Selenium WebDriver with Java', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/selenium-real-time-examplesi/', 'level': 'Intermediate'},
            {'name': 'Cypress End-to-End Testing', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/cypress-io-master-class/', 'level': 'Intermediate'},
            {'name': 'API Testing with Postman', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/postman-the-complete-guide/', 'level': 'Beginner'},
            {'name': 'Test Automation University', 'platform': 'Applitools', 'url': 'https://testautomationu.applitools.com/', 'level': 'Beginner'},
            {'name': 'Performance Testing with JMeter', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/learn-jmeter-from-scratch/', 'level': 'Intermediate'},
        ]
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
        'growth_rate': 'Very High',
        'courses': [
            {'name': 'Blockchain Specialization', 'platform': 'Coursera', 'url': 'https://www.coursera.org/specializations/blockchain', 'level': 'Beginner'},
            {'name': 'Ethereum and Solidity: The Complete Developer\'s Guide', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/ethereum-and-solidity-the-complete-developers-guide/', 'level': 'Intermediate'},
            {'name': 'CryptoZombies - Learn Solidity', 'platform': 'CryptoZombies', 'url': 'https://cryptozombies.io/', 'level': 'Beginner'},
            {'name': 'Blockchain A-Z: Build a Blockchain', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/build-your-blockchain-az/', 'level': 'Beginner'},
            {'name': 'Solana Blockchain Developer Bootcamp', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/solana-developer/', 'level': 'Intermediate'},
            {'name': 'Patrick Collins - Learn Blockchain, Solidity & Full Stack Web3', 'platform': 'YouTube/freeCodeCamp', 'url': 'https://www.youtube.com/watch?v=gyMwXuJrbJQ', 'level': 'Intermediate'},
        ]
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
        'growth_rate': 'Medium',
        'courses': [
            {'name': 'Google Data Analytics Professional Certificate', 'platform': 'Coursera', 'url': 'https://www.coursera.org/professional-certificates/google-data-analytics', 'level': 'Beginner'},
            {'name': 'Business Analysis Fundamentals', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/business-analysis-ba/', 'level': 'Beginner'},
            {'name': 'Tableau 2024 A-Z: Hands-On Tableau Training', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/tableau10/', 'level': 'Beginner'},
            {'name': 'Microsoft Power BI Data Analyst', 'platform': 'Coursera', 'url': 'https://www.coursera.org/professional-certificates/microsoft-power-bi-data-analyst', 'level': 'Intermediate'},
            {'name': 'Excel Skills for Business Specialization', 'platform': 'Coursera', 'url': 'https://www.coursera.org/specializations/excel', 'level': 'Beginner'},
            {'name': 'IIBA Entry Certificate in Business Analysis', 'platform': 'IIBA', 'url': 'https://www.iiba.org/business-analysis-certifications/ecba/', 'level': 'Beginner'},
        ]
    }
]

# All unique skills across all careers
ALL_SKILLS = sorted(list(set(
    skill 
    for career in CAREER_PATHS 
    for skill in career['required_skills'] + career['optional_skills']
)))
