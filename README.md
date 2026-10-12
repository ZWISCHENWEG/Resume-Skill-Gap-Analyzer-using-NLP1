# Resume Skill Gap Analyzer using NLP

A deterministic Natural Language Processing (NLP) web application designed to evaluate candidate resumes against target job descriptions, extracting canonical technical skills and identifying explicit skill gaps.

---

## Overview

Recruiters and job applicants often face difficulty in objectively assessing how well a resume aligns with a technical job description. Standard Applicant Tracking Systems (ATS) can be opaque. This project provides a transparent, explainable pipeline:
1. **Document Parsing**: Extracts clean text from standard `.pdf` and `.docx` resumes.
2. **NLP Preprocessing**: Normalizes text while strictly preserving technical punctuation (e.g., `C++`, `C#`, `.NET`, `Node.js`).
3. **Skill Extraction**: Identifies technical skills using a curated dictionary with regex boundary lookaheads and alias mapping.
4. **Overall Match Score**: Computes lexical similarity across the document vocabulary using TF-IDF and Cosine Similarity.
5. **Skill Gap Analysis**: Computes explicit skill coverage and missing qualifications using Discrete Set Mathematics.

---

## Technology Stack

- **Programming Language**: Python 3.14 (compatible with Python 3.10+)
- **Web Interface**: Streamlit
- **NLP & Vectorization**: NLTK (stop-word removal), scikit-learn (TF-IDF vectorizer & cosine similarity)
- **Document Extraction**: PyMuPDF (`fitz`), python-docx
- **Data & Charting**: pandas, Altair
- **Automated Testing**: pytest

---

## Project Structure

```text
Resume Project/
├── PBL_Activity_Resume_Skill_Gap_Analyzer.pdf     # Academic PBL specification
├── Resume_Skill_Gap_Analyzer_Presentation.pptx   # Presentation slide deck
├── README.md                                     # Project documentation
├── requirements.txt                              # Pinned Python dependencies
├── pytest.ini                                    # Test runner configuration
├── data/
│   ├── processed/
│   │   └── skill_dictionary.json                 # Curated canonical skills & aliases
│   └── raw/
│       ├── resume_dataset.csv                    # Reference resume dataset
│       └── jd_dataset.csv                        # Reference job dataset (local)
├── src/
│   ├── app.py                                    # Streamlit web application
│   ├── extraction/
│   │   ├── document_parser.py                    # Format router (.pdf, .docx)
│   │   ├── pdf_parser.py                         # PyMuPDF text extractor
│   │   └── docx_parser.py                        # python-docx paragraph/table extractor
│   └── nlp/
│       ├── preprocessing.py                      # Normalization & symbol preservation
│       ├── skill_extractor.py                    # Dictionary phrase matcher & overlap filter
│       └── matching.py                           # TF-IDF & Set-theoretic gap engine
└── tests/                                        # Automated regression test suite (64 tests)
```

---

## Installation & Setup

1. **Clone or open the repository**:
   ```bash
   cd "Resume Project"
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   # Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Application

Launch the Streamlit web server:
```bash
streamlit run src/app.py
```
Open **`http://localhost:8501`** in your browser.

To run the automated regression tests:
```bash
pytest -v
```

---

## How to Use the Application

1. **Upload Resume**: Select a text-based resume file in `.pdf` or `.docx` format.
2. **Enter Job Description**: Paste the target job posting or technical requirements into the text area.
3. **Analyze**: Click the **Analyze Resume** button.
4. **Review Results**:
   - **Overall Match Score**: Textual similarity percentage based on TF-IDF cosine geometry across the entire vocabulary.
   - **Skill Coverage**: Percentage of required job skills satisfied by the candidate's resume.
   - **Matched Skills**: Technical skills found in both the resume and the job description ($Resume \cap Job$).
   - **Missing Skills**: Explicit qualifications required by the job that are absent from the resume ($Job \setminus Resume$).
   - **Additional Skills**: Extra candidate qualifications not specifically required by the job.

---

## Scoring Metrics Explained

- **Overall Match Score (Lexical Similarity)**:  
  Documents are converted into numerical term vectors using **TF-IDF**. The cosine of the angle between the vectors is calculated:
  $$\text{Cosine Similarity} = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \|\mathbf{B}\|} \times 100$$
  This reflects general technical and contextual vocabulary overlap.

- **Skill Coverage (Set Theoretic Ratio)**:  
  Calculated using exact set theory based on recognized canonical skills:
  $$\text{Skill Coverage} = \frac{|\text{Matched Skills}|}{|\text{Job Skills}|} \times 100$$
  If no recognized skills are present in the job description, the coverage safely defaults to $0.0\%$.

---

## Known Limitations

1. **Lexical, Not Semantic**: TF-IDF measures statistical word overlap. It does not map latent conceptual synonyms (e.g., "predictive modeling" will not match "machine learning" unless the exact tokens appear).
2. **Dictionary-Bound Extraction**: Skill tagging relies on the curated vocabulary in `data/processed/skill_dictionary.json`. Tools not listed in the dictionary are still evaluated in the overall TF-IDF score, but will not appear as discrete skill pills.
3. **Scanned Documents (No OCR)**: The current version extracts digital text layers. Image-only or scanned PDFs without embedded text are detected and flagged with an informative error; OCR (e.g., Tesseract) is planned for future iterations.
