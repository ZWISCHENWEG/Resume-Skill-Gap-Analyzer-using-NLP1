import os
import sys
from pathlib import Path

# Ensure project root is in sys.path so imports work regardless of launch directory
ROOT_DIR = str(Path(__file__).resolve().parent.parent)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st
import pandas as pd
import altair as alt
import tempfile

from src.extraction.document_parser import parse_document
from src.nlp.preprocessing import TextPreprocessor
from src.nlp.skill_extractor import SkillExtractor
from src.nlp.matching import MatchingEngine

# Configure the Streamlit page
st.set_page_config(
    page_title="Resume Skill Gap Analyzer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- AWWWARDS-GRADE MINIMAL OBSIDIAN DESIGN SYSTEM ---
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* Global Reset & Base */
html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    background-color: #080c14 !important;
    color: #f1f5f9 !important;
}

/* Hide Streamlit default header decoration */
header[data-testid="stHeader"] {
    background: transparent !important;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background-color: #0b0f19 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
}
[data-testid="stSidebar"] .block-container {
    padding-top: 2rem !important;
}

/* Hero Section */
.hero-wrapper {
    margin-bottom: 2.2rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}
.hero-tag {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 5px 12px;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 9999px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #94a3b8;
    margin-bottom: 1rem;
}
.hero-tag-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background-color: #10b981;
    display: inline-block;
}
.hero-title {
    font-size: 2.4rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1.15;
    color: #ffffff;
    margin: 0 0 0.6rem 0;
}
.hero-title span {
    color: #94a3b8;
    font-weight: 400;
}
.hero-subtitle {
    font-size: 0.98rem;
    color: #94a3b8;
    line-height: 1.6;
    max-width: 780px;
    margin: 0;
}

/* Section Labels */
.section-marker {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 2rem 0 1rem 0;
}
.section-number {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    font-weight: 600;
    color: #64748b;
    letter-spacing: 0.05em;
}
.section-title {
    font-size: 1.1rem;
    font-weight: 700;
    letter-spacing: -0.01em;
    color: #f8fafc;
    margin: 0;
}

/* Input Fields */
.stTextArea textarea {
    background-color: #0d121d !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 10px !important;
    color: #f8fafc !important;
    font-size: 0.9rem !important;
    line-height: 1.5 !important;
    transition: all 0.2s ease !important;
}
.stTextArea textarea:focus {
    border-color: rgba(255, 255, 255, 0.25) !important;
    box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.15) !important;
}

/* File Uploader */
[data-testid="stFileUploader"] section {
    background-color: #0d121d !important;
    border: 1px dashed rgba(255, 255, 255, 0.12) !important;
    border-radius: 10px !important;
    transition: border-color 0.2s ease !important;
}
[data-testid="stFileUploader"] section:hover {
    border-color: rgba(255, 255, 255, 0.25) !important;
}

/* Refined Primary Button (Monochrome Luxury - No Neon) */
.stButton > button {
    background: #f8fafc !important;
    color: #090d16 !important;
    border: 1px solid rgba(255, 255, 255, 0.9) !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    letter-spacing: 0.01em !important;
    padding: 0.65rem 1.6rem !important;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3) !important;
}
.stButton > button:hover {
    background: #ffffff !important;
    color: #000000 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(255, 255, 255, 0.12) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* Bento Metric Cards */
[data-testid="stMetric"] {
    background: #0f1422 !important;
    border: 1px solid rgba(255, 255, 255, 0.07) !important;
    border-radius: 12px !important;
    padding: 18px 22px !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25) !important;
    transition: border-color 0.2s ease, transform 0.2s ease !important;
}
[data-testid="stMetric"]:hover {
    border-color: rgba(255, 255, 255, 0.14) !important;
    transform: translateY(-2px) !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.76rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    color: #94a3b8 !important;
}
[data-testid="stMetricValue"] {
    font-size: 2.1rem !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    letter-spacing: -0.02em !important;
}

/* Skill Container & Badges */
.card-panel {
    background: #0f1422;
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 12px;
    padding: 20px;
    height: 100%;
}
.card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 14px;
}
.card-title {
    font-size: 0.88rem;
    font-weight: 700;
    letter-spacing: 0.02em;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 0;
}
.card-count {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    padding: 2px 8px;
    border-radius: 6px;
    background: rgba(255, 255, 255, 0.05);
    color: #94a3b8;
}

