<%namespace name="support" file="_base_support.mako" inheritable="True"/>\
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>
            <%block name="title">
                ${support.maketitle()}
            </%block>
        </title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="canonical" href="${g.config.scheme}://${g.config.get('site.canonical')}${request.script_root}${request.path}">
        ${support.makecss("main.css")}
        <%block name="extracss"></%block>
        <% style = g.auth.get_character_prop("style") or g.config.get("style.default") %>
        % if style:
            ${support.makecss("styles/{}.css".format(style), "user-style")}
        % endif
        % for size in g.eve.image.corp_widths:
            <link rel="icon" type="image/png" sizes="${size}x${size}" href="${g.eve.image.corp(g.config.get('corp.id'), size)}"/>
        % endfor
        <script src="https://code.jquery.com/jquery-3.1.1.min.js" integrity="sha256-hVVnYaiADRTO2PzUGmuLJr8BLUSjGIZsDYGmIJLv2b8=" crossorigin="anonymous"></script>
        ${support.makejs("main.js")}
        <%block name="extrajs"></%block>
    </head>
    <body>
        <%block name="header">
            <header class="styled-border">
                <div>
                    <div>
                        <div class="left">
                            <%block name="lefthead">
                                <a id="corp-masthead" title="Home" href="${url_for('index')}">
                                    <img alt="Logo" src="${g.eve.image.corp(g.config.get('corp.id'), 256)}"/>
                                    <h1>${g.config.get("corp.name") | h}</h1>
                                </a>
                            </%block>
                        </div>
                        <div class="right">
                            <%block name="righthead">
                                <img class="spacer" alt="" src="data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs="/>
                            </%block>
                        </div>
                    </div>
                </div>
            </header>
        </%block>
        <%block name="container">
            <div id="container">
                <div>
                    <main class="styled-border">
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
            <footer class="styled-border">
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
