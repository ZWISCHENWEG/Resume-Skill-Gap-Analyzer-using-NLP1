import re
import nltk
from typing import Dict, List, Any

class TextPreprocessor:
    """
    Handles deterministic NLP preprocessing of raw text for the Skill Gap Analyzer.
    
    This preprocessor is specifically designed to safely handle technical terminology
    by preserving punctuation that is commonly part of tech skills (e.g., C++, Node.js, .NET).
    """

    def __init__(self):
        # Ensure NLTK stopwords are available
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords', quiet=True)
            
        from nltk.corpus import stopwords
        self.stop_words = set(stopwords.words('english'))

    def _selective_punctuation_removal(self, text: str) -> str:
        """
        Removes general punctuation but preserves technical symbols.
        """
        # 1. Replace general grammatical punctuation with space
        # We target: , ; : ( ) [ ] { } " ' ! ? < > |
        # We also replace tabs and newlines with spaces here or later.
        text = re.sub(r'[\\,;:\(\)\[\]\{\}\"\'!\?<>|]', ' ', text)
        
        # 2. Handle periods (.) carefully.
        # Remove periods that are followed by a space or end of string (sentence enders).
        text = re.sub(r'\.(?=\s|$)', ' ', text)
        
        # Replace period preceded by whitespace and followed by whitespace (isolated periods).
        text = re.sub(r'(?<=\s)\.(?=\s)', ' ', text)
        
        # Note: Periods embedded (Node.js) or preceded by space but followed by word (.NET) remain intact.
        
        # 3. Handle trailing punctuation on words that should be clean (like `-` at the end of a word).
        # We will just strip leading/trailing hyphens from words safely by normalizing space around them if they are isolated.
        # But `C++` and `C#` are fine since they are symbols.
        
        return text

    def _normalize_whitespace(self, text: str) -> str:
        """
        Reduces all whitespace (tabs, newlines, multiple spaces) to a single space.
        """
        # Replace newlines, tabs, and carriage returns with space
        text = re.sub(r'[\r\n\t]+', ' ', text)
        # Collapse multiple spaces into one and strip leading/trailing spaces
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def preprocess(self, raw_text: str) -> Dict[str, Any]:
        """
        Executes the full preprocessing pipeline on the raw text.
        
        Args:
            raw_text (str): The raw string extracted from a document.
            
        Returns:
            Dict containing:
            - original_text: The untouched string.
            - cleaned_text: Lowercased, selectively stripped of punctuation, and space-normalized.
            - tokens: List of tokens derived from cleaned_text (retains stop words).
            - filtered_tokens: List of tokens with standard stop words removed.
        """
        if not raw_text or not isinstance(raw_text, str) or not raw_text.strip():
            return {
                "original_text": raw_text if raw_text is not None else "",
                "cleaned_text": "",
                "tokens": [],
                "filtered_tokens": []
            }

        # 1. Lowercase normalization
        lowercased = raw_text.lower()
        
        # 2. Punctuation handling
        punct_handled = self._selective_punctuation_removal(lowercased)
        
        # 3. Whitespace normalization
        cleaned_text = self._normalize_whitespace(punct_handled)
        
        # 4. Tokenization
        # Simple whitespace split
        tokens = cleaned_text.split(' ') if cleaned_text else []
        
        # 5. Stop-word filtering
        # We keep tokens that are NOT in the stop word list.
        filtered_tokens = [token for token in tokens if token not in self.stop_words]
        
        return {
            "original_text": raw_text,
            "cleaned_text": cleaned_text,
            "tokens": tokens,
            "filtered_tokens": filtered_tokens
        }
