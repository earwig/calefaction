<%inherit file="_base.mako"/>
<%block name="righthead">
    <a href="${g.auth.make_login_link()}">
        <img id="login-button" class="aligned" title="Log in with EVE Online" alt="Log in with EVE Online" src="${url_for('staticv', filename='images/eve-login.png')}"/>
    </a>
</%block>
<div id="welcome">
    % for paragraph in g.config.get("welcome").split("\n\n"):
        <p>${paragraph.replace("\n", " ")}</p>
    % endfor
</div>
