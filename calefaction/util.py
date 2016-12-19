# -*- coding: utf-8  -*-

from functools import wraps
from hashlib import md5
from os import path
from traceback import format_exc

from flask import flash, url_for
from flask_mako import render_template, TemplateError

from .exceptions import AccessDeniedError, EVEAPIError
from .messages import Messages

__all__ = [
    "try_func", "make_error_catcher", "make_route_restricter",
    "set_up_asset_versioning"]

def try_func(inner):
    """Evaluate inner(), catching subclasses of CalefactionError.

    If nothing was caught, return (inner(), False). Otherwise, flash an
    appropriate error message and return (False, True).
    """
    try:
        result = inner()
        return (result, False)
    except EVEAPIError:
        flash(Messages.EVE_API_ERROR, "error")
        return (False, True)
    except AccessDeniedError:
        flash(Messages.ACCESS_DENIED, "error")
        return (False, True)

def make_error_catcher(app, error_template):
    """Wrap a route to display and log any uncaught exceptions."""
    def callback(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except TemplateError as exc:
                app.logger.error("Caught exception:\n{0}".format(exc.text))
                return render_template(error_template, traceback=exc.text)
            except Exception:
                app.logger.exception("Caught exception:")
                return render_template(error_template, traceback=format_exc())
        return inner
    return callback

def make_route_restricter(auth, on_failure):
    """Wrap a route to ensure the user is authenticated."""
    def callback(func):
        @wraps(func)
        def inner(*args, **kwargs):
            success, caught = try_func(auth.is_authenticated)
            if success:
                return func(*args, **kwargs)
            if not caught:
                flash(Messages.LOG_IN_FIRST, "error")
            return on_failure()
        return inner
    return callback

def set_up_asset_versioning(app):
    """Add a staticv endpoint that adds hash versioning to static assets."""
    def callback(app, error, endpoint, values):
        if endpoint == "staticv":
            filename = values["filename"]
            fpath = path.join(app.static_folder, filename)
            try:
                mtime = path.getmtime(fpath)
            except OSError:
                return url_for("static", filename=filename)
            cache = app._hash_cache.get(fpath)
            if cache and cache[0] == mtime:
                hashstr = cache[1]
            else:
                with open(fpath, "rb") as fp:
                    hashstr = md5(fp.read()).hexdigest()
                app._hash_cache[fpath] = (mtime, hashstr)
            return url_for("static", filename=filename, v=hashstr)
        raise error

    app._hash_cache = {}
    app.url_build_error_handlers.append(lambda a, b, c: callback(app, a, b, c))
