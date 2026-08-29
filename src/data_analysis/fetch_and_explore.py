import pandas as pd
import urllib.request
import os
import re
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

os.makedirs('data/raw', exist_ok=True)

resume_urls = [
    'https://raw.githubusercontent.com/gauravduttakiit/Resume-Screening/master/UpdatedResumeDataSet.csv',
    'https://raw.githubusercontent.com/anukalp-mishra/Resume-Screening/master/resume_dataset.csv'
]

jd_urls = [
    'https://raw.githubusercontent.com/Mlawrence95/LinkedIn-Tech-Job-Data/main/jobs.csv',
    'https://raw.githubusercontent.com/binoydutt/Resume-Job-Description-Matching/main/data.csv'
]

def download_and_explore(urls, name):
    df = None
    for url in urls:
        try:
            print(f"Trying to download {name} from {url}...")
            df = pd.read_csv(url)
            print(f"Success! Downloaded {name} from {url}")
            df.to_csv(f'data/raw/{name}.csv', index=False)
            break
        except Exception as e:
            print(f"Failed: {e}")
            
    if df is not None:
        print(f"\n--- {name.upper()} DATASET EXPLORATION ---")
        print(f"Shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        print("\nMissing Values:")
        print(df.isnull().sum())
        print("\nDuplicates:", df.duplicated().sum())
        print("-" * 50)
        return df
    else:
        print(f"Could not download any {name} dataset.")
        return None

def extract_potential_skills(text_series):
    print("Extracting potential skills/keywords to analyze vocabulary...")
    # Very naive word frequency to see what technical terms pop up
    all_text = " ".join(text_series.dropna().astype(str)).lower()
    words = re.findall(r'\b[a-z\+\#\.]{2,}\b', all_text)
    # Filter common stop words manually for this quick check
    stop_words = set(["the", "and", "to", "of", "a", "in", "for", "is", "on", "that", "by", "this", "with", "i", "you", "it", "not", "or", "be", "are", "from", "at", "as", "your"])
    words = [w for w in words if w not in stop_words]
    
    counter = Counter(words)
    print("Top 50 words (excluding basic stop words):")
    print(counter.most_common(50))
    print("-" * 50)

if __name__ == "__main__":
    resume_df = download_and_explore(resume_urls, 'resume_dataset')
    if resume_df is not None:
        if 'Resume' in resume_df.columns:
            extract_potential_skills(resume_df['Resume'])
        
    jd_df = download_and_explore(jd_urls, 'jd_dataset')
    if jd_df is not None:
        # Assuming there is a description column, check common names
        desc_col = None
        for col in ['Job Description', 'Description', 'description', 'job_description']:
            if col in jd_df.columns:
                desc_col = col
                break
        if desc_col:
            extract_potential_skills(jd_df[desc_col])
