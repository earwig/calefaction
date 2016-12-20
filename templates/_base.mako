<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>
            <%block name="title">${g.config.get("corp.name") | h}</%block>
        </title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="canonical" href="${g.config.scheme}://${g.config.get('site.canonical')}${request.script_root}${request.path}">
        <link rel="stylesheet" type="text/css" href="${url_for('staticv', filename='main.css')}"/>
        % if g.config.get("style"):
            <%
                charstyle = g.auth.get_character_prop("style")
                style = charstyle if charstyle else g.config.get("style")
                stylesheet = "styles/{}.css".format(style)
            %>
            <link rel="stylesheet" type="text/css" href="${url_for('staticv', filename=stylesheet)}"/>
        % endif
        % for size in g.eve.image.corp_widths:
            <link rel="icon" type="image/png" sizes="${size}x${size}" href="${g.eve.image.corp(g.config.get('corp.id'), size)}"/>
        % endfor
    </head>
    <body>
        <%block name="header">
            <header>
                <div>
                    <div class="left">
                        <%block name="lefthead">
                            <a id="corp-masthead-link" href="${url_for('index')}">
                                <img id="corp-masthead" class="aligned" title="Home" alt="Home" src="${g.eve.image.corp(g.config.get('corp.id'), 256)}"/>
                            </a>
                            <a id="corp-title" class="aligned" href="${url_for('index')}">${g.config.get("corp.name") | h}</a>
                        </%block>
                    </div>
                    <div class="right">
                        <%block name="righthead">
                            <img class="spacer aligned" alt="" src="data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs="/>
                        </%block>
                    </div>
                </div>
            </header>
        </%block>
        <%block name="container">
            <div id="container">
                <div>
                    <main>
                        <%block name="flashes">
                            <% messages = get_flashed_messages(with_categories=True) %>
                            % if messages:
                                <div id="flashes">
                                    % for category, message in messages:
                                        <div class="${category | h}">${message | h}</div>
                                    % endfor
                                </div>
                            % endif
                        </%block>
                        ${next.body()}
                    </main>
                </div>
            </div>
        </%block>
        <%block name="footer">
            <footer>
                <div>
                    <ul>
                        <li>YC&nbsp;${g.eve.clock.now()}</li>
                        <li>Running <a href="https://github.com/earwig/calefaction">Calefaction</a>&nbsp;${g.version}</li>
                        <li><a href="https://eveonline.com">EVE&nbsp;Online</a> and all related trademarks are property of <a href="https://ccpgames.com">CCP&nbsp;hf</a>.</li>
                    </ul>
                </div>
            </footer>
        </%block>
    </body>
</html>
