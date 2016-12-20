<%inherit file="_base.mako"/>
<%block name="lefthead">
    ${parent.lefthead()}
    <nav class="aligned">
        Campaign: XYZ | Map | Intel | Members...
    </nav>
</%block>
<%block name="righthead">
    <img id="character-portrait" class="aligned" title="${g.auth.get_character_prop('name')}" alt="" src="${g.eve.image.character(g.auth.get_character_id(), 256)}"/>
    <span id="character-summary" class="aligned">
        ${g.auth.get_character_prop("name")}
        <span class="sep">[</span><a id="logout" title="Log out" href="${url_for('logout')}">log out</a><span class="sep">]</span>
    </span>
</%block>
${next.body()}
