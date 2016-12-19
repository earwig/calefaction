<%inherit file="_default.mako"/>
<div id="welcome">
    <p><em>Hi, ${g.auth.get_character_prop("name")}!</em></p>
    % for paragraph in g.config.get("welcome").split("\n\n"):
        <p>${paragraph.replace("\n", " ")}</p>
    % endfor
</div>
