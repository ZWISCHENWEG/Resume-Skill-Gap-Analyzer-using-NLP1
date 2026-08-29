import pytest
from src.nlp.matching import MatchingEngine
from src.nlp.preprocessing import TextPreprocessor

@pytest.fixture
def engine():
    return MatchingEngine()

@pytest.fixture
def preprocessor():
    return TextPreprocessor()

# --- TF-IDF & Cosine Similarity Tests ---

def test_identical_text(engine):
    # Identical text -> approx 100%
    r_tokens = ["python", "developer", "aws"]
    j_tokens = ["python", "developer", "aws"]
    score = engine.calculate_similarity(r_tokens, j_tokens)
    assert score == 100.0

def test_completely_different_text(engine):
    # Completely different text -> 0%
    r_tokens = ["python", "developer"]
    j_tokens = ["marketing", "manager"]
    score = engine.calculate_similarity(r_tokens, j_tokens)
    assert score == 0.0

def test_partially_overlapping_text(engine):
    # Partial overlap -> intermediate similarity
    r_tokens = ["python", "developer", "sql"]
    j_tokens = ["python", "developer", "aws"]
    score = engine.calculate_similarity(r_tokens, j_tokens)
    assert 0.0 < score < 100.0

def test_same_text_different_capitalization(engine, preprocessor):
    # If preprocessor outputs were mixed case, vectorizer lowercase=True handles it
    r_tokens = ["Python", "Developer"]
    j_tokens = ["python", "developer"]
    score = engine.calculate_similarity(r_tokens, j_tokens)
    assert score == 100.0

def test_empty_resume(engine):
    r_tokens = []
    j_tokens = ["python", "developer"]
    score = engine.calculate_similarity(r_tokens, j_tokens)
    assert score == 0.0

def test_empty_job_description(engine):
    r_tokens = ["python", "developer"]
    j_tokens = []
    score = engine.calculate_similarity(r_tokens, j_tokens)
    assert score == 0.0

def test_both_empty(engine):
    score = engine.calculate_similarity([], [])
    assert score == 0.0

def test_repeated_words(engine):
    # TF-IDF penalizes high frequency if DF is high, but here both docs have the words.
    r_tokens = ["python", "python", "python"]
    j_tokens = ["python"]
    # They share the exact same vocabulary. Cosine angle between [x] and [y] is 0 degrees -> 1.0
    score = engine.calculate_similarity(r_tokens, j_tokens)
    assert score == 100.0

def test_multi_word_phrases(engine):
    # We join tokens by space, so "machine learning" becomes two tokens to TfidfVectorizer.
    r_tokens = ["machine", "learning", "engineer"]
    j_tokens = ["machine", "learning", "expert"]
    score = engine.calculate_similarity(r_tokens, j_tokens)
    assert 0.0 < score < 100.0
    assert score > 50.0  # Should be high because they share 2/3 words

def test_deterministic_repeated_calculation(engine):
    r_tokens = ["python", "developer"]
    j_tokens = ["python", "engineer"]
    score1 = engine.calculate_similarity(r_tokens, j_tokens)
    score2 = engine.calculate_similarity(r_tokens, j_tokens)
    assert score1 == score2


# --- Skill Gap Mathematics Tests ---

def test_identical_skill_sets(engine):
    r_skills = ["Python", "SQL"]
    j_skills = ["Python", "SQL"]
    res = engine.calculate_skill_gap(r_skills, j_skills)
    assert res["matched_skills"] == ["Python", "SQL"]
    assert res["missing_skills"] == []
    assert res["additional_skills"] == []
    assert res["skill_coverage"] == 100.0

def test_completely_different_skill_sets(engine):
    r_skills = ["Python"]
    j_skills = ["Java"]
    res = engine.calculate_skill_gap(r_skills, j_skills)
    assert res["matched_skills"] == []
    assert res["missing_skills"] == ["Java"]
    assert res["additional_skills"] == ["Python"]
    assert res["skill_coverage"] == 0.0

def test_partial_overlap(engine):
    r_skills = ["Python", "AWS", "Git"]
    j_skills = ["Python", "AWS", "Docker"]
    res = engine.calculate_skill_gap(r_skills, j_skills)
    assert res["matched_skills"] == ["AWS", "Python"]  # Sorted alphabetically
    assert res["missing_skills"] == ["Docker"]
    assert res["additional_skills"] == ["Git"]
    assert res["skill_coverage"] == round((2/3)*100, 2)

def test_empty_resume_skill_set(engine):
    res = engine.calculate_skill_gap([], ["Python"])
    assert res["matched_skills"] == []
    assert res["missing_skills"] == ["Python"]
    assert res["skill_coverage"] == 0.0

def test_empty_job_skill_set(engine):
    res = engine.calculate_skill_gap(["Python"], [])
    assert res["matched_skills"] == []
    assert res["missing_skills"] == []
    assert res["skill_coverage"] == 0.0  # As defined in plan

def test_alias_normalized_skills(engine):
    # Engine expects canonical names, so we just test duplicate elimination implicitly via sets
    r_skills = ["React"]
    j_skills = ["React"]
    res = engine.calculate_skill_gap(r_skills, j_skills)
    assert res["matched_skills"] == ["React"]

def test_duplicate_skills(engine):
    r_skills = ["Python", "Python"]
    j_skills = ["Python"]
    res = engine.calculate_skill_gap(r_skills, j_skills)
    assert res["matched_skills"] == ["Python"]
    assert res["additional_skills"] == []
    assert res["skill_coverage"] == 100.0

# --- Mathematical Verification ---

def test_mathematical_verification_as_requested(engine):
    """
    Example from instructions:
    Resume skills: {Python, SQL, Git}
    Job skills: {Python, SQL, Docker, AWS}
    Expected:
    Matched: {Python, SQL}
    Missing: {Docker, AWS}
    Coverage: 2 / 4 * 100 = 50%
    """
    r_skills = ["Python", "SQL", "Git"]
    j_skills = ["Python", "SQL", "Docker", "AWS"]
    
    res = engine.calculate_skill_gap(r_skills, j_skills)
    
    assert res["matched_skills"] == ["Python", "SQL"]
    assert res["missing_skills"] == ["AWS", "Docker"] # Sorted
    assert res["skill_coverage"] == 50.0

# --- Combined Analysis Result ---

def test_calculate_match(engine):
    resume_pre = {"filtered_tokens": ["python", "dev"]}
    job_pre = {"filtered_tokens": ["python", "dev"]}
    
    resume_ext = {"canonical_names": ["Python"]}
    job_ext = {"canonical_names": ["Python", "SQL"]}
    
    res = engine.calculate_match(resume_pre, job_pre, resume_ext, job_ext)
    
    assert res["similarity_score"] == 100.0
    assert res["resume_skills"] == ["Python"]
    assert res["job_skills"] == ["Python", "SQL"]
    assert res["matched_skills"] == ["Python"]
    assert res["missing_skills"] == ["SQL"]
    assert res["additional_skills"] == []
    assert res["skill_coverage"] == 50.0
