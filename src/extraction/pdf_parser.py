import pymupdf

def extract_text_from_pdf(filepath: str) -> str:
    """
    Extracts raw text from a PDF document.
    
    Args:
        filepath (str): The path to the PDF file.
        
    Returns:
        str: The extracted text.
        
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file cannot be opened, parsed, or contains no extractable text.
    """
    text_content = []
    
    try:
        # Context manager ensures file is closed automatically
        with pymupdf.open(filepath) as doc:
            for page in doc:
                # get_text("text") returns text in a reasonably readable order
                text = page.get_text("text")
                if text:
                    text_content.append(text)
                    
        extracted_text = "\n".join(text_content).strip()
        
        # If no text was extracted, it might be an image-only PDF
        if not extracted_text:
            raise ValueError(f"No extractable text found in '{filepath}'. "
                             "The PDF might be empty or contain only images (OCR is not currently supported).")
            
        return extracted_text
        
    except FileNotFoundError:
        raise
    except Exception as e:
        if isinstance(e, ValueError) and "No extractable text found" in str(e):
            raise
        raise ValueError(f"Failed to parse PDF '{filepath}': {e}")
