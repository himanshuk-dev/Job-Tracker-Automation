import os

from contextlib import contextmanager
from typing import Dict

import pytest

from utils.errors import EnvironmentNotSetError
from utils.helpers import get_springboard_credentials_from_env


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
        "SPRINGBOARD_EMAIL": "test_username",
        "SPRINGBOARD_PASSWORD": "test_password",
    }

    with mock_env_vars(**mock_env):
        username, password = get_springboard_credentials_from_env()
        assert username == "test_username"
        assert password == "test_password"


def test_get_springboard_creds_from_env_raises_error() -> None:
    """
    Tests that the get_springboard_credentials_from_env function raises an
    EnvironmentNotSetError when the username or password is not set in the .env file.
    """

    # Override the value in the .env file for SPRINGBOARD_PASSWORD
    mock_env: Dict[str, str] = {
        "SPRINGBOARD_EMAIL": "test_username",
        "SPRINGBOARD_PASSWORD": "",
    }

    with mock_env_vars(**mock_env):
        with pytest.raises(EnvironmentNotSetError) as e:
            get_springboard_credentials_from_env()

    assert str(e.value) == (
        "Please set your Springboard username and password in the .env file."
    )

    assert e.type == EnvironmentNotSetError
