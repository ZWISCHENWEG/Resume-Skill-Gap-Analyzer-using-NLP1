# Architecture & System Design
## Resume Skill Gap Analyzer using NLP

### 1. Overall Architecture
The system follows a modular, monolithic architecture typical for data science academic projects. It separates concerns into data ingestion, dataset exploration, preprocessing (cleaning text), skill extraction (curated vocabulary), mathematical comparison (TF-IDF vectorization and similarity), skill gap set operations, and presentation (UI).

### 2. Application Flow
1. **Input Stage**: User uploads a resume (PDF/DOCX) and inputs a Job Description.
2. **Parsing Stage**: Document parsers extract raw text from the files.
3. **Preprocessing Stage**: Text is cleaned (lowercased, tokenized, stop words and punctuation removed).
4. **Extraction Stage**: Technical skills are explicitly extracted using phrase matching and a curated vocabulary.
5. **Analysis Stage**: 
   - *Similarity Engine*: Calculates Overall Resume-JD Similarity.
   - *Gap Engine*: Calculates explicitly Matched and Missing skills.
6. **Output Stage**: UI dashboard renders scores, lists, and visualizations.

### 3. Folder Structure
```
project_root/
│
├── docs/                 # Project documentation
├── data/                 # Raw and processed datasets (Resume/JD data)
├── src/                  # Main source code
│   ├── app.py            # Main Streamlit UI application
│   ├── data_analysis/    # Scripts/Notebooks for dataset exploration
│   ├── extraction/       # PDF & DOCX text extractors (`document_parser.py` unified interface)
│   ├── nlp/              # Text preprocessing & explicit Skill Extraction pipelines
│   ├── matching/         # Vectorization (TF-IDF) & Set Operations
│   └── utils/            # Helper functions
├── tests/                # Unit tests and manual evaluation scripts
├── requirements.txt      # Verified Python dependencies
└── README.md             # Entry point
```

### 4. Technology Stack & Dependencies
- **Language**: Python 3.14.2 (Verified in `.venv`)
- **UI Framework**: `streamlit`
- **Text Parsing**: `PyMuPDF` (`pymupdf`) for PDF, `python-docx` for DOCX.
- **Data Manipulation**: `pandas`, `numpy`
- **NLP & Preprocessing**: `nltk` (for tokenization and stop words)
- **Vectorization & Similarity**: `scikit-learn` (TF-IDF, Cosine Similarity)
- **Testing**: `pytest`

### 5. NLP & Skill Extraction Pipeline
- **Preprocessing**: 
  - **Whitespace Normalization**: Reducing newlines, tabs, and multiple spaces to a single space.
  - **Lowercasing**: Converting all text to lowercase for standard NLP matching.
  - **Selective Punctuation Handling**: Removing general grammatical punctuation (e.g., commas, colons, brackets, exclamation marks, and sentence-ending periods) while explicitly preserving technical symbols (e.g., `+`, `#`, `/`, `-`, and embedded periods like `.NET` or `Node.js`).
  - **Tokenization**: Deterministic splitting by space, outputting standard `tokens`.
  - **Stop-word Filtering**: NLTK stop-words are removed to create a `filtered_tokens` list strictly for TF-IDF. The `cleaned_text` string and full `tokens` list are preserved for phrase-level Skill Extraction (Phase 5) to avoid breaking multi-word concepts (e.g., "Internet of Things").
- **Explicit Skill Extraction (Phase 5)**: 
  - **Curated Technical Vocabulary**: A JSON dictionary (`data/processed/skill_dictionary.json`) of technical skills validated by empirical exploration.
  - **Normalization & Aliases**: Explicit mapping of synonyms to a canonical form (e.g., "NodeJS", "Node.js" -> "Node.js").
  - **Matching Strategy**: Phrase matching is conducted deterministically. Unambiguous skills match against the lowercased `cleaned_text` using boundary negative lookbehinds/lookaheads (`(?<!\w)`). Ambiguous skills (like `C`, `R`) are matched case-sensitively against the `original_text` to eliminate false positives (e.g. "communication", "research").
  - **Overlap Handling**: Overlapping matches of the same class (e.g. "React" inside "React JS") are resolved by keeping the longest match, preventing duplicate subset skills.

### 6. Vectorization & Overall Similarity Engine (Phase 6)
- **Purpose**: Calculate how conceptually close the entire Resume is to the Job Description, distinct from explicit skill matching.
- **Algorithm**: `TfidfVectorizer` (Term Frequency-Inverse Document Frequency) followed by `cosine_similarity`.
- **Input**: The engine consumes the `filtered_tokens` list from Phase 4, joined by spaces. This ensures standard English stop-words are ignored and focus remains on domain vocabulary.
- **Output**: A raw scalar (0.0 to 1.0) multiplied by 100 to yield a deterministic **Similarity Score Percentage**.
- **Limitations**: Measures statistical lexical overlap, not true deep semantic meaning (e.g., "predictive models" and "machine learning" will not inherently match unless they share exact tokenized words).

### 7. Explicit Skill Gap Analysis (Phase 6)
- **Purpose**: Measure exactly which required technical skills the candidate possesses.
- **Algorithm**: Deterministic Set Mathematics.
- **Input**: The deduplicated `canonical_names` arrays produced by Phase 5.
- **Metrics**: 
  - **Matched Skills**: Intersection ($Resume \cap Job$)
  - **Missing Skills**: Difference ($Job - Resume$)
  - **Additional Skills**: Difference ($Resume - Job$)
  - **Skill Coverage**: $(|Matched| / |Job|) \times 100$ 

### 8. Streamlit UI (Phase 7)
- **Purpose**: Provide a clean, user-friendly interface for the "Resume Skill Gap Analyzer".
- **Module**: `src/app.py`
- **Methodology**: 
  - Strictly separates UI from backend processing.
  - Takes a PDF/DOCX resume via `st.file_uploader` and Job Description via `st.text_area`.
  - Sequentially passes inputs through: Document Parser -> Text Preprocessor -> Skill Extractor -> Matching Engine.
  - Displays deterministic results via `st.metric`, lists, and `st.bar_chart`.
  - Includes an academic transparency expander to explain NLP processes (TF-IDF, Cosine Similarity).
