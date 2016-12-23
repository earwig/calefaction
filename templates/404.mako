<%inherit file="_base.mako"/>
<%block name="title">
    404 &ndash; ${g.config.get("corp.name") | h}
</%block>
<h2>Error 404</h2>
<p>The page you asked for couldn't be found.</p>
