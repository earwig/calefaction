<%inherit file="_base.mako"/>
<%block name="lefthead">
    ${parent.lefthead()}
    <nav class="aligned">
        Campaign: XYZ | Map | Intel | Members...
    </nav>
</%block>
<%block name="righthead">
    <img id="character-portrait" class="styled-border aligned" alt="" src="${g.eve.image.character(g.auth.get_character_id(), 256)}"/>
    <div id="character-options" class="styled-border">
        <div id="style-options">
            % for style in g.config.get("style.enabled"):
                <form action="${url_for('set_style', style=style)}" method="post">
                    <input type="submit" title="${style.title()}" value="${style}" style="background-image: url('${url_for('staticv', filename='images/style/{}.png'.format(style))}')">
                </form>
            % endfor
        </div>
    </div>
    <span id="character-summary" class="aligned">
        ${g.auth.get_character_prop("name")}
        <span class="sep">[</span><a id="logout" title="Log out" href="${url_for('logout')}">log out</a><span class="sep">]</span>
    </span>
</%block>
${next.body()}
