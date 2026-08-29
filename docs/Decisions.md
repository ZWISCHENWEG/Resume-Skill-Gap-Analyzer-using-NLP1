# Architectural Decisions

### 1. Python 3.14.2 Dependency Verification
- **Decision**: Delayed blind dependency installation and successfully tested imports in an isolated virtual environment (`.venv`). All core packages imported successfully.

### 2. Curated Vocabulary over Generic NER
- **Decision**: Use a curated, extensible technical skill vocabulary, normalization, and phrase matching as the primary mechanism for skill extraction, completely rejecting generic Named Entity Recognition (NER).

### 3. Rejection of spaCy; Selection of NLTK
- **Decision**: Reject `spaCy` in favor of `NLTK` (and standard Regex) to avoid massive model bloat for tasks that don't require deep dependency parsing.

### 4. Separation of Overall Similarity vs. Skill Gap
- **Decision**: The system uses TF-IDF + Cosine Similarity for the Overall Similarity score, and Set Operations (`Job Skills - Resume Skills`) for exact Skill Gap detection.

### 5. Dedicated Dataset Exploration Phase
- **Decision**: Implemented `src/data_analysis/fetch_and_explore.py` to source datasets directly from raw GitHub mirrors of public Kaggle data without violating Terms of Service via scraping.

### 6. Ground-Truth Evaluation Requirement
- **Decision**: Require testing the skill extraction against manually verified examples. The datasets fetched in Phase 2 will be randomly sampled, manually annotated, and used as a test suite in Phase 8.

### 7. Explicit Alias and Ambiguity Handling Strategy
- **Decision**: Build an exact-match phrase dictionary with explicit alias mapping (e.g., `{"js": "JavaScript", "node.js": "Node.js", "machine learning": "Machine Learning"}`).
- **Handling Ambiguity**: Ambiguous single-letter skills (like "R" or "C") will be matched strictly using regex word boundaries (`\bC\b`, `\bR\b`) and case-sensitivity checks where appropriate, preventing false positives from common words or substrings. All other non-ambiguous terms will be lowercased before matching to maximize recall.
### 8. Text Extraction Libraries
- **Decision**: Use `PyMuPDF` (`pymupdf`) for PDFs and `python-docx` for DOCX files.
- **Rationale**: `PyMuPDF` provides robust text extraction (via `page.get_text("text")`) preserving readable document order without requiring full OCR. `python-docx` trivially allows paragraph and table traversal, essential for modern formatted resumes. Both throw catchable exceptions for corrupted/empty documents.

### 9. Selective Punctuation Removal for NLP
- **Decision**: Avoid generic punctuation stripping. Instead, selectively remove grammatical punctuation (`,`, `;`, `:`, `(`, `)`, `[`, `]`, `!`, `?`) while explicitly preserving symbols critical to technical terms (`+`, `#`, `/`, `-`, and embedded `.`).
- **Rationale**: A naive `string.punctuation` removal destroys skills like `C++`, `Node.js`, and `CI/CD`. This selective strategy guarantees technical phrases survive for Phase 5 extraction while keeping text clean for TF-IDF.

### 10. Multi-Output Preprocessing Pipeline
- **Decision**: The NLP pipeline outputs multiple variations of the text: `cleaned_text` (retains stop-words for intact multi-word phrase matching), `tokens`, and `filtered_tokens` (standard NLTK stop-words removed for TF-IDF).
- **Rationale**: Removing stop-words universally breaks skills like "Internet of Things" or "Ruby on Rails". Segregating the outputs ensures we have the right data shape for both exact skill extraction and semantic similarity.

### 11. Dual-Matching Strategy for Ambiguity
- **Decision**: Unambiguous skills (like "Python" or "Machine Learning") are matched case-insensitively against the punctuation-stripped `cleaned_text`. Ambiguous single-letter skills (like "C" and "R") are matched case-sensitively against the raw `original_text`.
- **Rationale**: A naive regex for `\bc\b` on lowercased text triggers catastrophic false positives for common English (e.g. the "c" in bullet points or "communication"). Checking `original_text` securely resolves this without requiring heavy NER models.

### 12. Non-Word Character Boundaries
- **Decision**: Replaced standard `\b` regex boundaries with negative lookbehinds/lookaheads `(?<!\w)...(?!\w)`.
- **Rationale**: `\b` evaluates boundaries between word (`\w`) and non-word (`\W`) characters. Skills ending in symbols (e.g., `C++`, `.NET`) break standard `\b` assertions because `+` and space are both non-word. The lookahead logic prevents extracting partial matches (like "C++_dev") while successfully capturing the pure skill.

### 13. Subsumed Match Filtering (Overlap Handling)
- **Decision**: If the extraction engine finds multiple skill spans in the same text string where one span is entirely consumed by the other, the subsumed (smaller) match is discarded.
- **Rationale**: Prevents returning both "React" and "React JS" when parsing "Experience with React JS", ensuring clean, canonical output.

### 14. Input Representation for TF-IDF
- **Decision**: The TF-IDF vectorizer explicitly consumes `filtered_tokens` (where words are joined by spaces) rather than raw text or `cleaned_text`.
- **Rationale**: `filtered_tokens` has all NLTK stop-words removed and punctuation stripped. Feeding this to the vectorizer prevents common words ("and", "is", "the") from inflating the similarity score, ensuring the algorithm measures the overlap of actual nouns, verbs, and technical jargon.

### 15. Zero Division & Edge Case Handling in Matching
- **Decision**: If a Job Description has 0 extracted skills, the `skill_coverage` metric defaults to 0.0% (rather than 100% or throwing a ZeroDivisionError). Empty input arrays to the vectorizer are caught and return a 0.0% Similarity Score.
- **Rationale**: A completely blank JD shouldn't guarantee a 100% perfect skill match. Returning 0.0% safely handles edge cases without crashing the matching mathematics.

### 16. Pure UI Layer Architecture
- **Decision**: The Streamlit application (`src/app.py`) is restricted solely to input gathering, visualization, and sequential backend function calls. It contains no text manipulation or algorithm logic.
- **Rationale**: Keeps the analytical core pristine, tested, and fully decoupled from the UI framework, ensuring the engine remains explainable and strictly bounded by the NLP algorithms built in earlier phases.
