def test_app_imports_successfully():
    """
    Regression test to ensure the Streamlit application can be imported
    without throwing ModuleNotFoundError or similar import exceptions.
    This verifies that all internal paths used by the UI are correct.
    """
    try:
        import src.app
    except ImportError as e:
        import pytest
        pytest.fail(f"Failed to import src.app due to an ImportError: {e}")

import pytest
from streamlit.testing.v1 import AppTest
import pymupdf
import os

def test_image_only_pdf_error_message(tmp_path):
    """
    Verifies that uploading an image-only (or empty) PDF triggers the
    graceful, user-friendly error message in the Streamlit UI, instead
    of crashing with a raw traceback.
    """
    # 1. Create a truly empty PDF
    pdf_path = tmp_path / "empty.pdf"
    doc = pymupdf.open()
    doc.new_page() # Just an empty page, no text
    doc.save(str(pdf_path))
    doc.close()
    
    # 2. Run Streamlit AppTest
    app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "app.py"))
    at = AppTest.from_file(app_path)
    at.run()
    
    assert not at.exception, "App should load without exceptions"
    
    # 3. Fill inputs
    at.text_area[0].input("Looking for a Python developer").run()
    with open(str(pdf_path), "rb") as f:
        file_content = f.read()
    
    # We simulate uploading a file using the upload() method available in Streamlit AppTest
    at.file_uploader[0].upload(str(pdf_path), file_content).run()
    
    # 4. Click Analyze Resume
    at.button[0].click().run()
    
    # 5. Assert the friendly error message is shown and NO uncaught exception occurred
    assert not at.exception, "App should handle the empty PDF gracefully without crashing."
    
    # The error should be rendered via st.error
    found_error = False
    for el in at.error:
        if "Unable to extract text from this resume." in el.value:
            found_error = True
            break
            
    assert found_error, "The graceful error message for image-only PDFs was not displayed."
