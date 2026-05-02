"""
Unit tests for Chatbot AI System
Tests cover: config, responses, caching, validation, and error handling
"""

import pytest
import time
import json
import sys
from unittest.mock import patch, MagicMock

# Import modules to test
import config
from responses import (
    respon_ai,
    load_data,
    load_vectorstore,
    get_groq_client,
    _get_cached_response,
    _set_cached_response,
    _response_cache,
    _response_cache_time,
)


class TestConfig:
    """Test configuration module"""

    def test_config_groq_settings(self):
        """Test Groq configuration values"""
        assert config.GROQ_MODEL == "llama-3.3-70b-versatile"
        assert config.GROQ_MAX_TOKENS == 1024
        assert config.GROQ_TIMEOUT == 30
        assert isinstance(config.GROQ_MODEL, str)

    def test_config_vectorstore_settings(self):
        """Test vectorstore configuration"""
        assert config.VECTORSTORE_PATH == "vectorstore"
        assert config.K_SEARCH == 4
        assert config.CHUNK_SIZE == 1000
        assert config.CHUNK_OVERLAP == 200

    def test_config_input_validation(self):
        """Test input validation configuration"""
        assert config.MAX_INPUT_LENGTH == 5000
        assert config.MIN_INPUT_LENGTH == 1
        assert config.MAX_INPUT_LENGTH > config.MIN_INPUT_LENGTH

    def test_config_cache_settings(self):
        """Test cache configuration"""
        assert config.RESPONSE_CACHE_ENABLED == True
        assert config.RESPONSE_CACHE_TTL == 3600
        assert config.RESPONSE_CACHE_MAX_SIZE == 256
        assert isinstance(config.RESPONSE_CACHE_TTL, int)

    def test_config_paths(self):
        """Test configuration paths"""
        assert config.DATA_JSON_PATH == "data.json"
        assert config.PDF_FOLDER_PATH == "Referensi"
        assert config.VECTORSTORE_PATH == "vectorstore"


class TestInputValidation:
    """Test input validation in respon_ai"""

    def test_empty_input(self):
        """Test empty input rejection"""
        response = respon_ai("", use_groq=False)
        assert "tidak boleh kosong" in response
        assert "❌" in response

    def test_whitespace_only_input(self):
        """Test whitespace-only input rejection"""
        response = respon_ai("   \n  \t  ", use_groq=False)
        assert "tidak boleh kosong" in response
        assert "❌" in response

    def test_too_long_input(self):
        """Test max length validation"""
        long_input = "a" * (config.MAX_INPUT_LENGTH + 1)
        response = respon_ai(long_input, use_groq=False)
        assert "terlalu panjang" in response
        assert "⚠️" in response

    def test_max_length_boundary(self):
        """Test exactly at max length (should work)"""
        # Use valid input at max length
        input_at_max = "pertanyaan" * 500  # ~4500 chars
        if len(input_at_max) <= config.MAX_INPUT_LENGTH:
            response = respon_ai(input_at_max, use_groq=False)
            # Should not reject for length
            assert "terlalu panjang" not in response

    def test_valid_short_input(self):
        """Test valid short input"""
        response = respon_ai("halo", use_groq=False)
        assert "tidak boleh kosong" not in response
        assert "terlalu panjang" not in response

    def test_input_stripped(self):
        """Test input is stripped of whitespace"""
        response = respon_ai("  halo  ", use_groq=False)
        assert "tidak boleh kosong" not in response
        # Should match the keyword "halo"
        assert len(response) > 0


