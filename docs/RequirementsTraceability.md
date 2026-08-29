# Requirements Traceability Matrix

This document maps the original PBL requirements to their final implementation in the Resume Skill Gap Analyzer.

## Core PBL Requirements

### 1. Data Collection & Dataset
- **Requirement**: Use available datasets (e.g., from Kaggle).
- **Implementation**: Utilized a Python script (`src/data_analysis/fetch_and_explore.py`) to download Kaggle dataset mirrors from GitHub raw URLs to avoid scraping limitations.
- **Evidence**: `data/raw/resume_dataset.csv` and `data/raw/jd_dataset.csv` successfully downloaded and documented in Phase 2.

### 2. Text Preprocessing
- **Requirement**: Implement NLP preprocessing (lowercasing, punctuation removal, tokenization).
- **Implementation**: Created `TextPreprocessor` (`src/nlp/preprocessing.py`). Crucially, technical punctuation (`+`, `#`, `.`, `-`) is preserved to prevent corrupting skills like `C++` or `Node.js`.
- **Evidence**: 20 tests in `tests/test_preprocessing.py` confirm stop-word removal and specific technical punctuation survival.

### 3. Feature & Skill Extraction
- **Requirement**: Extract relevant technical skills from both the Resume and the Job Description.
- **Implementation**: Created `SkillExtractor` (`src/nlp/skill_extractor.py`). It uses a curated technical vocabulary, overlap resolution (to prevent counting both "React" and "React JS"), and dual-matching (ambiguous single-letter skills like "C" are matched securely on original text, while standard skills are matched case-insensitively).
- **Evidence**: Ground-truth evaluation in `tests/test_ground_truth.py` demonstrates a Precision of 96% and Recall of 100% on a sample of realistic resume snippets.

### 4. Vectorization & Matching
- **Requirement**: Compute similarity between Resume and JD using TF-IDF and Cosine Similarity.
- **Implementation**: Created `MatchingEngine` (`src/nlp/matching.py`). It vectors the `filtered_tokens` (text stripped of grammatical stop words) using `scikit-learn`'s `TfidfVectorizer` and calculates textual overlap using `cosine_similarity`.
- **Evidence**: Tested heavily in `tests/test_matching.py`. Edge cases like empty inputs are caught.

### 5. Skill Gap Analysis
- **Requirement**: Identify missing skills explicitly.
- **Implementation**: Supplementing the lexical TF-IDF score, the system calculates exact skill gaps using deterministic Set Mathematics (Job - Resume).
- **Evidence**: 19 tests in `tests/test_matching.py` confirm accurate intersections and differences.

### 6. Output & Visualization
- **Requirement**: Display overall similarity, matched skills, missing skills, and visual representations.
- **Implementation**: Created `src/app.py` using Streamlit. It consumes the decoupled NLP backend and displays the matching metrics cleanly alongside a bar chart visualization of the exact skill gaps.
- **Evidence**: Fully functional local web application handling PDF and DOCX uploads gracefully.

## Project Constraints & Traceability
- **Constraint**: Must remain explainable and academic.
- **Traceability**: Generative AI and unexplainable deep-learning LLMs were strictly avoided. The extraction uses deterministic boundaries, and the NLP engine uses standard lexical mathematics (TF-IDF), accompanied by an educational "How it works" section in the UI.

- **Constraint**: Fast execution.
- **Traceability**: By relying on exact-phrase matching and TF-IDF instead of deep transformer models (like BERT or spaCy), processing representative resumes completes almost instantly.
