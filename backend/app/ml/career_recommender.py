"""
AI-based Career Path Recommendation System
Uses scikit-learn for similarity-based recommendations with feature extraction
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple
from .career_data import CAREER_PATHS, ALL_SKILLS


class CareerRecommender:
    """ML-based career path recommender using TF-IDF and cosine similarity"""
    
    def __init__(self):
        self.career_paths = CAREER_PATHS
        self.all_skills = ALL_SKILLS
        self.vectorizer = None
        self.career_vectors = None
        self._train_model()
    
    def _train_model(self):
        """
        Train the recommendation model using TF-IDF vectorization
        Converts career skills into numerical feature vectors
        """
        # Create text representation of each career (skills as documents)
        career_documents = []
        for career in self.career_paths:
            # Combine required and optional skills into a single document
            skills_text = ' '.join(career['required_skills'] + career['optional_skills'])
            career_documents.append(skills_text)
        
        # Initialize and fit TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            token_pattern=r'(?u)\b[\w/+-]+\b',  # Handle skills like "CI/CD", "C++"
            min_df=1
        )
        
        # Create feature vectors for all careers
        self.career_vectors = self.vectorizer.fit_transform(career_documents)
    
    def extract_user_features(self, user_profile: Dict) -> np.ndarray:
        """
        Extract features from user profile
        Args:
            user_profile: Dictionary containing user skills, interests, experience
        Returns:
            Feature vector representing user's skills
        """
        # Extract skills from user profile
        user_skills = user_profile.get('skills', [])
        user_interests = user_profile.get('interests', [])
        
        # Combine skills and interests
        user_text = ' '.join(user_skills + user_interests)
        
        # Transform to feature vector using trained vectorizer
        if user_text.strip():
            user_vector = self.vectorizer.transform([user_text])
            return user_vector
        else:
            # Return zero vector if no skills
            return np.zeros((1, len(self.vectorizer.get_feature_names_out())))
    
    def calculate_skill_match(self, user_skills: List[str], career_skills: List[str]) -> float:
        """Calculate percentage of required skills the user has"""
        if not career_skills:
            return 0.0
        
        user_skills_lower = [s.lower() for s in user_skills]
        career_skills_lower = [s.lower() for s in career_skills]
        
        matched = sum(1 for skill in career_skills_lower if skill in user_skills_lower)
        return (matched / len(career_skills_lower)) * 100
    
    def identify_skill_gaps(self, user_skills: List[str], career: Dict) -> Dict:
        """
        Identify missing skills for a career path
        Args:
            user_skills: List of user's current skills
            career: Career path dictionary
        Returns:
            Dictionary with missing required and optional skills
        """
        user_skills_lower = set(s.lower() for s in user_skills)
        required_skills_lower = set(s.lower() for s in career['required_skills'])
        optional_skills_lower = set(s.lower() for s in career['optional_skills'])
        
        # Find missing skills (preserve original casing)
        missing_required = [
            skill for skill in career['required_skills']
            if skill.lower() not in user_skills_lower
        ]
        
        missing_optional = [
            skill for skill in career['optional_skills']
            if skill.lower() not in user_skills_lower
        ]
        
        # Find matching skills
        matched_required = [
            skill for skill in career['required_skills']
            if skill.lower() in user_skills_lower
        ]
        
        matched_optional = [
            skill for skill in career['optional_skills']
            if skill.lower() in user_skills_lower
        ]
        
        return {
            'missing_required': missing_required,
            'missing_optional': missing_optional,
            'matched_required': matched_required,
            'matched_optional': matched_optional,
            'required_match_percentage': len(matched_required) / len(career['required_skills']) * 100 if career['required_skills'] else 0,
            'total_match_percentage': (len(matched_required) + len(matched_optional)) / (len(career['required_skills']) + len(career['optional_skills'])) * 100 if (career['required_skills'] or career['optional_skills']) else 0
        }
    
    def recommend_careers(
        self, 
        user_profile: Dict, 
        top_n: int = 5,
        min_similarity: float = 0.0
    ) -> List[Dict]:
        """
        Recommend career paths based on user profile
        Args:
            user_profile: User profile dictionary with skills and interests
            top_n: Number of top recommendations to return
            min_similarity: Minimum similarity score threshold
        Returns:
            List of recommended career paths with scores and reasoning
        """
        # Extract user features
        user_vector = self.extract_user_features(user_profile)
        
        # Calculate cosine similarity between user and all careers
        similarities = cosine_similarity(user_vector, self.career_vectors)[0]
        
        # Get user skills for skill gap analysis
        user_skills = user_profile.get('skills', [])
        
        # Create recommendations with detailed analysis
        recommendations = []
        for idx, similarity_score in enumerate(similarities):
            if similarity_score >= min_similarity:
                career = self.career_paths[idx].copy()
                
                # Calculate skill match percentage
                skill_match = self.calculate_skill_match(
                    user_skills,
                    career['required_skills']
                )
                
                # Identify skill gaps
                skill_gaps = self.identify_skill_gaps(user_skills, career)
                
                # Generate reasoning
                reasoning = self._generate_reasoning(
                    career,
                    skill_match,
                    skill_gaps,
                    similarity_score
                )
                
                recommendations.append({
                    'role': career['role'],
                    'category': career['category'],
                    'similarity_score': round(float(similarity_score * 100), 2),
                    'skill_match_percentage': round(skill_match, 2),
                    'description': career['description'],
                    'average_salary': career['average_salary'],
                    'growth_rate': career['growth_rate'],
                    'required_skills': career['required_skills'],
                    'optional_skills': career['optional_skills'],
                    'skill_gaps': skill_gaps,
                    'reasoning': reasoning
                })
        
        # Sort by similarity score (primary) and skill match (secondary)
        recommendations.sort(
            key=lambda x: (x['similarity_score'], x['skill_match_percentage']),
            reverse=True
        )
        
        return recommendations[:top_n]
    
    def _generate_reasoning(
        self,
        career: Dict,
        skill_match: float,
        skill_gaps: Dict,
        similarity_score: float
    ) -> str:
        """Generate human-readable reasoning for recommendation"""
        reasons = []
        
        # Overall fit
        if similarity_score > 0.7:
            reasons.append(f"Excellent fit based on your skills and interests")
        elif similarity_score > 0.5:
            reasons.append(f"Good match for your profile")
        elif similarity_score > 0.3:
            reasons.append(f"Potential career path with some skill development")
        else:
            reasons.append(f"Emerging opportunity requiring skill building")
        
        # Required skills match
        matched_count = len(skill_gaps['matched_required'])
        total_required = len(career['required_skills'])
        
        if matched_count > 0:
            reasons.append(
                f"You already have {matched_count} out of {total_required} required skills "
                f"({skill_gaps['required_match_percentage']:.0f}%)"
            )
        
        # Skill gaps
        if skill_gaps['missing_required']:
            gap_count = len(skill_gaps['missing_required'])
            if gap_count <= 3:
                reasons.append(
                    f"Focus on learning: {', '.join(skill_gaps['missing_required'][:3])}"
                )
            else:
                reasons.append(
                    f"Need to develop {gap_count} key skills including: "
                    f"{', '.join(skill_gaps['missing_required'][:3])}"
                )
        else:
            reasons.append("You meet all required skill criteria!")
        
        # Growth potential
        if career['growth_rate'] == 'Very High':
            reasons.append("High demand career with excellent growth prospects")
        elif career['growth_rate'] == 'High':
            reasons.append("Strong job market demand")
        
        return '. '.join(reasons) + '.'
    
    def get_skill_recommendations(self, user_skills: List[str], target_career: str) -> Dict:
        """
        Get specific skill recommendations for a target career
        Args:
            user_skills: User's current skills
            target_career: Target career role name
        Returns:
            Detailed skill gap analysis and learning path
        """
        # Find the target career
        career = next(
            (c for c in self.career_paths if c['role'].lower() == target_career.lower()),
            None
        )
        
        if not career:
            return {
                'error': f"Career '{target_career}' not found",
                'available_careers': [c['role'] for c in self.career_paths]
            }
        
        # Get skill gaps
        skill_gaps = self.identify_skill_gaps(user_skills, career)
        
        # Prioritize missing required skills
        learning_path = []
        
        # Phase 1: Critical required skills
        if skill_gaps['missing_required']:
            learning_path.append({
                'phase': 'Phase 1: Essential Skills',
                'priority': 'High',
                'skills': skill_gaps['missing_required'][:5],  # Top 5 most important
                'timeline': '3-6 months'
            })
        
        # Phase 2: Remaining required skills
        if len(skill_gaps['missing_required']) > 5:
            learning_path.append({
                'phase': 'Phase 2: Core Competencies',
                'priority': 'Medium',
                'skills': skill_gaps['missing_required'][5:],
                'timeline': '6-12 months'
            })
        
        # Phase 3: Optional skills
        if skill_gaps['missing_optional']:
            learning_path.append({
                'phase': 'Phase 3: Advanced Skills',
                'priority': 'Low',
                'skills': skill_gaps['missing_optional'][:5],
                'timeline': '12+ months'
            })
        
        return {
            'career': career['role'],
            'category': career['category'],
            'current_match': f"{skill_gaps['required_match_percentage']:.1f}%",
            'skills_you_have': skill_gaps['matched_required'] + skill_gaps['matched_optional'],
            'skills_needed': skill_gaps['missing_required'],
            'bonus_skills': skill_gaps['missing_optional'],
            'learning_path': learning_path,
            'estimated_time_to_ready': self._estimate_readiness_time(skill_gaps)
        }
    
    def _estimate_readiness_time(self, skill_gaps: Dict) -> str:
        """Estimate time needed to become job-ready"""
        missing_required = len(skill_gaps['missing_required'])
        
        if missing_required == 0:
            return "You're ready now!"
        elif missing_required <= 3:
            return "3-6 months with focused learning"
        elif missing_required <= 7:
            return "6-12 months of dedicated study"
        else:
            return "12-18 months to build strong foundation"


# Singleton instance
_recommender_instance = None

def get_recommender() -> CareerRecommender:
    """Get or create singleton recommender instance"""
    global _recommender_instance
    if _recommender_instance is None:
        _recommender_instance = CareerRecommender()
    return _recommender_instance
