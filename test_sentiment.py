import pytest
from project3 import SentimentAnalyzer

def test_sentiment_analyzer_classification(monkeypatch):
    """
    Test SentimentAnalyzer.analyze() by mocking Ollama response to avoid real API call.
    """

    # Mock ollama.generate to always return a "positive" sentiment
    def mock_generate(model, prompt, **kwargs):
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

    def mock_generate_error(model, prompt, **kwargs):
        raise Exception("Connection refused")

    from project3 import ollama
    monkeypatch.setattr(ollama, 'generate', mock_generate_error)

    analyzer = SentimentAnalyzer(model='llama3.2')
    result = analyzer.analyze("Test headline")

    assert isinstance(result, str)
    assert result.startswith("error:")

def _analyze_with_reply(monkeypatch, reply):
    from project3 import ollama
    captured = {}

    def mock_generate(model, prompt, **kwargs):
        captured.update(kwargs)
        return {'response': reply}

    monkeypatch.setattr(ollama, 'generate', mock_generate)
    return SentimentAnalyzer().analyze("Some headline"), captured


def test_label_clean_one_word_reply(monkeypatch):
    result, captured = _analyze_with_reply(monkeypatch, "  Negative\n")
    assert result == "negative"
    assert captured["options"] == {"temperature": 0}


def test_label_extracted_from_sentence(monkeypatch):
    result, _ = _analyze_with_reply(
        monkeypatch, "I would classify this headline as Neutral, since it only reports facts.")
    assert result == "neutral"


def test_label_missing_returns_unknown(monkeypatch):
    # "unpositive" must not count: labels match only as whole words
    result, _ = _analyze_with_reply(monkeypatch, "It is hard to say; somewhat unpositive.")
    assert result == "unknown"
