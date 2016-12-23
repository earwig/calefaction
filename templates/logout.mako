<%inherit file="_base.mako"/>
<%block name="title">
    Log out &ndash; ${g.config.get("corp.name") | h}
</%block>
<h2>Log out</h2>
<p>Use the button below to safely log out and clear your session.</p>
<form id="logout-form" method="post">
    <input type="submit" value="Log out">
</form>
