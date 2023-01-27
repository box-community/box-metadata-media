# project/tests/test_info.py

from tests.conftest import get_settings_override

def test_info_tests_config(test_app):
    """Should return the same configurations as set on project/tests/conftest.py"""
    response = test_app.get("/info")
    
    assert response.status_code == 200
    assert response.json() == get_settings_override().dict()