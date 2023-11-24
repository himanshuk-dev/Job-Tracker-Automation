import os

from typing import Optional, Tuple

from dotenv import load_dotenv

from utils.constants import Constants
from utils.errors import EnvironmentNotSetError


def get_springboard_credentials_from_env() -> Tuple[str, str]:
    """
    Gets the Springboard username and password from the .env file.
    Raises an EnvironmentNotSetError if either the username or password is not set.

    @Raises: EnvironmentNotSetError if either the username or password is not set.
    @Return: A tuple of strings containing the Springboard username and password.
    """
    load_dotenv()
    username: Optional[str] = os.getenv(Constants.SPRINGBOARD_EMAIL)
    password: Optional[str] = os.getenv(Constants.SPRINGBOARD_PASSWORD)

    if any(
        cred is None or cred == Constants.EMPTY_STRING for cred in {username, password}
    ):
        raise EnvironmentNotSetError(
            "Please set your Springboard username and password in the .env file."
        )

    return username, password
