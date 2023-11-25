from typing import NamedTuple


class SpringboardCredentials(NamedTuple):
    """
    A named tuple containing the Springboard email and password.
    Can be called with dot notation to get the values, e.g.:

    credentials = SpringboardCredentials(email, password)
    credentials.email
    credentials.password
    """

    email: str
    password: str
