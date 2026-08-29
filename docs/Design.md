# UI/UX Design Specification

### 1. UI Structure
The application will be built using Streamlit, featuring a clean, single-page dashboard layout.

**Sidebar**:
- Application Title and Logo.
- File Uploader (PDF / DOCX) for Resume.
- Text Area / File Uploader for Target Job Description.
- "Analyze" Button to trigger the pipeline.
- About / Methodology section (for academic explanation).

**Main Area**:
- **Section 1: Summary**
  - High-level metric cards: Overall Match Score (%), Total Resume Skills, Total Job Skills.
- **Section 2: Skill Gap Analysis**
  - Matched Skills (Green badges/tags).
  - Missing Skills (Red/Orange badges/tags).
- **Section 3: Visualizations**
  - A chart (e.g., Radar chart or Bar chart) comparing skills present vs missing.
- **Section 4: Extracted Data (Collapsible)**
  - Expandable sections to view the raw extracted resume text and cleaned text, demonstrating the NLP pipeline process.

### 2. Typography & Colors
- **Framework Defaults**: Utilize Streamlit's default typography (sans-serif) for academic cleanliness.
- **Colors**:
  - Success/Match: Green (#28a745)
  - Missing/Gap: Red/Orange (#dc3545 / #fd7e14)
  - Primary UI Elements: Blue / Default Streamlit theme.

### 3. UX Principles
- **Feedback**: Show a loading spinner during document processing and NLP extraction.
- **Error States**: Display clear warning banners if a document cannot be read or if no skills are found.
- **Clarity**: Avoid dense text blobs in the results. Use tags, pills, and metrics for quick scannability.
- **Academic Transparency**: Include tooltips or subheaders explaining *how* a score was calculated (e.g., "Calculated using TF-IDF and Cosine Similarity").