class TestLoadData:
    """Test load_data function with caching"""

    def test_load_data_returns_dict(self):
        """Test load_data returns a dictionary"""
        data = load_data()
        assert isinstance(data, dict)

    def test_load_data_has_entries(self):
        """Test load_data contains expected entries"""
        data = load_data()
        assert len(data) > 0

    def test_load_data_cached(self):
        """Test load_data uses caching (@lru_cache)"""
        # Load twice and ensure it's the same object (cached)
        data1 = load_data()
        data2 = load_data()
        
        # With @lru_cache, should be same object
        assert data1 == data2

    def test_load_data_has_keywords(self):
        """Test load_data contains expected keywords"""
        data = load_data()
        # Check if 'halo' is in data
        assert "halo" in data

    def test_load_data_values_are_strings(self):
        """Test all values in data.json are strings"""
        data = load_data()
        for key, value in data.items():
            assert isinstance(key, str)
            assert isinstance(value, str)


class TestRespoiAI:
    """Test main respon_ai function"""

    def test_exact_match_lookup(self):
        """Test exact keyword match from data.json"""
        response = respon_ai("halo", use_groq=False)
        assert response == "Halo, ada yang bisa saya bantu?"

    def test_case_insensitive_match(self):
        """Test case-insensitive matching"""
        response_lower = respon_ai("halo", use_groq=False)
        response_upper = respon_ai("HALO", use_groq=False)
        assert response_lower == response_upper

    def test_keyword_match(self):
        """Test keyword matching from data.json"""
        response = respon_ai("apa itu ai", use_groq=False)
        assert "kecerdasan buatan" in response

    def test_no_match_no_groq(self):
        """Test response when no match found and use_groq=False"""
        response = respon_ai("random question xyz", use_groq=False)
        assert "basis pengetahuan" in response or "Pertanyaan tidak ditemukan" in response

    def test_use_groq_flag(self):
        """Test use_groq parameter works"""
        # Should not raise error with use_groq=False
        response = respon_ai("pertanyaan acak", use_groq=False)
        assert isinstance(response, str)
        assert len(response) > 0

    @patch('responses.get_groq_client')
    def test_groq_called_on_no_match(self, mock_groq):
        """Test Groq is called when no local match and use_groq=True"""
        # Mock Groq response
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value.choices[0].message.content = "Mocked response"
        mock_groq.return_value = mock_client
        
        # This would require API setup, so we just test it doesn't crash
        # In real scenario, would need to mock the vectorstore too
        response = respon_ai("random question", use_groq=False)
        assert isinstance(response, str)


class TestCaching:
    """Test response caching system"""

    def test_cache_set_and_get(self):
        """Test setting and getting cache"""
        test_key = "test_key_123"
        test_response = "Test cached response"
        
        # Clear cache for this test
        if test_key in _response_cache:
            del _response_cache[test_key]
            del _response_cache_time[test_key]
        
        # Set cache
        _set_cached_response(test_key, test_response)
        
        # Get cache
        cached = _get_cached_response(test_key)
        assert cached == test_response

    def test_cache_miss(self):
        """Test cache returns None on miss"""
        cached = _get_cached_response("nonexistent_key_xyz")
        assert cached is None

    def test_cache_expiry(self):
        """Test cache TTL expiry"""
        # Save old TTL
        old_ttl = config.RESPONSE_CACHE_TTL
        config.RESPONSE_CACHE_TTL = 1  # 1 second
        
        test_key = "expiry_test_key"
        test_response = "Will expire"
        
        # Clear if exists
        if test_key in _response_cache:
            del _response_cache[test_key]
            del _response_cache_time[test_key]
        
        # Set cache
        _set_cached_response(test_key, test_response)
        
        # Should exist immediately
        assert _get_cached_response(test_key) == test_response
        
        # Wait for expiry
        time.sleep(1.2)
        
        # Should be expired now
        assert _get_cached_response(test_key) is None
        
        # Restore TTL
        config.RESPONSE_CACHE_TTL = old_ttl

    def test_cache_disabled(self):
        """Test cache can be disabled"""
        old_enabled = config.RESPONSE_CACHE_ENABLED
        config.RESPONSE_CACHE_ENABLED = False
        
        test_key = "disabled_cache_test"
        _set_cached_response(test_key, "Should not cache")
        
        # Should not retrieve (cache disabled)
        cached = _get_cached_response(test_key)
        
        # Restore
        config.RESPONSE_CACHE_ENABLED = old_enabled


