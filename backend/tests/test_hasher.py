import pytest

from backend.hashers import PasswordHashCheker, PasswordHasher


@pytest.mark.hashers
class TestHashers:
    """
    Тесты хэширования
    """
    
    def test_hash_str(self):
        string = 'somesting'
        hasher = PasswordHasher(password=string).get_hashed_password()
        assert type(hasher) == bytes

    def test_some_hash(self):
        string = 'somesting'
        hasher = PasswordHasher(password=string).get_hashed_password()
        is_some = PasswordHashCheker(password=string,
                                     hash_password=hasher,
                                     ).is_correct()
        assert is_some

    def test_not_some_hash(self):
        string = 'somesting'
        enather = 'enather'
        hasher = PasswordHasher(password=string).get_hashed_password()
        is_some = PasswordHashCheker(password=enather,
                                     hash_password=hasher,
                                     ).is_correct()
        assert not is_some
