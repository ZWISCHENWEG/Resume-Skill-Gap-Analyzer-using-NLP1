import docx

def extract_text_from_docx(filepath: str) -> str:
    """
    Extracts text from a DOCX document, including paragraphs and tables.
    
    Args:
        filepath (str): The path to the DOCX file.
        
    Returns:
        str: The extracted text.
        
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file cannot be opened, parsed, or contains no extractable text.
    """
    text_content = []
    
    try:
        doc = docx.Document(filepath)
        
        # Extract paragraph text
        for para in doc.paragraphs:
            if para.text.strip():
                text_content.append(para.text.strip())
                
        # Extract table text
        for table in doc.tables:
            for row in table.rows:
                row_data = []
                for cell in row.cells:
                    if cell.text.strip():
                        row_data.append(cell.text.strip())
                if row_data:
                    text_content.append(" | ".join(row_data))
                    
        extracted_text = "\n".join(text_content).strip()
        
        if not extracted_text:
            raise ValueError(f"No extractable text found in '{filepath}'. "
                             "The DOCX might be empty.")
                             
        return extracted_text
        
    except FileNotFoundError:
        raise
    except Exception as e:
        if isinstance(e, ValueError) and "No extractable text found" in str(e):
            raise
        raise ValueError(f"Failed to parse DOCX '{filepath}': {e}")
