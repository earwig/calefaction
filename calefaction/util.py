# -*- coding: utf-8  -*-

from functools import wraps
from hashlib import md5
from os import path
from traceback import format_exc

from flask import url_for
from flask_mako import render_template, TemplateError

__all__ = ["catch_errors", "set_up_asset_versioning"]

def catch_errors(app):
    """Wrap a route to display and log any uncaught exceptions."""
    def callback(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except TemplateError as exc:
                app.logger.error("Caught exception:\n{0}".format(exc.text))
                return render_template("error.mako", traceback=exc.text)
            except Exception:
                app.logger.exception("Caught exception:")
                return render_template("error.mako", traceback=format_exc())
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
                with open(fpath, "rb") as f:
                    hashstr = md5(f.read()).hexdigest()
                app._hash_cache[fpath] = (mtime, hashstr)
            return url_for("static", filename=filename, v=hashstr)
        raise error

    app._hash_cache = {}
    app.url_build_error_handlers.append(lambda a, b, c: callback(app, a, b, c))
