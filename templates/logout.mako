<%inherit file="_base.mako"/>
<%block name="title">
    Log out &ndash; ${g.config.get("corp.name") | h}
</%block>
<h1>Log out</h1>  <!-- ... style -->
<p>Use the button below to safely log out and clear your session.</p>
<form method="post">
    <input type="submit" value="Log out">
</form>
