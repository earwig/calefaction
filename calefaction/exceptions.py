# -*- coding: utf-8  -*-

"""
This module contains exceptions for Calefaction.

+-- CalefactionError
    +-- AccessDeniedError
    +-- EVEAPIError
        +-- EVEAPIForbiddenError
"""

class CalefactionError(RuntimeError):
    """Base exception class for errors within Calefaction."""
    pass

class AccessDeniedError(CalefactionError):
    """The user tried to do something they don't have permission for."""
    pass

class EVEAPIError(CalefactionError):
    """Represents (generally external) errors while using the EVE APIs."""
    pass

class EVEAPIForbiddenError(EVEAPIError):
    """We tried to make an API request that we don't have permission for."""
    pass
