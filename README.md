# Resume Skill Gap Analyzer using NLP

An academic, deterministic Natural Language Processing (NLP) pipeline designed to evaluate the technical fit between a candidate's resume and a job description. Developed as part of a Project-Based Learning (PBL) lifecycle.

## Problem Statement
Recruiters and candidates struggle to objectively evaluate resumes against job descriptions due to the sheer volume of text and inconsistent terminology. Automated Tracking Systems (ATS) often lack transparency. This project solves this by providing a fully deterministic, explainable mathematical engine to calculate textual similarity and extract concrete skill gaps.

## Objectives
1. Extract raw text from standard Resume formats (`.pdf`, `.docx`).
2. Clean and preprocess the text using core NLP techniques (tokenization, stop-word removal) while strictly preserving technical punctuation (e.g., `C++`, `Node.js`).
3. Extract canonical technical skills from both documents using a curated, alias-aware vocabulary and phrase-boundary matching.
4. Calculate a lexical **Similarity Score** using **TF-IDF** vectorization and **Cosine Similarity**.
5. Calculate explicit **Skill Coverage** and identify **Missing Skills** using exact Set Mathematics.
6. Present the analysis in a clean, user-friendly Streamlit web interface.

## Methodology
The system strictly avoids black-box Generative AI or heavy deep-learning NER models (like `spaCy`), opting instead for a highly transparent pipeline:
1. **Extraction**: `PyMuPDF` and `python-docx` extract raw text.
2. **Preprocessing**: Custom `NLTK` tokenizers clean the text.
3. **Skill Extraction**: Hand-crafted negative lookaheads `(?<!\w)` and dual-matching mechanisms guarantee high precision for both standard and ambiguous single-letter skills (like "C" or "R").
4. **Matching Engine**: `scikit-learn` computes TF-IDF statistical overlap.
5. **Set Math**: Extracts the exact missing requirements ($Job - Resume$).

## Technology Stack
- **Language**: Python 3.14
- **NLP / ML**: `nltk`, `scikit-learn`
- **Extraction**: `pymupdf`, `python-docx`
- **Data / Visualization**: `pandas`, `streamlit`
- **Testing**: `pytest`

## Project Structure
```text
Resume Project/
├── data/
│   └── raw/                   # Downloaded Kaggle datasets (CSV)
├── docs/                      # Extensive PBL Lifecycle documentation
├── src/
│   ├── app.py                 # Streamlit UI
│   ├── extraction/            # PDF & DOCX Parsers
│   ├── nlp/                   # Preprocessing, Skill Extractor, Matching Engine
│   └── data_analysis/         # Dataset fetching scripts
├── tests/                     # 64 automated regression tests
└── README.md
```

## Dataset Information
The underlying evaluation vocabulary was guided by exploring raw GitHub mirrors of two prominent public datasets:
1. **Resume Dataset**: 2,400+ resumes spanning various IT roles.
2. **Job Description Dataset**: Standard IT roles with specific requirements.
*Note: Datasets were fetched cleanly without TOS-violating scraping.*

## How to Install
1. Ensure Python 3.14 (or compatible Python 3.x) is installed.
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Download necessary NLTK data (handled automatically by the application on first run).

## How to Run
To launch the Streamlit Web Application:
```bash
streamlit run src/app.py
```
Open `http://localhost:8501` in your browser.

To run the automated test suite:
```bash
pytest -v
```

## Evaluation Results
The system is backed by a robust regression suite consisting of 64 unit tests covering edge cases like empty files, unreadable PDFs, and boundary anomalies.
On a manually verified Ground-Truth subset of realistic resume snippets, the **Skill Extraction Engine** achieved:
- **Precision**: 96%
- **Recall**: 100%
- **F1 Score**: 98%

## Known Limitations
- **Lexical, not Semantic**: TF-IDF measures statistical word overlap. It does not possess deep semantic understanding (e.g., it will not inherently link "Machine Learning" to "Predictive Models" unless they share exact tokenized words).
- **Static Vocabulary**: The skill extraction relies on a curated vocabulary dictionary. Unrecognized niche tools will not be extracted unless added to `data/processed/skill_dictionary.json`.

## Future Improvements
- Expand the technical vocabulary to encompass more domains (e.g., specific Medical or Legal terminologies).
- Integrate Sentence Transformers (e.g., `all-MiniLM-L6-v2`) to capture true semantic similarity, replacing TF-IDF.
- Add visual PDF bounding-box highlighting for extracted skills.
