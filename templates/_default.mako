<%inherit file="_layout.mako"/>
<%block name="lefthead">
    <a href="/">
        <img id="corp-masthead" class="aligned" src="${g.eve.image.corp(g.config.get('corp.id'), 256)}"/>
    </a>
    <a href="/" class="aligned">${g.config.get("corp.name")}</a>
    <nav>
        Campaign: XYZ | Map | Intel | Members...
    </nav>
</%block>
<%block name="righthead">
    PLAYER_NAME... [logout]
</%block>
${next.body()}
