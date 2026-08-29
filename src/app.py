import streamlit as st
import pandas as pd
import tempfile
import os

from src.extraction.document_parser import parse_document
from src.nlp.preprocessing import TextPreprocessor
from src.nlp.skill_extractor import SkillExtractor
from src.nlp.matching import MatchingEngine

# Configure the Streamlit page
st.set_page_config(
    page_title="Resume Skill Gap Analyzer",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    st.title("About the Project")
    st.write("""
    This application is an academic **Resume Skill Gap Analyzer** utilizing Natural Language Processing (NLP).
    
    ### Methodology
    1. **Text Extraction**: Reads PDF/DOCX.
    2. **NLP Preprocessing**: Normalizes text while preserving technical symbols (e.g., C++, .NET).
    3. **Skill Extraction**: Matches text against a curated technical vocabulary using overlapping span detection.
    4. **TF-IDF & Cosine Similarity**: Measures statistical lexical similarity.
    5. **Set Mathematics**: Calculates explicit skill gap coverage.
    """)
    st.divider()
    st.caption("Developed for Phase 7 of the PBL Lifecycle.")

# --- Main Page Header ---
st.title("🎓 Resume Skill Gap Analyzer using NLP")
st.markdown("Analyze how well a candidate's resume matches a job description, mathematically calculating textual similarity and extracting concrete skill gaps.")

# --- Inputs Section ---
st.subheader("1. Input Data")

uploaded_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
job_description_text = st.text_area("Job Description", height=200, placeholder="Paste the target job description here...")

st.write("") # Spacer
analyze_button = st.button("Analyze Resume", type="primary", use_container_width=True)

# --- Processing & Results ---
if analyze_button:
    # 1. Validations
    if not uploaded_file:
        st.error("Please upload a resume file.")
    elif not job_description_text.strip():
        st.error("Please provide a job description.")
    else:
        with st.spinner("Analyzing text and calculating mathematics..."):
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
                
                # --- RESULTS DASHBOARD ---
                st.success("Analysis Complete!")
                st.subheader("2. Analysis Results")
                
                m1, m2, m3, m4 = st.columns(4)
                
                m1.metric(
                    label="Overall Match Score", 
                    value=f"{match_results['similarity_score']}%",
                    help="Measures textual similarity between the resume and job description using TF-IDF and Cosine Similarity."
                )
                
                m2.metric(
                    label="Skill Coverage", 
                    value=f"{match_results['skill_coverage']}%",
                    help="Measures the percentage of recognized job skills that are also present in the resume."
                )
                
                m3.metric(
                    label="Matched Skills",
                    value=len(match_results['matched_skills'])
                )
                
                m4.metric(
                    label="Missing Skills",
                    value=len(match_results['missing_skills'])
                )
                
                st.divider()
                
                # Detailed Skill Lists
                list_col1, list_col2 = st.columns(2)
                
                with list_col1:
                    st.markdown("### 🟢 Matched Skills")
                    if match_results['matched_skills']:
                        for skill in match_results['matched_skills']:
                            st.markdown(f"- ✓ **{skill}**")
                    else:
                        st.info("No matching required skills found.")
                        
                    st.markdown("### 🔵 Additional Resume Skills")
                    if match_results['additional_skills']:
                        st.caption("Candidate possesses these technical skills not explicitly requested:")
                        st.markdown(", ".join(match_results['additional_skills']))
                    else:
                        st.caption("None.")
                        
                with list_col2:
                    st.markdown("### 🔴 Missing Skills")
                    if match_results['missing_skills']:
                        for skill in match_results['missing_skills']:
                            st.markdown(f"- ⚠ **{skill}**")
                    else:
                        if len(match_results['job_skills']) > 0:
                            st.success("Perfect! No required skills are missing.")
                        else:
                            st.info("Skill coverage cannot be meaningfully calculated because no recognized technical skills were found in the job description.")

                st.divider()
                
                # Visualization
                st.subheader("3. Skill Gap Visualization")
                
                chart_data = pd.DataFrame({
                    "Skill Category": ["Matched Skills", "Missing Skills", "Additional Skills"],
                    "Count": [
                        len(match_results['matched_skills']),
                        len(match_results['missing_skills']),
                        len(match_results['additional_skills'])
                    ]
                })
                chart_data.set_index("Skill Category", inplace=True)
                st.bar_chart(chart_data)

                # --- NLP TRANSPARENCY SECTION ---
                with st.expander("🔬 How the Analysis Works & Technical Details"):
                    st.markdown("""
                    ### How the scores are calculated
                    **Overall Match Score**: 
                    The raw text is filtered of grammatical stop words (like 'and', 'the'). We then convert the remaining vocabulary into mathematical vectors using **TF-IDF**. Finally, we calculate the angle between the resume's vector and the job description's vector using **Cosine Similarity**. A high score means the documents use very similar domain vocabulary.
                    
                    **Skill Coverage**:
                    Using a handcrafted technical vocabulary and phrase-matching engine, we explicitly detect canonical skills. We use standard set mathematics (Intersection) to find exactly which required tools the candidate possesses.
                    """)
                    
                    st.write("---")
                    st.markdown("**Extracted Resume Skills (Canonical):**")
                    st.json(match_results["resume_skills"])
                    
                    st.markdown("**Extracted Job Skills (Canonical):**")
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
