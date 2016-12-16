<%inherit file="_base.mako"/>
<%block name="title">
    Error &ndash; ${g.config.get("corp.name") | h}
</%block>
<%block name="header"/>
<h1>Error!</h1>
<p>You may report the following information to the developers:</p>
<div id="error">
    <pre>${traceback | trim,h}</pre>
</div>
