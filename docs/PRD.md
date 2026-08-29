# Resume Skill Gap Analyzer using NLP
## Product Requirements Document (PRD)

### 1. Project Overview
An NLP-based system designed to analyze uploaded student resumes against target job descriptions. The system aims to identify key missing skills and bridge the gap between candidate qualifications and employer expectations. This is an academic Problem-Based Learning (PBL) project for the Python for Data Science subject.

### 2. Problem Statement
Students often struggle to identify the specific skills they lack when applying for technical job roles. This gap between current qualifications and employer expectations leads to lower hiring rates. A programmatic, data-driven approach is needed to analyze resumes against job descriptions to highlight matched and missing skills.

### 3. Target Users
- **College Students/Candidates**: Looking to evaluate their resume against target job roles and identify specific areas for improvement (skill gaps).
- **Academic Evaluators (Professors)**: Evaluating the system as a demonstration of Python, Data Science, and NLP concepts.

### 4. Goals
- Efficiently extract text from unstructured resumes (PDF/DOCX).
- Apply NLP techniques to extract key skills and technical terms.
- Compute a similarity/match score between the resume and job requirements.
- Automate the identification of missing technical skills.
- **Evaluate the system's accuracy** by testing against manually verified examples.

### 5. Functional Requirements
- **FR1**: The system must allow users to upload a resume in PDF or DOCX format.
- **FR2**: The system must accept a target job description (via text input or dataset selection).
- **FR3**: The system must extract and clean text from the uploaded resume.
- **FR4**: The system must identify and extract technical skills from both the resume and the job description using a curated, extensible vocabulary and phrase matching.
- **FR5**: The system must calculate an overall similarity score (%) between the resume and job description using TF-IDF and Cosine Similarity.
- **FR6**: The system must output a list of "Matched Skills" based on explicit skill extraction.
- **FR7**: The system must output a list of "Missing Skills" (Skill Gap) calculated as `Job Skills - Resume Skills`.
- **FR8**: The system must display the results in a user-friendly web interface.

### 6. Acceptance Criteria (Finalized)
1. **[MET]** Can ingest a PDF or DOCX file and successfully extract English text.
2. **[MET]** Implements NLP text preprocessing (tokenization, stop-word removal, lowercasing) without relying on heavy external models like GPT.
3. **[MET]** Identifies technical skills from a pre-defined or extracted list and normalizes them (e.g., matching ReactJS to React).
4. **[MET]** Computes a mathematical matching score (Similarity Score) between the Resume and the Job Description using TF-IDF + Cosine Similarity.
5. **[MET]** Computes explicit Skill Coverage using exact set mathematics and displays Missing Skills.
6. **[MET]** Provides a local Streamlit dashboard to upload files and view results clearly without exposing raw Python outputs.
7. **[MET]** Explains its analytical choices clearly in an academic format.
8. **[MET]** All core functional requirements (FR1-FR8) are implemented and validated.

### 7. Non-Functional Requirements
- **Performance**: Text extraction and NLP processing should complete within a few seconds.
- **Explainability**: The NLP matching logic must be modular and explainable for academic review.
- **Robustness**: The system must handle poor formatting, empty files, and unsupported formats gracefully.
- **Deterministic**: The analysis must produce consistent results for the same resume and job description.

### 7. Inputs
- Candidate Resume (PDF or DOCX file).
- Target Job Description (Text).

### 8. Outputs
- Resume Extraction Status.
- Target Job Information summary.
- Overall Match Percentage (%).
- Matched Skills (List).
- Missing Skills (List).
- Explanatory visual summaries of the skill gap.

### 9. Core Features (MVP Scope)
- File Upload & Text Extraction.
- Text Preprocessing Pipeline.
- **Curated Skill Extraction Engine** (Dictionary, Phrase Matching, Normalization).
- **Vectorization & Matching Engine** (TF-IDF & Cosine Similarity).
- **Skill Gap Analysis Logic** (Set Differences).
- Interactive Dashboard UI.

### 10. Out of Scope
- User Authentication / Accounts.
- Database storage of user resumes.
- Payment systems or premium features.
- Cloud microservices architecture.
- Complex generative AI features that act as "black boxes" without explanation.

### 11. Success Criteria
- The system correctly extracts readable text from standard academic resumes.
- The system accurately identifies technical skills when tested against manually verified, ground-truth examples.
- The skill gap analysis accurately reflects the set difference between required skills and resume skills.
- The application runs locally without crashing on edge-case inputs.

### 12. Limitations
- Skill extraction accuracy depends on the underlying vocabulary and aliases.
- PDF extraction may struggle with highly graphical or multi-column resumes.
