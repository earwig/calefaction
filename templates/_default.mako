<%inherit file="_base.mako"/>
<%block name="lefthead">
    ${parent.lefthead()}
    <nav>
        <ul>
            % for module in g.modules:
                <% navitem = module.navitem() %>
                % if navitem:
                    <li>${navitem}</li>
                % endif
            % endfor
        </ul>
    </nav>
</%block>
<%block name="righthead">
    <div id="character-portrait">
        <img class="styled-border" alt="Portrait" src="${g.eve.image.character(g.auth.get_character_id() or 1, 256)}"/>
        <div id="character-options" class="styled-border">
            <div id="style-options">
                <% cur_style = g.auth.get_character_prop("style") or g.config.get("style.default") %>
                % for style in g.config.get("style.enabled"):
                    <%
                        stitle = style.title()
                        url = url_for('staticv', filename='images/style/{}.png'.format(style))
                    %>
                    <form action="${url_for('set_style', style=style)}" method="post"${' class="cur"' if style == cur_style else ''}>
                        <input type="submit" title="${stitle | h}" value="${stitle | h}" data-style="${style | h}"${' disabled' if style == cur_style else ''}
                            style="background-image: url('${url}')">
                    </form>
                % endfor
            </div>
        </div>
    </div>
    <span id="character-summary">
        ${g.auth.get_character_prop("name") | h}
        <span class="sep">[</span><a id="logout" title="Log out" href="${url_for('logout')}">log out</a><span class="sep">]</span>
    </span>
</%block>
${next.body()}
