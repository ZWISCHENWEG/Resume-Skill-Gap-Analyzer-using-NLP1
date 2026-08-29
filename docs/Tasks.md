# Implementation Tasks & Roadmap

### Phase 0: Inspection & Planning (Completed)
- [x] Inspect workspace and environment.
- [x] Create project documentation (PRD, Architecture, Rules, Design, Tasks, Memory).
- [x] Define Roadmap and adjust based on review.

### Phase 1: Environment & Dependency Verification (Completed)
- [x] Verify Python 3.14.2 compatibility with proposed core packages.
- [x] Install only the required, compatible dependencies.
- [x] Initialize Python virtual environment/requirements.txt.
- [x] Setup initial folder structure (`src/`, `data/`, `tests/`).

### Phase 2: Dataset Collection & Exploration (Completed)
- [x] Identify suitable publicly available Resume and Job Description datasets (e.g., from Kaggle).
- [x] Inspect dataset structure, sample records, and useful columns.
- [x] Check for missing values, duplicates, and formatting inconsistencies.
- [x] Determine how the datasets will be used for testing, evaluation, and building the skill vocabulary.
- [x] Document dataset source and usage.

### Phase 3: Data Handling & Text Extraction (Completed)
- [x] Implement PDF text extraction (`src/extraction/pdf_parser.py`).
- [x] Implement DOCX text extraction (`src/extraction/docx_parser.py`).
- [x] Write unit tests for extractors ensuring robustness against bad files.

### Phase 4: NLP Preprocessing (Completed)
- [x] Implement text cleaner (lowercase, remove punctuation, remove stop words).
- [x] Create tokenization logic.

### Phase 5: Skill Extraction Engine (Curated Vocabulary) (Completed)
- [x] Build an extensible technical skill dictionary/vocabulary (derived from Phase 2 exploration).
- [x] Implement skill normalization and alias resolution safely (avoiding ambiguous abbreviations).
- [x] Implement phrase matching to extract exact technical terms from cleaned text.

### Phase 6: Vectorization & Matching Engine (Completed)
- [x] Implement TF-IDF vectorizer and Cosine Similarity for **Overall Similarity** score.
- [x] Implement deterministic set mathematics for **Explicit Skill Gap Analysis** (Matched, Missing, Additional).
- [x] Consolidate into a modular calculation engine returning structured JSON (ready for Phase 7).

### Phase 7: UI & Visualization (Completed)
- [x] Build Streamlit sidebar for inputs.
- [x] Integrate document parsing with Streamlit file uploader.
- [x] Hook up text preprocessing & skill extraction.
- [x] Hook up matching engine & similarity calculations.
- [x] Create clean, academic visual styling (using `st.metric`, `st.bar_chart`).
- [x] Add "NLP Transparency" section (showing raw vs preprocessed text if needed).

### Phase 8: Testing & Evaluation (Completed)
- [x] Create a set of manually verified examples (ground-truth resumes and JDs sampled from `data/raw`).
- [x] Run precision/recall metrics on the Skill Extraction engine.
- [x] Ensure 100% of the extraction, preprocessing, and matching tests pass.
- [x] Document the mathematical verification of the Skill Gap detection.
- [x] Write the final README and finalize all architecture/design documentation.
- [ ] Refactor, finalize code, and freeze for PBL demonstration.
