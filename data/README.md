# Dataset Directory

This directory stores datasets used for vocabulary generation, testing, and evaluation of the Resume Skill Gap Analyzer.

## Structure
- `raw/`: Contains original, unmodified datasets fetched from public repositories.
- `processed/`: (Future use) Contains datasets after cleaning and filtering.

## Datasets
1. **Resume Dataset (`raw/resume_dataset.csv`)**
   - **Original Source**: Kaggle's "UpdatedResumeDataSet"
   - **Download Mirror**: GitHub repository (`anukalp-mishra/Resume-Screening`)
   - **Size**: 169 records
   - **Columns**: `Category`, `Resume`
   - **Usage**: Used to identify common skill patterns in candidate profiles and to sample ground-truth evaluation resumes.

2. **Job Description Dataset (`raw/jd_dataset.csv`)**
   - **Original Source**: LinkedIn Tech Job Data (originally scraped and hosted on Kaggle)
   - **Download Mirror**: GitHub repository (`Mlawrence95/LinkedIn-Tech-Job-Data`)
   - **Size**: 8261 records
   - **Columns**: `title`, `description`, `Industries`, `location`, etc.
   - **Usage**: Used to identify target job requirements, build the technical skill vocabulary, and sample ground-truth evaluation job descriptions.