.pill-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}
.pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 0.82rem;
    font-weight: 500;
    line-height: 1;
    transition: all 0.15s ease;
}
.pill:hover {
    transform: translateY(-1px);
}
.pill-matched {
    background: rgba(16, 185, 129, 0.09);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.22);
}
.pill-missing {
    background: rgba(244, 63, 94, 0.09);
    color: #fb7185;
    border: 1px solid rgba(244, 63, 94, 0.22);
}
.pill-additional {
    background: rgba(148, 163, 184, 0.08);
    color: #cbd5e1;
    border: 1px solid rgba(148, 163, 184, 0.18);
}
.pill-empty-state {
    color: #64748b;
    font-size: 0.85rem;
    font-style: italic;
    padding: 4px 0;
}

/* Success Toast */
.status-toast {
    display: flex;
    align-items: center;
    gap: 10px;
    background: rgba(16, 185, 129, 0.08);
    border: 1px solid rgba(16, 185, 129, 0.2);
    color: #34d399;
    padding: 10px 16px;
    border-radius: 8px;
    font-size: 0.85rem;
    font-weight: 500;
    margin-bottom: 1.5rem;
}

/* Expander Transparency */
[data-testid="stExpander"] {
    background: #0f1422 !important;
    border: 1px solid rgba(255, 255, 255, 0.07) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}
[data-testid="stExpander"] summary {
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    color: #cbd5e1 !important;
    padding: 14px 18px !important;
}

/* Sidebar Info Blocks */
.sidebar-card {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 8px;
    padding: 14px;
    margin-bottom: 12px;
}
.sidebar-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #64748b;
    margin-bottom: 6px;
}
.sidebar-val {
    font-size: 0.85rem;
    color: #e2e8f0;
    line-height: 1.4;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Initialize Backend Modules once
@st.cache_resource
def load_nlp_modules():
    return {
        "preprocessor": TextPreprocessor(),
        "extractor": SkillExtractor(),
        "engine": MatchingEngine()
    }

modules = load_nlp_modules()
preprocessor = modules["preprocessor"]
extractor = modules["extractor"]
engine = modules["engine"]

# --- Sidebar ---
with st.sidebar:
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <div style="font-size: 1rem; font-weight: 700; color: #ffffff; letter-spacing: -0.01em;">System Architecture</div>
        <div style="font-size: 0.76rem; color: #64748b; margin-top: 2px;">PBL Academic NLP Specification</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-card">
        <div class="sidebar-label">01 / Ingestion Layer</div>
        <div class="sidebar-val">PyMuPDF (fitz) & python-docx with context managers. Rejects scans without OCR.</div>
    </div>
    
    <div class="sidebar-card">
        <div class="sidebar-label">02 / Tokenization & Cleaning</div>
        <div class="sidebar-val">Selective punctuation retention preserving C++, C#, .NET, Node.js. NLTK stop-words.</div>
    </div>
    
    <div class="sidebar-card">
        <div class="sidebar-label">03 / Skill Extraction</div>
        <div class="sidebar-val">Curated dictionary with regex lookaheads <code>(?<!\\w)</code> and case-sensitive matching for C & R.</div>
    </div>
    
    <div class="sidebar-card">
        <div class="sidebar-label">04 / Mathematical Engine</div>
        <div class="sidebar-val">TF-IDF & Cosine Angle for lexical similarity. Discrete Set Theory for Skill Gaps.</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.06); font-size: 0.72rem; color: #475569;">
        Verified with 64 automated regression tests. Python 3.14 compatible.
    </div>
    """, unsafe_allow_html=True)

# --- Hero Header ---
st.markdown("""
<div class="hero-wrapper">
    <div class="hero-tag">
        <span class="hero-tag-dot"></span>
        Deterministic NLP Pipeline • Academic PBL
    </div>
    <h1 class="hero-title">Resume Skill Gap <span>Analyzer</span></h1>
    <p class="hero-subtitle">
        An explainable evaluation engine that calculates mathematical lexical overlap using TF-IDF cosine geometry and derives exact skill gaps through set-theoretic operations.
    </p>
</div>
""", unsafe_allow_html=True)

# --- Section 1: Inputs ---
st.markdown("""
<div class="section-marker">
    <span class="section-number">01</span>
    <span class="section-title">Document Inputs</span>
