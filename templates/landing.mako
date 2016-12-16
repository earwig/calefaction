<%inherit file="_base.mako"/>
<%block name="righthead">
    <img id="login-button" class="aligned" src="${url_for('staticv', filename='images/eve-login.png')}"/>
</%block>
<div id="welcome">
    % for paragraph in g.config.get("welcome").split("\n\n"):
        <p>${paragraph.replace("\n", " ")}</p>
    % endfor
</div>
