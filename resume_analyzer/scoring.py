import logging
from typing import Dict, List, Any, Tuple

from resume_analyzer.vectorization import TextVectorizer
from resume_analyzer.extraction import InformationExtractor, extract_resume_and_job_description

from fuzzywuzzy import fuzz
import spacy

class ResumeScorer:
    def __init__(self):
        """
        Initialize the ResumeScorer with a text vectorizer.
        Supports advanced scoring across multiple dimensions.
        """
        self.degree_hierarchy = {
            'doctoral': {
                'variants': ['phd', 'doctorate', 'doctor of philosophy', 'ph.d', 'd.', 'postdoctoral'],
                'weight': 1.0
            },
            'professional': {
                'variants': ['md', 'jd', 'dds', 'dmd', 'pharmd', 'professional degree'],
                'weight': 0.95
            },
            'masters': {
                'variants': ['master', 'm.s.', 'm.sc.', 'master of science', 'ma', 'mba', 'mfa'],
                'weight': 0.85
            },
            'bachelors': {
                'variants': ['bachelor', 'b.s.', 'b.sc.', 'ba', 'bs', 'bfa', 'bba', 'undergraduate'],
                'weight': 0.7
            },
            'associate': {
                'variants': ['associate', 'a.a.', 'a.s.', 'associate degree'],
                'weight': 0.5
            },
            'certificate': {
                'variants': ['certificate', 'diploma', 'vocational', 'technical training'],
                'weight': 0.3
            }
        }

        try:
            self.nlp = spacy.load('en_core_web_sm')
        except OSError:
            self.nlp = None
        
        self.vectorizer = TextVectorizer()
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
    
    def compute_similarity(self, resume_text: str, jd_text: str) -> float:
        """
        Compute semantic similarity between resume and job description.
        
        Args:
            resume_text (str): Full text of the resume
            jd_text (str): Full text of the job description
        
        Returns:
            float: Similarity score between 0 and 1
        """
        try:
            resume_vec = self.vectorizer.get_document_embedding(resume_text, method='sbert')
            jd_vec = self.vectorizer.get_document_embedding(jd_text, method='sbert')
            return self.vectorizer.calculate_similarity(resume_vec, jd_vec)
        except Exception as e:
            self.logger.error(f"Similarity computation error: {e}")
            return 0.0
    
    def score_resume(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive resume scoring based on multiple factors.
        
        Args:
            extracted_data (Dict): Structured data from resume and job description extraction
        
        Returns:
            Dict containing various scoring metrics
        """
        resume = extracted_data['resume']
        job_description = extracted_data['job_description']
        
        # Call match_skills with additional return for matching and missing skills
        skills_match, matching_skills, missing_skills = self.match_skills(
            resume.get('skills', []), 
            job_description.get('skills', [])
        )
        
        scores = {
            'skills_match': skills_match,
            'matching_skills': matching_skills,
            'missing_skills': missing_skills,
            'experience_match': self.match_experience(
                resume.get('experience', []), 
                job_description.get('experience', [])
            ),
            'education_match': self.match_education(
                resume.get('education', []), 
                job_description.get('education', [])
            ),
            'job_title_relevance': self.match_job_title(
                resume.get('job_titles', []), 
                job_description.get('job_titles', [])
            ),
            'overall_similarity': self.match_full_text(
                resume.get('full_text', []),
                job_description.get('full_text', [])
            ),
            'resume_ner': resume.get('ner', ''),
            'job_ner': job_description.get('ner', '') 
        }
        
        # Weighted average score
        weights = {
            'skills_match': 0.6,
            'experience_match': 0.1,
            'education_match': 0.1,
            'job_title_relevance': 0.1,
            'overall_similarity': 0.1
        }
        
        scores['total_score'] = sum(
            scores.get(metric, 0) * weight 
            for metric, weight in weights.items()
        )
        
        return scores
    
    def match_skills(self, resume_skills: List[str], jd_skills: List[str]) -> Tuple[float, List[str], List[str]]:
        """
        Calculate skill match percentage with advanced matching.
        
        Args:
            resume_skills (List[str]): Skills from resume
            jd_skills (List[str]): Skills from job description
        
        Returns:
            Tuple containing:
            - Skill match percentage (0-1)
            - List of matching skills
            - List of missing skills
        """
        if not jd_skills:
            return 0.0, [], []
        
        # Normalize skills to lowercase for case-insensitive matching
        resume_skills_lower = [skill.lower() for skill in resume_skills]
        jd_skills_lower = [skill.lower() for skill in jd_skills]
        
        # Find matching and missing skills
        matching_skills = list(set(resume_skills_lower) & set(jd_skills_lower))
        missing_skills = list(set(jd_skills_lower) - set(resume_skills_lower))

        # Compute match percentage
        match_percentage = len(matching_skills) / len(jd_skills)
        
        # Bonus points for full match
        bonus = 0.2 if match_percentage == 1.0 else 0
        match_score = min(match_percentage + bonus, 1.0)
        
        # Restore original case for matching and missing skills
        matching_skills = [
            jd_skills[jd_skills_lower.index(skill)] 
            for skill in matching_skills
        ]
        missing_skills = [
            jd_skills[jd_skills_lower.index(skill)] 
            for skill in missing_skills
        ]
        
        return match_score, matching_skills, missing_skills
    
    def match_experience(self, resume_experience: List[Dict], jd_exp_requirements: List[str]) -> float:
        """
        Advanced experience matching considering various factors.
        
        Args:
            resume_experience (List[Dict]): Work experience from resume
            jd_exp_requirements (List[str]): Experience requirements from job description
        
        Returns:
            float: Experience match score (0-1)
        """
        if not jd_exp_requirements:
            return 0.0
        
        def extract_years(requirements):
            """Extract years of experience from requirements."""
            import re
            for req in requirements:
                match = re.search(r'(\d+)\+?\s*(?:years?|yrs?)', str(req), re.IGNORECASE)
                if match:
                    return int(match.group(1))
            return 0
        
        required_years = extract_years(jd_exp_requirements)
        
        # Calculate actual total experience
        total_experience_years = sum(
            self._compute_experience_duration(exp.get('dates', [])) 
            for exp in resume_experience
        )
        
        # Exponential scoring to favor meeting/exceeding requirements
        if total_experience_years >= required_years:
            return min(1.0, 1 - 1 / (1 + total_experience_years - required_years + 1))
        
        return total_experience_years / required_years
    
    def _compute_experience_duration(self, dates: List[str]) -> float:
        """
        Compute duration of work experience.
        Simple estimation based on string dates.
        
        Args:
            dates (List[str]): Date strings from experience
        
        Returns:
            float: Estimated years of experience
        """
        import re
        from datetime import datetime
        
        def parse_year(date_str):
            try:
                year_match = re.search(r'\d{4}', str(date_str))
                return int(year_match.group()) if year_match else None
            except Exception:
                return None
        
        if len(dates) >= 2:
            start_year = parse_year(dates[0])
            end_year = parse_year(dates[1]) or datetime.now().year
            
            if start_year and end_year:
                return max(0, end_year - start_year)
        
        return 0
    
    
    #* EDUCATION SECTION STARTS*#

    def _normalize_degree(self, degree: str) -> str:
        """
        Normalize degree strings to a standardized format.
        
        Args:
            degree (str): Raw degree string
        
        Returns:
            str: Normalized degree level
        """
        # Convert to lowercase and remove extra whitespaces
        degree = degree.lower().strip()
        
        # Check against known degree variants
        for level, info in self.degree_hierarchy.items():
            if any(variant in degree for variant in info['variants']):
                return level
        
        return 'unknown'

    def match_education(self, resume_education: List[str], jd_education: List[str]) -> float:
        """
        Advanced education matching using multiple strategies.
        
        Args:
            resume_education (List[str]): Education details from resume
            jd_education (List[str]): Education requirements from job description
        
        Returns:
            float: Education match score (0-1)
        """
        # Handle empty job description education requirements
        if not jd_education:
            return 0.0
        
        # Normalize degrees
        resume_degrees = [self._normalize_degree(degree) for degree in resume_education]
        jd_degrees = [self._normalize_degree(degree) for degree in jd_education]
        
        # Compute matches
        degree_matches = []
        for jd_degree in jd_degrees:
            # Find best match with semantic and hierarchical scoring
            best_match = max([
                self._compute_degree_match(resume_degree, jd_degree)
                for resume_degree in resume_degrees
            ], default=0.0)
            degree_matches.append(best_match)
        
        # Scoring strategy
        if not degree_matches:
            return 0.0
        
        # Compute weighted mean with bonus for high matches
        mean_match = sum(degree_matches) / len(jd_degrees)
        
        # Bonus for exact or near-exact matches
        if all(match >= 0.9 for match in degree_matches):
            mean_match = min(mean_match * 1.2, 1.0)
        
        return mean_match

    def _compute_degree_match(self, resume_degree: str, jd_degree: str) -> float:
        """
        Compute match score between two degrees.
        
        Args:
            resume_degree (str): Normalized resume degree
            jd_degree (str): Normalized job description degree
        
        Returns:
            float: Match score (0-1)
        """
        # Exact match
        if resume_degree == jd_degree:
            return 1.0
        
        # Hierarchical match with weighted importance
        hierarchy_match = self._hierarchical_degree_match(resume_degree, jd_degree)
        
        # Fuzzy string matching as a fallback
        if self.nlp:
            fuzzy_score = fuzz.ratio(resume_degree, jd_degree) / 100.0
            semantic_score = self._semantic_similarity(resume_degree, jd_degree)
            
            # Weighted combination of techniques
            return min(
                0.5 * hierarchy_match + 
                0.3 * fuzzy_score + 
                0.2 * semantic_score, 
                1.0
            )
        
        return hierarchy_match

    def _hierarchical_degree_match(self, resume_degree: str, jd_degree: str) -> float:
        """
        Compare degrees based on hierarchical importance.
        
        Args:
            resume_degree (str): Normalized resume degree
            jd_degree (str): Normalized job description degree
        
        Returns:
            float: Hierarchical match score (0-1)
        """
        # Position in hierarchy
        degree_order = [
            'unknown', 'certificate', 'associate', 
            'bachelors', 'masters', 'professional', 'doctoral'
        ]
        
        resume_index = degree_order.index(resume_degree)
        jd_index = degree_order.index(jd_degree)
        
        # If resume degree meets or exceeds job description requirement
        if resume_index >= jd_index:
            # Compute relative match based on degree weights
            resume_weight = self.degree_hierarchy.get(resume_degree, {}).get('weight', 0)
            jd_weight = self.degree_hierarchy.get(jd_degree, {}).get('weight', 0)
            if jd_weight:
                return min(resume_weight / jd_weight, 1.0)
            else:
                return 1.0
        
        return 0.0
    
    def _semantic_similarity(self, degree1: str, degree2: str) -> float:
        """
        Compute semantic similarity between degrees.
        
        Args:
            degree1 (str): First degree
            degree2 (str): Second degree
        
        Returns:
            float: Semantic similarity score (0-1)
        """
        if not self.nlp:
            return 0.0
        
        # Convert to spaCy documents
        doc1 = self.nlp(degree1)
        doc2 = self.nlp(degree2)
        
        # Compute semantic similarity
        return doc1.similarity(doc2)

    #*   EDUCATION SECTION ENDS  *#

    
    def match_job_title(self, resume_titles: List[str], jd_titles: List[str]) -> float:
        """
        Match job title relevance between resume and job description titles.
        
        Args:
            resume_titles (List[str]): Job titles from resume
            jd_titles (List[str]): Job titles from job description
        
        Returns:
            float: Job title relevance score (0-1)
        """
        if not jd_titles or not resume_titles:
            return 0.0
        
        # Convert all titles to lowercase for matching
        resume_titles_lower = [title.lower() for title in resume_titles]
        jd_titles_lower = [title.lower() for title in jd_titles]
        
        # For each JD title, find best match from resume titles
        title_matches = []
        for jd_title in jd_titles_lower:
            matches = [
                1.0 if jd_title in resume_title else 
                0.5 if any(word in resume_title for word in jd_title.split()) 
                else 0.0 
                for resume_title in resume_titles_lower
            ]
            title_matches.append(max(matches) if matches else 0.0)
        
        # Return average of best matches for each JD title
        return sum(title_matches) / len(jd_titles) if title_matches else 0.0

    def match_full_text(self, resume_text: List[str], jd_text: List[str]) -> float:
        """
        Match full text content between resume and job description.
        
        Args:
            resume_text (str): Full text content of resume
            jd_text (str): Full text content of job description
            
        Returns:
            float: Full text match score between 0 and 1
        """
        if not resume_text or not jd_text:
            return 0.0
            
        similarity_score = self.compute_similarity(resume_text, jd_text)
        
        # Add bonus for keyword overlap
        resume_words = set(resume_text)
        jd_words = set(jd_text)
        
        overlap = len(resume_words.intersection(jd_words))
        total = len(jd_words)
        
        if total > 0:
            keyword_score = overlap / total
        else:
            keyword_score = 0.0
            
        # Combine semantic and keyword scores
        final_score = (0.7 * similarity_score) + (0.3 * keyword_score)
        
        return min(final_score, 1.0)

def main():
    """
    Example usage of ResumeScorer.
    """
        
    # Sample texts (similar to extraction.py example)
    resume_text = '''
        John Doe
        Email: john.doe@email.com
        Phone: 5551234567
        New York, NY

        EXPERIENCE
        Senior Software Engineer
        Tesla, Palo Alto, CA
        June 2019 - Present
        • Led microservices architecture design
        • Created CI/CD pipeline
        
        SKILLS
        • Python, Java, JavaScript
        • AWS, Docker, Kubernetes
        
        EDUCATION
        University of Washington
        Bachelor of Science in Computer Science
        Graduation: May 2019
    '''
    
    job_description_text = '''
        Job Title: Senior Data Scientist
        Requirements:
        - 5+ years of experience in data science
        - Python, AWS skills
        - Bachelor or Master degree
    '''
    
    # Initialize Extractor and Scorer
    extractor = InformationExtractor()
    scorer = ResumeScorer()
    
    # Extract structured data
    extracted_data = extract_resume_and_job_description(
        resume_text, 
        job_description_text, 
    )
    
    # Score resume
    scores = scorer.score_resume(extracted_data)
    for metric, score in scores.items():
        print(f"{metric}: {score}")

if __name__ == "__main__":
    main()