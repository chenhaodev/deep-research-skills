def test_pytest_works():
    """Verify pytest infrastructure is working"""
    assert 1 + 1 == 2


def test_fixtures_available(mock_qwen_client, temp_cache_db):
    """Verify fixtures are available"""
    assert mock_qwen_client is not None
    assert temp_cache_db is not None
