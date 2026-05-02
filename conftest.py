"""
Pytest configuration and fixtures
Shared fixtures for all tests
"""

import pytest
import sys
import os
from unittest.mock import MagicMock, patch

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))


@pytest.fixture
def mock_groq_client():
    """Mock Groq client for testing"""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Mocked Groq response"
    mock_client.chat.completions.create.return_value = mock_response
    return mock_client


@pytest.fixture
def mock_vectorstore():
    """Mock FAISS vectorstore for testing"""
    mock_vs = MagicMock()
    mock_vs.similarity_search.return_value = [
        MagicMock(page_content="Referensi 1: Test content"),
        MagicMock(page_content="Referensi 2: More test content"),
    ]
    return mock_vs


@pytest.fixture
def sample_data():
    """Sample data for testing"""
    return {
        "halo": "Halo, ada yang bisa saya bantu?",
        "apa itu ai": "AI adalah kecerdasan buatan.",
        "apa itu machine learning": "Machine learning adalah cabang AI.",
        "apa itu iot": "IoT adalah Internet of Things.",
    }


@pytest.fixture
def clear_cache():
    """Clear response cache before test"""
    from responses import _response_cache, _response_cache_time
    _response_cache.clear()
    _response_cache_time.clear()
    yield
    _response_cache.clear()
    _response_cache_time.clear()


@pytest.fixture
def mock_env_with_api_key():
    """Mock environment with Groq API key"""
    with patch.dict(os.environ, {'GROQ_API_KEY': 'gsk_test_123_abc'}):
        yield


@pytest.fixture
def mock_env_without_api_key():
    """Mock environment without Groq API key"""
    with patch.dict(os.environ, {}, clear=True):
        yield
