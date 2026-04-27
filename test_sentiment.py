import pytest
from project3 import SentimentAnalyzer

def test_sentiment_analyzer_classification(monkeypatch):
    """
    Test SentimentAnalyzer.analyze() by mocking Ollama response to avoid real API call.
    """

    # Mock ollama.generate to always return a "positive" sentiment
    def mock_generate(model, prompt):
        return {'response': 'Positive'}

    from project3 import ollama  # Import here to patch
    monkeypatch.setattr(ollama, 'generate', mock_generate)

    analyzer = SentimentAnalyzer(model='llama3.2')
    result = analyzer.analyze("The stock market surged 5% today")

    assert isinstance(result, str)
    assert result == "positive"

def test_sentiment_analyzer_error_handling(monkeypatch):
    """
    Test SentimentAnalyzer.analyze() returns an error string starting with
    'error:' when ollama.generate raises an Exception.
    """

    def mock_generate_error(model, prompt):
        raise Exception("Connection refused")

    from project3 import ollama
    monkeypatch.setattr(ollama, 'generate', mock_generate_error)

    analyzer = SentimentAnalyzer(model='llama3.2')
    result = analyzer.analyze("Test headline")

    assert isinstance(result, str)
    assert result.startswith("error:")
