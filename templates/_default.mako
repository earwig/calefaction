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
            <% cur_style = g.auth.get_character_prop("style") or g.config.get("style.default") %>
            % for style in g.config.get("style.enabled"):
                <%
                    stitle = style.title()
                    url = url_for('staticv', filename='images/style/{}.png'.format(style))
                %>
                % if style == cur_style:
                    <div class="cur">
                        <div style="background-image: url('${url}')">${stitle}</div>
                    </div>
                % else:
                    <form action="${url_for('set_style', style=style)}" method="post">
                        <input type="submit" title="${stitle}" value="${stitle}" style="background-image: url('${url}')">
                    </form>
                % endif
            % endfor
        </div>
    </div>
    <span id="character-summary" class="aligned">
        ${g.auth.get_character_prop("name")}
        <span class="sep">[</span><a id="logout" title="Log out" href="${url_for('logout')}">log out</a><span class="sep">]</span>
    </span>
</%block>
${next.body()}