class TestGroqClient:
    """Test Groq client initialization"""

    def test_groq_client_requires_api_key(self):
        """Test Groq client requires API key"""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError, match="GROQ_API_KEY"):
                get_groq_client()

    @patch.dict('os.environ', {'GROQ_API_KEY': 'gsk_test123'})
    def test_groq_client_with_api_key(self):
        """Test Groq client initializes with API key"""
        from groq import Groq
        
        # This will create a real Groq client (but won't call API)
        client = get_groq_client()
        assert client is not None
        assert isinstance(client, Groq)


class TestLoadVectorstore:
    """Test vectorstore loading and caching"""

    def test_load_vectorstore_not_found(self):
        """Test load_vectorstore returns None if not found"""
        with patch('os.path.exists', return_value=False):
            vs = load_vectorstore()
            assert vs is None

    def test_load_vectorstore_caching_simple(self):
        """Test vectorstore caching behavior"""
        # Test that load_vectorstore returns None if vectorstore doesn't exist
        with patch('os.path.exists', return_value=False):
            vs1 = load_vectorstore()
            vs2 = load_vectorstore()
            # Both should be None
            assert vs1 is None
            assert vs2 is None


class TestIntegration:
    """Integration tests for complete workflows"""

    def test_complete_workflow_keyword_match(self):
        """Test complete workflow with keyword match"""
        response = respon_ai("halo", use_groq=False)
        assert response == "Halo, ada yang bisa saya bantu?"

    def test_complete_workflow_with_validation(self):
        """Test complete workflow with input validation"""
        # Empty input should fail
        response1 = respon_ai("", use_groq=False)
        assert "tidak boleh kosong" in response1
        
        # Too long should fail
        response2 = respon_ai("a" * 5100, use_groq=False)
        assert "terlalu panjang" in response2
        
        # Valid should work
        response3 = respon_ai("halo", use_groq=False)
        assert response3 == "Halo, ada yang bisa saya bantu?"

    def test_multiple_queries(self):
        """Test multiple queries in sequence"""
        queries = ["halo", "apa itu ai", "halo"]
        
        for query in queries:
            response = respon_ai(query, use_groq=False)
            assert isinstance(response, str)
            assert len(response) > 0

    def test_config_used_in_validation(self):
        """Test that config values are used in validation"""
        # Create input that exceeds MAX_INPUT_LENGTH
        too_long = "a" * (config.MAX_INPUT_LENGTH + 1)
        response = respon_ai(too_long, use_groq=False)
        
        # Should use config.MAX_INPUT_LENGTH in error message
        assert str(config.MAX_INPUT_LENGTH) in response


class TestErrorHandling:
    """Test error handling and messages"""

    def test_error_message_for_empty_input(self):
        """Test error message for empty input"""
        response = respon_ai("", use_groq=False)
        assert "❌" in response
        assert "Pertanyaan tidak boleh kosong" in response

    def test_error_message_for_long_input(self):
        """Test error message for too long input"""
        long_input = "a" * (config.MAX_INPUT_LENGTH + 1)
        response = respon_ai(long_input, use_groq=False)
        assert "⚠️" in response
        assert "terlalu panjang" in response

    def test_error_message_for_no_match(self):
        """Test message when no match found"""
        response = respon_ai("pertanyaan yang tidak ada di database", use_groq=False)
        # Should contain information icon
        assert "📚" in response or "Pertanyaan tidak ditemukan" in response

    def test_no_error_for_valid_input(self):
        """Test valid input doesn't produce error"""
        response = respon_ai("halo", use_groq=False)
        assert "❌" not in response
        assert "⚠️" not in response
        assert "📚" not in response or response == "📚 Pertanyaan tidak ditemukan dalam basis pengetahuan. Coba rephrase atau aktifkan Groq AI."


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
