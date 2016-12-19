# -*- coding: utf-8  -*-

class CalefactionError(RuntimeError):
    """Base exception class for errors within Calefaction."""
    pass

class EVEAPIError(CalefactionError):
    """Represents (generally external) errors while using the EVE APIs."""
    pass

class AccessDeniedError(CalefactionError):
    """The user tried to do something they don't have permission for."""
    pass
