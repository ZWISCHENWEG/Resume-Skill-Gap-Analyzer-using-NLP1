import pytest
from src.nlp.preprocessing import TextPreprocessor

@pytest.fixture
def preprocessor():
    return TextPreprocessor()

def test_empty_input(preprocessor):
    result = preprocessor.preprocess("")
    assert result["original_text"] == ""
    assert result["cleaned_text"] == ""
    assert result["tokens"] == []
    assert result["filtered_tokens"] == []

    result_none = preprocessor.preprocess(None)
    assert result_none["original_text"] == ""
    assert result_none["cleaned_text"] == ""
    assert result_none["tokens"] == []
    assert result_none["filtered_tokens"] == []

def test_whitespace_normalization(preprocessor):
    text = "   This   has\nmultiple\ttabs and   spaces.  "
    result = preprocessor.preprocess(text)
    assert result["cleaned_text"] == "this has multiple tabs and spaces"
    assert result["tokens"] == ["this", "has", "multiple", "tabs", "and", "spaces"]

def test_lowercase_conversion(preprocessor):
    text = "MIXED Case TEXT"
    result = preprocessor.preprocess(text)
    assert result["cleaned_text"] == "mixed case text"

def test_tokenization(preprocessor):
    text = "token one two"
    result = preprocessor.preprocess(text)
    assert result["tokens"] == ["token", "one", "two"]

def test_stop_word_handling(preprocessor):
    text = "this is a test of the preprocessor"
    result = preprocessor.preprocess(text)
    
    # "this", "is", "a", "of", "the" should be in tokens but NOT in filtered_tokens
    assert "this" in result["tokens"]
    assert "this" not in result["filtered_tokens"]
    assert "is" in result["tokens"]
    assert "is" not in result["filtered_tokens"]
    assert "the" in result["tokens"]
    assert "the" not in result["filtered_tokens"]
    
    assert "test" in result["filtered_tokens"]
    assert "preprocessor" in result["filtered_tokens"]

def test_general_punctuation_handling(preprocessor):
    text = "Hello, world! This is a test (and it's working) [right]? Yes: indeed;"
    result = preprocessor.preprocess(text)
    assert result["cleaned_text"] == "hello world this is a test and it s working right yes indeed"

def test_technical_punctuation_c_plus_plus(preprocessor):
    text = "Experienced in C++ development."
    result = preprocessor.preprocess(text)
    assert "c++" in result["tokens"]
    assert "c++" in result["filtered_tokens"]

def test_technical_punctuation_c_sharp(preprocessor):
    text = "Looking for a C# developer"
    result = preprocessor.preprocess(text)
    assert "c#" in result["tokens"]
    assert "c#" in result["filtered_tokens"]

def test_technical_punctuation_dot_net(preprocessor):
    text = "Experience with .NET framework"
    result = preprocessor.preprocess(text)
    assert ".net" in result["tokens"]
    assert ".net" in result["filtered_tokens"]

def test_technical_punctuation_node_js(preprocessor):
    text = "Node.js backend developer."
    result = preprocessor.preprocess(text)
    assert "node.js" in result["tokens"]
    assert "node.js" in result["filtered_tokens"]

def test_technical_punctuation_next_js(preprocessor):
    text = "Frontend in Next.js"
    result = preprocessor.preprocess(text)
    assert "next.js" in result["tokens"]

def test_technical_punctuation_react_js(preprocessor):
    text = "React.js is great"
    result = preprocessor.preprocess(text)
    assert "react.js" in result["tokens"]

def test_technical_punctuation_ci_cd(preprocessor):
    text = "Set up CI/CD pipelines"
    result = preprocessor.preprocess(text)
    assert "ci/cd" in result["tokens"]

def test_technical_punctuation_asp_net(preprocessor):
    text = "Working with ASP.NET Core"
    result = preprocessor.preprocess(text)
    assert "asp.net" in result["tokens"]

def test_technical_punctuation_scikit_learn(preprocessor):
    text = "Machine learning with scikit-learn"
    result = preprocessor.preprocess(text)
    assert "scikit-learn" in result["tokens"]

def test_multi_word_technical_phrases(preprocessor):
    text = "Machine Learning and Artificial Intelligence"
    result = preprocessor.preprocess(text)
    # The tokens should be individually lowercased and clean
    assert "machine" in result["tokens"]
    assert "learning" in result["tokens"]
    # The cleaned_text preserves the space
    assert "machine learning and artificial intelligence" in result["cleaned_text"]
    
def test_realistic_resume_sentence(preprocessor):
    text = "Experienced Python developer with Node.js, C++, React.js and CI/CD experience."
    result = preprocessor.preprocess(text)
    assert "node.js" in result["tokens"]
    assert "c++" in result["tokens"]
    assert "react.js" in result["tokens"]
    assert "ci/cd" in result["tokens"]
    assert "python" in result["tokens"]
    
    assert "with" in result["tokens"]
    assert "with" not in result["filtered_tokens"]
    assert "and" in result["tokens"]
    assert "and" not in result["filtered_tokens"]

def test_realistic_job_description_sentence(preprocessor):
    text = "Requirements: 5+ years of software engineering, proficient in Java, Spring Boot, and AWS."
    result = preprocessor.preprocess(text)
    assert "java" in result["tokens"]
    assert "spring" in result["tokens"]
    assert "boot" in result["tokens"]
    assert "aws" in result["tokens"]
    # Verify the colon and comma were removed
    assert "requirements" in result["tokens"]

def test_deterministic_repeated_processing(preprocessor):
    text = "Test processing. Node.js is great!"
    result1 = preprocessor.preprocess(text)
    result2 = preprocessor.preprocess(text)
    assert result1 == result2
