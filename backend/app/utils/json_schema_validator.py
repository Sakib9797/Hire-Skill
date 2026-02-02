"""
JSON Schema Validator for ATS Resume
Validates resume JSON against strict ATS-compliant schema
"""

import json
from typing import Dict, Tuple, List, Any


class JSONSchemaValidator:
    """Validate ATS resume JSON schema"""
    
    # Strict ATS-compliant resume schema
    ATS_RESUME_SCHEMA = {
        "type": "object",
        "required": ["personal_info", "summary", "skills", "work_experience", "education"],
        "properties": {
            "personal_info": {
                "type": "object",
                "required": ["full_name", "email"],
                "properties": {
                    "full_name": {"type": "string", "minLength": 1},
                    "email": {"type": "string", "pattern": r"^[^\s@]+@[^\s@]+\.[^\s@]+$"},
                    "phone": {"type": "string"},
                    "location": {"type": "string"},
                    "linkedin": {"type": "string"},
                    "github": {"type": "string"},
                    "portfolio": {"type": "string"}
                }
            },
            "summary": {
                "type": "string",
                "minLength": 50,
                "maxLength": 500
            },
            "skills": {
                "type": "object",
                "properties": {
                    "technical": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "soft": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "tools": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                }
            },
            "work_experience": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["title", "company", "duration", "responsibilities"],
                    "properties": {
                        "title": {"type": "string"},
                        "company": {"type": "string"},
                        "location": {"type": "string"},
                        "duration": {"type": "string"},
                        "responsibilities": {
                            "type": "array",
                            "items": {"type": "string"},
                            "minItems": 2
                        }
                    }
                }
            },
            "projects": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["name", "description", "technologies"],
                    "properties": {
                        "name": {"type": "string"},
                        "description": {"type": "string"},
                        "technologies": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "link": {"type": "string"}
                    }
                }
            },
            "education": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["degree", "institution", "year"],
                    "properties": {
                        "degree": {"type": "string"},
                        "institution": {"type": "string"},
                        "location": {"type": "string"},
                        "year": {"type": "string"},
                        "gpa": {"type": "string"}
                    }
                },
                "minItems": 1
            },
            "certifications": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["name", "issuer"],
                    "properties": {
                        "name": {"type": "string"},
                        "issuer": {"type": "string"},
                        "year": {"type": "string"},
                        "credential_id": {"type": "string"}
                    }
                }
            }
        }
    }
    
    @staticmethod
    def validate_resume(resume_data: Dict) -> Tuple[bool, List[str]]:
        """
        Validate resume data against ATS schema
        
        Args:
            resume_data: Resume data to validate
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        try:
            # Validate required root fields
            if not isinstance(resume_data, dict):
                return False, ["Resume data must be a dictionary/object"]
            
            # Check required fields
            required_fields = ["personal_info", "summary", "skills", "work_experience", "education"]
            for field in required_fields:
                if field not in resume_data:
                    errors.append(f"Missing required field: {field}")
            
            if errors:
                return False, errors
            
            # Validate personal_info
            personal_errors = JSONSchemaValidator._validate_personal_info(resume_data.get("personal_info", {}))
            errors.extend(personal_errors)
            
            # Validate summary
            summary_errors = JSONSchemaValidator._validate_summary(resume_data.get("summary", ""))
            errors.extend(summary_errors)
            
            # Validate skills
            skills_errors = JSONSchemaValidator._validate_skills(resume_data.get("skills", {}))
            errors.extend(skills_errors)
            
            # Validate work_experience
            work_errors = JSONSchemaValidator._validate_work_experience(resume_data.get("work_experience", []))
            errors.extend(work_errors)
            
            # Validate education
            edu_errors = JSONSchemaValidator._validate_education(resume_data.get("education", []))
            errors.extend(edu_errors)
            
            # Validate optional fields
            if "projects" in resume_data:
                project_errors = JSONSchemaValidator._validate_projects(resume_data["projects"])
                errors.extend(project_errors)
            
            if "certifications" in resume_data:
                cert_errors = JSONSchemaValidator._validate_certifications(resume_data["certifications"])
                errors.extend(cert_errors)
            
            # Check for ATS-unfriendly content
            ats_errors = JSONSchemaValidator._check_ats_compliance(resume_data)
            errors.extend(ats_errors)
            
            return len(errors) == 0, errors
            
        except Exception as e:
            return False, [f"Validation error: {str(e)}"]
    
    @staticmethod
    def _validate_personal_info(personal_info: Dict) -> List[str]:
        """Validate personal info section"""
        errors = []
        
        if not isinstance(personal_info, dict):
            return ["personal_info must be an object"]
        
        # Required fields
        if not personal_info.get("full_name"):
            errors.append("personal_info.full_name is required")
        
        if not personal_info.get("email"):
            errors.append("personal_info.email is required")
        elif "@" not in personal_info["email"]:
            errors.append("personal_info.email must be a valid email address")
        
        return errors
    
    @staticmethod
    def _validate_summary(summary: str) -> List[str]:
        """Validate summary section"""
        errors = []
        
        if not isinstance(summary, str):
            return ["summary must be a string"]
        
        if len(summary) < 50:
            errors.append("summary must be at least 50 characters")
        
        if len(summary) > 500:
            errors.append("summary should not exceed 500 characters")
        
        return errors
    
    @staticmethod
    def _validate_skills(skills: Dict) -> List[str]:
        """Validate skills section"""
        errors = []
        
        if not isinstance(skills, dict):
            return ["skills must be an object"]
        
        # At least one skill category should have items
        has_skills = False
        for category in ["technical", "soft", "tools"]:
            if category in skills and isinstance(skills[category], list) and len(skills[category]) > 0:
                has_skills = True
                break
        
        if not has_skills:
            errors.append("skills must contain at least one category (technical, soft, or tools) with items")
        
        # Validate arrays
        for category in ["technical", "soft", "tools"]:
            if category in skills and not isinstance(skills[category], list):
                errors.append(f"skills.{category} must be an array")
        
        return errors
    
    @staticmethod
    def _validate_work_experience(work_experience: List) -> List[str]:
        """Validate work experience section"""
        errors = []
        
        if not isinstance(work_experience, list):
            return ["work_experience must be an array"]
        
        for i, exp in enumerate(work_experience):
            if not isinstance(exp, dict):
                errors.append(f"work_experience[{i}] must be an object")
                continue
            
            # Required fields
            required = ["title", "company", "duration", "responsibilities"]
            for field in required:
                if field not in exp or not exp[field]:
                    errors.append(f"work_experience[{i}].{field} is required")
            
            # Validate responsibilities
            if "responsibilities" in exp:
                if not isinstance(exp["responsibilities"], list):
                    errors.append(f"work_experience[{i}].responsibilities must be an array")
                elif len(exp["responsibilities"]) < 2:
                    errors.append(f"work_experience[{i}].responsibilities must have at least 2 items")
        
        return errors
    
    @staticmethod
    def _validate_projects(projects: List) -> List[str]:
        """Validate projects section"""
        errors = []
        
        if not isinstance(projects, list):
            return ["projects must be an array"]
        
        for i, project in enumerate(projects):
            if not isinstance(project, dict):
                errors.append(f"projects[{i}] must be an object")
                continue
            
            required = ["name", "description", "technologies"]
            for field in required:
                if field not in project or not project[field]:
                    errors.append(f"projects[{i}].{field} is required")
            
            if "technologies" in project and not isinstance(project["technologies"], list):
                errors.append(f"projects[{i}].technologies must be an array")
        
        return errors
    
    @staticmethod
    def _validate_education(education: List) -> List[str]:
        """Validate education section"""
        errors = []
        
        if not isinstance(education, list):
            return ["education must be an array"]
        
        if len(education) == 0:
            errors.append("education must have at least one entry")
            return errors
        
        for i, edu in enumerate(education):
            if not isinstance(edu, dict):
                errors.append(f"education[{i}] must be an object")
                continue
            
            required = ["degree", "institution", "year"]
            for field in required:
                if field not in edu or not edu[field]:
                    errors.append(f"education[{i}].{field} is required")
        
        return errors
    
    @staticmethod
    def _validate_certifications(certifications: List) -> List[str]:
        """Validate certifications section"""
        errors = []
        
        if not isinstance(certifications, list):
            return ["certifications must be an array"]
        
        for i, cert in enumerate(certifications):
            if not isinstance(cert, dict):
                errors.append(f"certifications[{i}] must be an object")
                continue
            
            required = ["name", "issuer"]
            for field in required:
                if field not in cert or not cert[field]:
                    errors.append(f"certifications[{i}].{field} is required")
        
        return errors
    
    @staticmethod
    def _check_ats_compliance(resume_data: Dict) -> List[str]:
        """Check for ATS-unfriendly content"""
        warnings = []
        
        # Check for emojis or special characters
        text_content = json.dumps(resume_data)
        if any(ord(char) > 127 for char in text_content if char not in ['\n', '\t']):
            warnings.append("ATS Warning: Resume contains special characters or emojis that may not be ATS-friendly")
        
        # Check summary length (should be concise)
        summary = resume_data.get("summary", "")
        word_count = len(summary.split())
        if word_count < 20:
            warnings.append("ATS Warning: Summary is too short (should be 20-100 words)")
        elif word_count > 100:
            warnings.append("ATS Warning: Summary is too long (should be 20-100 words)")
        
        return warnings
    
    @staticmethod
    def validate_and_sanitize(resume_data: Dict) -> Tuple[bool, Dict, List[str]]:
        """
        Validate and sanitize resume data
        
        Returns:
            Tuple of (is_valid, sanitized_data, errors)
        """
        # First validate
        is_valid, errors = JSONSchemaValidator.validate_resume(resume_data)
        
        # Sanitize data
        sanitized = JSONSchemaValidator._sanitize_resume(resume_data)
        
        return is_valid, sanitized, errors
    
    @staticmethod
    def _sanitize_resume(resume_data: Dict) -> Dict:
        """Remove ATS-unfriendly content and sanitize data"""
        sanitized = json.loads(json.dumps(resume_data))  # Deep copy
        
        # Remove emojis and special characters
        def clean_string(s: str) -> str:
            if not isinstance(s, str):
                return s
            # Remove emojis and non-ASCII characters
            return ''.join(char for char in s if ord(char) < 128 or char in ['\n', '\t'])
        
        def clean_dict(obj: Any) -> Any:
            """Recursively clean dictionary"""
            if isinstance(obj, dict):
                return {k: clean_dict(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [clean_dict(item) for item in obj]
            elif isinstance(obj, str):
                return clean_string(obj)
            else:
                return obj
        
        return clean_dict(sanitized)
