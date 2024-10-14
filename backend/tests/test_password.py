import pytest

from fastapi import HTTPException

from backend.api_v1.users.passwords import PasswordsChecker


@pytest.mark.password
def test_check_passwords():
    string1 = 'some_string'
    string2 = 'some_string'
    correct = PasswordsChecker(
        password_1=string1,
        password_2=string2,
    ).get_password()

    assert bool(correct)


@pytest.mark.password
def test_duck_passwords():
    string1 = 'not_some_string'
    string2 = 'some_string'

    with pytest.raises(HTTPException) as ex:
        PasswordsChecker(
            password_1=string1,
            password_2=string2,
        ).get_password()
    assert ex.value.detail == {'passwords': 'Differents passwords'}
