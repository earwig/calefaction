<%inherit file="_base.mako"/>
<%block name="lefthead">
    ${parent.lefthead()}
    <nav class="aligned">
        Campaign: XYZ | Map | Intel | Members...
    </nav>
</%block>
<%block name="righthead">
    <img id="character-portrait" class="aligned" title="${g.auth.get_character_prop('name')}" alt="" src="${g.eve.image.character(g.auth.get_character_id(), 256)}"/>
    <span class="aligned">
        ${g.auth.get_character_prop("name")}
        [<a title="Log out" href="${url_for('logout')}">logout</a>]  <!-- ... JS switch to a POST form -->
    </span>
</%block>
${next.body()}