</div>
""", unsafe_allow_html=True)

col_file, col_jd = st.columns([1, 1], gap="medium")

with col_file:
    uploaded_file = st.file_uploader(
        "Upload Candidate Resume (PDF or DOCX)",
        type=["pdf", "docx"],
        help="Text-based documents only. Scanned images require OCR which is beyond current scope."
    )

with col_jd:
    job_description_text = st.text_area(
        "Target Job Description",
        height=165,
        placeholder="Paste technical requirements or full job description here..."
    )

st.write("")
analyze_button = st.button("Analyze Resume", type="primary", use_container_width=True)

# --- Section 2: Results & Processing ---
if analyze_button:
    # 1. Input Validations
    if not uploaded_file:
        st.error("Please upload a resume file.")
    elif not job_description_text.strip():
        st.error("Please provide a job description.")
    else:
        with st.spinner("Executing NLP pipeline and computing mathematical vector spaces..."):
            tmp_path = None
            try:
                # 2. Extract Text from Uploaded File
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name
                
                resume_text = parse_document(tmp_path)
                
                if not resume_text or not resume_text.strip():
                    st.error("We could not extract readable text from this document. It may be an image-only PDF.")
                    st.stop()
                
                # 3. NLP Pipeline
                res_pre = preprocessor.preprocess(resume_text)
                job_pre = preprocessor.preprocess(job_description_text)
                
                res_skills = extractor.extract_skills(res_pre)
                job_skills = extractor.extract_skills(job_pre)
                
                match_results = engine.calculate_match(res_pre, job_pre, res_skills, job_skills)
                
                # 4. Success Toast
                st.markdown("""
                <div class="status-toast">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                    Analysis complete. Vector metrics and skill sets compiled deterministically.
                </div>
                """, unsafe_allow_html=True)
                
                # --- METRICS DASHBOARD (Bento Grid) ---
                st.markdown("""
                <div class="section-marker">
                    <span class="section-number">02</span>
                    <span class="section-title">Evaluation Metrics</span>
                </div>
                """, unsafe_allow_html=True)
                
                m1, m2, m3, m4 = st.columns(4)
                
                m1.metric(
                    label="Overall Match Score",
                    value=f"{match_results['similarity_score']}%",
                    help="Lexical similarity between entire document vocabularies using TF-IDF and Cosine Angle."
                )
                
                m2.metric(
                    label="Skill Coverage",
                    value=f"{match_results['skill_coverage']}%",
                    help="Ratio of recognized job requirements possessed by candidate: |Matched| / |Job Skills|."
                )
                
                m3.metric(
                    label="Matched Skills",
                    value=len(match_results['matched_skills']),
                    help="Intersection of candidate skills and requested job skills."
                )
                
                m4.metric(
                    label="Missing Skills",
                    value=len(match_results['missing_skills']),
                    help="Set difference of requested job skills absent from resume."
                )
                
                st.write("")
                
                # --- SKILL PILLS BREAKDOWN ---
                col_match, col_miss, col_add = st.columns(3, gap="medium")
                
                with col_match:
                    matched_pills = "".join([
                        f'<span class="pill pill-matched">✓ {s}</span>'
                        for s in match_results['matched_skills']
                    ]) if match_results['matched_skills'] else '<span class="pill-empty-state">No matching technical skills found.</span>'
                    
                    st.markdown(f"""
                    <div class="card-panel">
                        <div class="card-header">
                            <span class="card-title" style="color: #34d399;">
                                <span style="width: 8px; height: 8px; border-radius: 50%; background: #10b981; display: inline-block;"></span>
                                Matched Skills
                            </span>
                            <span class="card-count">{len(match_results['matched_skills'])}</span>
                        </div>
                        <div class="pill-grid">
                            {matched_pills}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_miss:
                    missing_pills = "".join([
                        f'<span class="pill pill-missing">⚠ {s}</span>'
                        for s in match_results['missing_skills']
                    ]) if match_results['missing_skills'] else (
                        '<span class="pill-empty-state" style="color: #34d399;">Candidate possesses 100% of required skills.</span>'
                        if len(match_results['job_skills']) > 0 else
                        '<span class="pill-empty-state">No recognized technical skills found in Job Description.</span>'
                    )
                    
                    st.markdown(f"""
                    <div class="card-panel">
                        <div class="card-header">
                            <span class="card-title" style="color: #fb7185;">
                                <span style="width: 8px; height: 8px; border-radius: 50%; background: #f43f5e; display: inline-block;"></span>
                                Missing Skills
                            </span>
                            <span class="card-count">{len(match_results['missing_skills'])}</span>
                        </div>
                        <div class="pill-grid">
                            {missing_pills}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_add:
                    additional_pills = "".join([
                        f'<span class="pill pill-additional">+ {s}</span>'
                        for s in match_results['additional_skills']
                    ]) if match_results['additional_skills'] else '<span class="pill-empty-state">No additional candidate skills detected.</span>'
                    
                    st.markdown(f"""
                    <div class="card-panel">
                        <div class="card-header">
                            <span class="card-title" style="color: #94a3b8;">
                                <span style="width: 8px; height: 8px; border-radius: 50%; background: #64748b; display: inline-block;"></span>
                                Additional Skills
                            </span>
                            <span class="card-count">{len(match_results['additional_skills'])}</span>
                        </div>
                        <div class="pill-grid">
                            {additional_pills}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # --- VISUALIZATION: ALTAIR HORIZONTAL BAR CHART ---
                st.markdown("""
                <div class="section-marker">
                    <span class="section-number">03</span>
                    <span class="section-title">Distribution Visualization</span>
                </div>
                """, unsafe_allow_html=True)
                
                chart_df = pd.DataFrame({
                    "Category": ["Matched Skills", "Missing Skills", "Additional Skills"],
                    "Count": [
                        len(match_results['matched_skills']),
                        len(match_results['missing_skills']),
                        len(match_results['additional_skills'])
                    ],
                    "Color": ["#10b981", "#f43f5e", "#64748b"]
                })
                
                max_count = max(chart_df["Count"].max(), 1)
                
                altair_chart = (
                    alt.Chart(chart_df)
                    .mark_bar(cornerRadiusEnd=5, height=22)
                    .encode(
                        x=alt.X(
                            "Count:Q",
                            title=None,
                            scale=alt.Scale(domain=[0, max_count + 1]),
                            axis=alt.Axis(
                                tickMinStep=1,
                                gridColor="rgba(255, 255, 255, 0.05)",
                                domainColor="rgba(255, 255, 255, 0.1)",
                                labelColor="#64748b",
                                labelFont="JetBrains Mono"
                            )
                        ),
                        y=alt.Y(
                            "Category:N",
                            title=None,
                            sort=["Matched Skills", "Missing Skills", "Additional Skills"],
                            axis=alt.Axis(
                                labelColor="#cbd5e1",
                                labelFontSize=13,
                                labelFont="Plus Jakarta Sans",
                                labelFontWeight=500,
                                domain=False,
                                ticks=False
                            )
                        ),
                        color=alt.Color("Color:N", scale=None)
                    )
                    .properties(
                        height=160,
                        background="transparent"
                    )
                    .configure_view(strokeWidth=0)
                )
                
                st.altair_chart(altair_chart, width="stretch")
                
                # --- MATHEMATICAL TRANSPARENCY EXPANDER ---
                with st.expander("Mathematical Verification & Derivation Details"):
                    st.markdown("""
                    ### Theoretical Formulations
                    
                    **1. Overall Match Score (Cosine Similarity over TF-IDF space)**
                    $$\\text{Similarity}(\\mathbf{d}_{\\text{resume}}, \\mathbf{d}_{\\text{job}}) = \\frac{\\mathbf{d}_{\\text{resume}} \\cdot \\mathbf{d}_{\\text{job}}}{\\|\\mathbf{d}_{\\text{resume}}\\| \\|\\mathbf{d}_{\\text{job}}\\|} \\times 100$$
                    Measures the angular orientation of the two document vocabulary vectors after stripping grammatical stop-words.
                    
                    **2. Skill Coverage (Set Theoretic Ratio)**
                    $$\\text{Coverage} = \\frac{|S_{\\text{resume}} \\cap S_{\\text{job}}|}{|S_{\\text{job}}|} \\times 100$$
                    Quantifies the proportion of required technical skills satisfied by the candidate.
                    
                    **3. Missing Skills Gap**
                    $$\\text{Gap} = S_{\\text{job}} \\setminus S_{\\text{resume}}$$
                    Explicit actionable deficits required for job qualification.
                    """)
                    
                    st.markdown("---")
                    c_json1, c_json2 = st.columns(2)
                    with c_json1:
                        st.markdown("**Canonical Skills Extracted from Resume:**")
                        st.json(match_results["resume_skills"])
                    with c_json2:
                        st.markdown("**Canonical Skills Extracted from Job:**")
                        st.json(match_results["job_skills"])

            except ValueError as ve:
                if "No extractable text found" in str(ve):
                    st.error("Unable to extract text from this resume. The PDF appears to contain an image or scanned content. Please upload a text-based PDF or DOCX resume.")
                else:
                    st.error(f"Error parsing document: {ve}")
            except Exception as e:
                import traceback
                traceback.print_exc()
                st.error("An unexpected error occurred during processing. Please check the console logs or verify your input files.")
            finally:
                if tmp_path and os.path.exists(tmp_path):
                    try:
                        os.unlink(tmp_path)
                    except Exception:
                        pass
