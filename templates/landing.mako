<%inherit file="_layout.mako"/>
<%block name="lefthead">
    <a href="/">
        <img id="corp-masthead" class="aligned" src="${g.eve.image.corp(g.config.get('corp.id'), 256)}"/>
    </a>
    <a href="/" class="aligned">${g.config.get("corp.name")}</a>
</%block>
<%block name="righthead">
    <img id="login-button" class="aligned" src="${url_for('staticv', filename='images/eve-login.png')}"/>
</%block>
<p>Hello, world!</p>
