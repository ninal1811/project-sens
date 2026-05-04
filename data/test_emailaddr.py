import pytest
import data.emailaddr as em

TEST_EMAIL = 'user@example.com'


def test_abc_base():
    with pytest.raises(TypeError):
        em.Email(TEST_EMAIL)


def test_construct_standard_email():
    email = em.StandardEmail(TEST_EMAIL)
    assert isinstance(email, em.StandardEmail)


def test_construct_standard_email_bad_type():
    with pytest.raises(TypeError):
        em.StandardEmail(42)


def test_construct_standard_email_space():
    with pytest.raises(ValueError):
        em.StandardEmail(em.TEST_EMAIL_SPACE)


def test_construct_standard_email_no_at():
    with pytest.raises(ValueError):
        em.StandardEmail(em.TEST_EMAIL_NO_AT)
