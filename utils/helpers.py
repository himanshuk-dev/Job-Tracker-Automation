import logging
import os
import sys

from logging import Logger
from typing import Optional, Tuple

from dotenv import load_dotenv

from utils.constants import Constants
from utils.errors import EnvironmentNotSetError


logging.basicConfig(
    format="%(levelname)s - %(asctime)s: %(message)s ",
    level=logging.INFO,
    stream=sys.stdout,
)

log: Logger = logging.getLogger(__name__)


def get_springboard_credentials_from_env() -> Tuple[str, str]:
    """
    Gets the Springboard username and password from the .env file.
    Raises an EnvironmentNotSetError if either the username or password is not set.

    @Raises: EnvironmentNotSetError if either the username or password is not set.
    @Return: A tuple of strings containing the Springboard username and password.
    """
    log.info("Getting Springboard credentials from .env file.")
    load_dotenv()
    username: Optional[str] = os.getenv(Constants.SPRINGBOARD_EMAIL)
    password: Optional[str] = os.getenv(Constants.SPRINGBOARD_PASSWORD)

    if any(
        cred is None or cred == Constants.EMPTY_STRING for cred in {username, password}
    ):
        raise EnvironmentNotSetError(
            "One or more of SPRINGBOARD_EMAIL or SPRINGBOARD_PASSWORD is not set in the .env file."
            f"The provided values are: Username: {username}, Password: {password}"
        )

    # Note: Logging this info here should be ok, because this will
    # be unique to each user running it on their local machine.
    log.info(
        "Successfully retrieved Springboard credentials from .env file. "
        f"Username: {username}, Password: {password}",
    )

    return username, password
