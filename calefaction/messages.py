# -*- coding: utf-8  -*-

__all__ = ["Messages"]

class Messages:
    """Namespace for user interface message strings."""
    # success
    LOGGED_IN = "Logged in."
    LOGGED_OUT = "Logged out."

    # error
    LOG_IN_FIRST = "You need to log in to access that page."
    ACCESS_DENIED = "Your character is not permitted to access this site."
    SESSION_EXPIRED = "Session expired. You need to log in again."
    LOGIN_FAILED = "Login failed."
    EVE_API_ERROR = ("There was an error communicating with EVE's servers. "
                     "Please wait a while and try again.")
