import math
from typing import Dict, Any, List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class MatchingEngine:
    """
    Engine for calculating structural and textual similarity between Resumes and Job Descriptions.
    Implements TF-IDF + Cosine Similarity for overall text matching, and explicitly calculates
    skill gap coverage using set mathematics based on extracted canonical skills.
    """

    def __init__(self):
        # We use TfidfVectorizer to compute Term Frequency-Inverse Document Frequency.
        # We don't provide stop_words here because the preprocessor already returns
        # `filtered_tokens` which have NLTK stop-words removed and technical punctuation preserved.
        self.vectorizer = TfidfVectorizer(lowercase=True)

    def calculate_similarity(self, resume_tokens: List[str], job_tokens: List[str]) -> float:
        """
        Calculates the Cosine Similarity between the resume and the job description
        using their filtered tokens.
        
        Args:
            resume_tokens: List of filtered tokens from the Resume.
            job_tokens: List of filtered tokens from the Job Description.
            
        Returns:
            A percentage score (0.0 to 100.0) rounded to 2 decimal places.
        """
        if not resume_tokens or not job_tokens:
            return 0.0

        # Join tokens back into space-separated strings as expected by TfidfVectorizer
        resume_text = " ".join(resume_tokens)
        job_text = " ".join(job_tokens)

        # Vectorize both texts together to ensure they share the same vocabulary space
        try:
            tfidf_matrix = self.vectorizer.fit_transform([resume_text, job_text])
        except ValueError:
            # Raised if vocab is empty (e.g. only stop words remained, or empty string after parsing)
            return 0.0

        # tfidf_matrix[0] is resume, tfidf_matrix[1] is job
        # cosine_similarity returns a 2D array, e.g., [[1.0, 0.75], [0.75, 1.0]]
        # We want the similarity between document 0 and document 1
        similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        score = similarity_matrix[0][0]
        
        # Clamp between 0 and 1 just in case of minor floating point inaccuracies
        score = max(0.0, min(1.0, score))

        # Convert to percentage
        return round(score * 100, 2)

    def calculate_skill_gap(self, resume_skills: List[str], job_skills: List[str]) -> Dict[str, Any]:
        """
        Performs set mathematics on canonical skills to determine overlaps and gaps.
        
        Args:
            resume_skills: List of canonical skill names from Resume.
            job_skills: List of canonical skill names from Job Description.
            
        Returns:
            Dictionary containing matched, missing, and additional skills, plus coverage percentage.
        """
        r_set = set(resume_skills)
        j_set = set(job_skills)

        matched_skills = sorted(list(r_set.intersection(j_set)))
        missing_skills = sorted(list(j_set.difference(r_set)))
        additional_skills = sorted(list(r_set.difference(j_set)))

        # Skill coverage: what percentage of the requested job skills does the resume contain?
        if len(j_set) == 0:
            skill_coverage = 0.0  # As decided in implementation plan, 0% coverage if no skills asked
        else:
            skill_coverage = round((len(matched_skills) / len(j_set)) * 100, 2)

        return {
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "additional_skills": additional_skills,
            "skill_coverage": skill_coverage
        }

    def calculate_match(self, resume_preprocessed: Dict[str, Any], job_preprocessed: Dict[str, Any],
                        resume_extracted_skills: Dict[str, Any], job_extracted_skills: Dict[str, Any]) -> Dict[str, Any]:
        """
        Combines TF-IDF similarity and Skill Gap analysis into a single deterministic result.
        
        Args:
            resume_preprocessed: Output from TextPreprocessor for the resume.
            job_preprocessed: Output from TextPreprocessor for the JD.
            resume_extracted_skills: Output from SkillExtractor for the resume.
            job_extracted_skills: Output from SkillExtractor for the JD.
            
        Returns:
            Combined dictionary payload for the future UI.
        """
        # 1. Overall Similarity using TF-IDF on filtered tokens
        resume_tokens = resume_preprocessed.get("filtered_tokens", [])
        job_tokens = job_preprocessed.get("filtered_tokens", [])
        similarity_score = self.calculate_similarity(resume_tokens, job_tokens)

        # 2. Skill Gap Analysis
        resume_skills = resume_extracted_skills.get("canonical_names", [])
        job_skills = job_extracted_skills.get("canonical_names", [])
        
        gap_results = self.calculate_skill_gap(resume_skills, job_skills)

        # 3. Compile output
        return {
            "similarity_score": similarity_score,
            "resume_skills": sorted(resume_skills),
            "job_skills": sorted(job_skills),
            "matched_skills": gap_results["matched_skills"],
            "missing_skills": gap_results["missing_skills"],
            "additional_skills": gap_results["additional_skills"],
            "skill_coverage": gap_results["skill_coverage"]
        }
