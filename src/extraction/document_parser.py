import os
from .pdf_parser import extract_text_from_pdf
from .docx_parser import extract_text_from_docx

def parse_document(filepath: str) -> str:
    """
    Parses a supported document (.pdf, .docx) and returns the extracted raw text.
    
    Args:
        filepath (str): The path to the document file.
        
    Returns:
        str: The extracted raw text.
        
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file type is unsupported, empty, or cannot be parsed.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: '{filepath}'")
        
    _, ext = os.path.splitext(filepath)
    ext = ext.lower()
    
    if ext == '.pdf':
        return extract_text_from_pdf(filepath)
    elif ext == '.docx':
        return extract_text_from_docx(filepath)
    else:
        raise ValueError(f"Unsupported file format '{ext}'. Only .pdf and .docx are supported.")
