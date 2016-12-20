import logging

__version__ = "0.1.dev0"
__release__ = "0.1"

baseLogger = logging.getLogger("calefaction")
del logging

def enable_logging():
    """Set up calefaction's logger to print out all logs to stderr."""
    import logging

    fmt = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"

    formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    baseLogger.addHandler(handler)
    baseLogger.setLevel(logging.DEBUG)
