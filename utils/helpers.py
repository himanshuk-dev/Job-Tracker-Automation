import logging
import os
import sys

from logging import Logger
from typing import Optional

from dotenv import load_dotenv

from utils.constants import Constants
from utils.errors import EnvironmentNotSetError
from utils.type_aliases import SpringboardCredentials


logging.basicConfig(
    format="%(levelname)s - %(asctime)s: %(message)s ",
    level=logging.INFO,
    stream=sys.stdout,
)

log: Logger = logging.getLogger(__name__)


def get_springboard_credentials_from_env() -> SpringboardCredentials:
    """
    Gets the Springboard email and password from the .env file.
    Raises an EnvironmentNotSetError if either the email or password is not set.

    @Raises: EnvironmentNotSetError if either the email or password is not set.
    @Return: A tuple of strings containing the Springboard email and password.
    """
    log.info("Getting Springboard credentials from .env file.")
    load_dotenv()
    email: Optional[str] = os.getenv(Constants.SPRINGBOARD_EMAIL)
    password: Optional[str] = os.getenv(Constants.SPRINGBOARD_PASSWORD)

    if any(
        cred is None or cred == Constants.EMPTY_STRING for cred in {email, password}
    ):
        raise EnvironmentNotSetError(
            "One or more of SPRINGBOARD_EMAIL or SPRINGBOARD_PASSWORD is not set in the .env file."
            f"The provided values are: Email: {email}, Password: {password}"
        )

    # Note: Logging this info here should be ok, because this will
    # be unique to each user running it on their local machine.
    log.info(
        "Successfully retrieved Springboard credentials from .env file. "
        f"Email: {email}, Password: {password}",
    )

    return SpringboardCredentials(email, password)
