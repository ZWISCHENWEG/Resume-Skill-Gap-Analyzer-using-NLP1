# Project Memory

### Status
- **Current Phase**: Phase 6 (Completed).
- **Next Action**: Awaiting user approval of Phase 6 before starting Phase 7 (UI & Visualization).

### Important Constraints
- **Python 3.14.2 Compatibility**: Verified successfully in Phase 1. `NLTK` chosen over `spaCy`.
- **Skill Extraction Strategy**: Strictly reliant on a curated vocabulary, normalization, and phrase matching. Must avoid merging ambiguous abbreviations blindly (e.g., 'R' programming language vs letter 'R').
- **Separation of Concerns**: 
  - TF-IDF + Cosine Similarity = Overall Match %.
  - Job Skills set MINUS Resume Skills set = Skill Gap.
- **Academic Focus**: Demonstrating deterministic Data Science/NLP techniques (no opaque GenAI).

### Workspace Context
- **Python Env**: Isolated `.venv` is active with verified `requirements.txt`.
- **Data (Phase 2 Findings)**:
  - **Resume Dataset**: Downloaded from Kaggle mirror (169 rows, columns: `Category`, `Resume`). Found 3 duplicates. Clean text.
  - **JD Dataset**: Downloaded from LinkedIn-Tech-Job-Data mirror (8261 rows, 18 columns including `description`, `title`). Found 481 missing descriptions to be handled.
  - **Exploration**: Built `src/data_analysis/fetch_and_explore.py` which successfully loaded, inspected, and ran basic word-frequency extraction on the texts. Discovered strong prevalence of technical terms (`data`, `software`, `java`, `sql`, `cloud`, `machine learning`) confirming the viability of a dictionary-based approach.

### Planned Data Usage
- **Development & Vocabulary Building**: We will use the frequency counts and domain knowledge to build the `skill_dictionary.json` used by our phrase matcher.
- **Testing/Evaluation**: We will randomly sample a small set (e.g., 5 Resumes and 5 JDs) from `data/raw/` and manually label their explicit technical skills. These will serve as the ground-truth for Phase 8 automated evaluation. We will NOT claim high accuracy simply because the engine matches its own training dictionary on the same data.

### Phase 3 Extraction Details
- **Modules Created**: `src/extraction/pdf_parser.py`, `src/extraction/docx_parser.py`, `src/extraction/document_parser.py`.
- **Interface**: Exposed a unified `parse_document(filepath)` function that routes based on file extension.
- **Error Handling**: Missing files, unsupported formats, corrupt files, and empty files reliably raise descriptive `FileNotFoundError` or `ValueError`. OCR is explicitly not supported. 
- **Tests**: Exhaustively tested with 9 synthetic file test cases via `pytest`, all passing. No NLP logic was mixed in.

### Phase 4 NLP Preprocessing Details
- **Modules Created**: `src/nlp/preprocessing.py` containing `TextPreprocessor`.
- **Strategy**: Implemented a "Selective Punctuation Removal" approach. General punctuation is stripped, but technical symbols (`+`, `#`, `/`, `-`, embedded `.`) are preserved. This prevents destruction of terms like `C++` or `Node.js`.
- **Outputs**: Generates a dictionary with `original_text`, `cleaned_text` (stop-words intact for phrase matching), `tokens`, and `filtered_tokens` (stop-words removed for TF-IDF).
- **Tests**: Exhaustively tested with 20+ cases including edge cases for multi-word phrases and C/C++/C#/.NET. All passed. No skill matching logic introduced.

### Phase 5 Skill Extraction Details
- **Vocabulary**: Created `data/processed/skill_dictionary.json` featuring 30 structured technical skills.
- **Engine**: Implemented `SkillExtractor` class.
- **Dual Matching**: Matches standard skills case-insensitively on `cleaned_text`, and ambiguous skills (C, R) case-sensitively on `original_text` to prevent massive false positives.
- **Overlap Control**: Filters overlapping skills within the same text region using index containment to resolve the "React JS" vs "React" deduplication issue.
- **August 29, 2026:**
  - Completed Phase 6: Vectorization & Matching Engine. Implemented TF-IDF and Cosine Similarity, plus Set Mathematics for Skill Gaps. Achieved deterministic mathematical evaluation.
  - Completed Phase 7: UI & Visualization. Built the Streamlit interface (`src/app.py`) to wrap the backend analytical modules. Implemented file upload, visualization charts, and an educational "NLP Transparency" expander.
  - Completed Phase 8: Testing & Evaluation. Executed full regression suite (62/62 tests passing). Documented ground truth (96% Precision, 100% Recall on sample). Mapped PBL requirements in `RequirementsTraceability.md` and finalized documentation.

### Phase 6 Matching Engine Details
- **Engine**: Implemented `MatchingEngine` class in `src/nlp/matching.py`.
- **TF-IDF & Cosine Similarity**: Operates on `filtered_tokens` (stop-words removed) to calculate an Overall Match Score (0.0% to 100.0%) using `scikit-learn`.
- **Skill Gap Mathematics**: Operates exclusively on canonical skills returned by Phase 5. Calculates `matched_skills` (Intersection), `missing_skills` (Difference), `additional_skills` (Difference), and `skill_coverage` (Percentage).
- **Evaluation**: Extensively tested (19 new tests) covering edge cases like empty documents, duplicate skills, missing text, and identical sets. Demonstrated explicitly that high textual similarity does NOT guarantee high skill coverage (and vice-versa).
