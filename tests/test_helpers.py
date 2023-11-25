import os

from contextlib import contextmanager
from typing import Dict

import pytest

from utils.errors import EnvironmentNotSetError
from utils.helpers import get_springboard_credentials_from_env
from utils.type_aliases import SpringboardCredentials


@contextmanager
def mock_env_vars(**env_vars) -> None:
    """
    Context manager to temporarily set environment variables.
    At the end of the context manager, the environment variables are
    reset to their original values.

    @Param: **env_vars: A dictionary of environment variables to set.
    @Return: None
    """
    old_env: Dict[str, str] = os.environ.copy()
    os.environ.update(env_vars)
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(old_env)


def test_get_springboard_creds_from_env() -> None:
    """
    Tests that the get_springboard_credentials_from_env function returns the correct
    username and password when they are set in the .env file.
    """
    mock_env: Dict[str, str] = {
        "SPRINGBOARD_EMAIL": "test_email",
        "SPRINGBOARD_PASSWORD": "test_password",
    }

    with mock_env_vars(**mock_env):
        credentials = get_springboard_credentials_from_env()
        assert credentials.email == "test_email"
        assert credentials.password == "test_password"
        assert isinstance(credentials, SpringboardCredentials)


def test_get_springboard_creds_from_env_raises_error() -> None:
    """
    Tests that the get_springboard_credentials_from_env function raises an
    EnvironmentNotSetError when the email or password is not set in the .env file.
    """

    # Override the value in the .env file for SPRINGBOARD_PASSWORD
    mock_env: Dict[str, str] = {
        "SPRINGBOARD_EMAIL": "test_email",
        "SPRINGBOARD_PASSWORD": "",
    }

    with mock_env_vars(**mock_env):
        with pytest.raises(EnvironmentNotSetError) as e:
            get_springboard_credentials_from_env()

    assert str(e.value) == (
        "One or more of SPRINGBOARD_EMAIL or SPRINGBOARD_PASSWORD is not set in the .env file."
        "The provided values are: Email: test_email, Password: "
    )

    assert e.type == EnvironmentNotSetError
