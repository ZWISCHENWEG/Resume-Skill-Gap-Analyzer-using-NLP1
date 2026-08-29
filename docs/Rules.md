# Development Rules & Guidelines

### 1. Python 3.14 Compatibility & Dependency Rules
- **Do NOT blindly install packages**. Before adding a dependency to `requirements.txt`, verify that it is fully compatible with Python 3.14.2.
- Only install necessary libraries required for the scope. Do not bloat the project with unused data science tools.

### 2. Coding Standards
- Follow PEP 8 guidelines.
- Write modular code: separate UI logic from business/data logic.
- Use clear, descriptive variable and function names with Python type hints.

### 3. Clear Distinction of Analysis Types
The system MUST NOT mix the implementation of overall similarity and skill gap analysis:
- **Overall Similarity** = TF-IDF Vectorization + Cosine Similarity.
- **Skill Gap Detection** = Explicit Skill Extraction + Set Operations (Job Skills - Resume Skills).

### 4. NLP & AI Boundaries
- **Primary Skill Extraction**: Must be driven by a curated, extensible technical skill vocabulary, normalization, and phrase matching.
- **Generic NER**: Should NOT be blindly trusted to find technical skills. If used, it must be supplementary and explainable.
- **Generative AI APIs**: STRICTLY PROHIBITED for core matching logic (e.g., no OpenAI/GPT queries to find skills or calculate scores).

### 5. Error Handling & Validation
- Validate file extensions (.pdf, .docx).
- Handle unsupported file types or corrupted documents gracefully without application crashes.
- Handle edge cases where document text is empty (e.g. image-only PDFs lacking OCR).

### 6. Testing & Evaluation Rules
- Write automated tests for text extraction, similarity computation, and set mathematics.
- **Evaluation Requirement**: The skill extraction system MUST be tested against manually verified examples (ground-truth). Report evaluation results (precision/recall where practical) to prove the system works, rather than just claiming it does.

### 7. Documentation Rules
- Maintain these `/docs` files as the absolute source of truth.
- Update `Tasks.md`, `Memory.md`, and `Decisions.md` continuously. No silent architectural changes.
