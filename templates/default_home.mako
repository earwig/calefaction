<%inherit file="_default.mako"/>
<p>Hi, ${g.auth.get_character_prop("name") | h}!</p>
