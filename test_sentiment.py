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
