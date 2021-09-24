from survey_api.utils import get_test

def test_get_test():
    test_library = get_test(0)
    assert isinstance(test_library, dict)