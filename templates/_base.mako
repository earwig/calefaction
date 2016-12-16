<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>
            <%block name="title">${g.config.get("corp.name") | h}</%block>
        </title>
        <link rel="stylesheet" type="text/css" href="${url_for('staticv', filename='main.css')}" />
        <link rel="stylesheet" type="text/css" href="${url_for('staticv', filename='styles/minmatar.css')}" />
        % for size in g.eve.image.corp_widths:
            <link rel="icon" type="image/png" sizes="${size}x${size}" href="${g.eve.image.corp(g.config.get('corp.id'), size)}" />
        % endfor
    </head>
    <body>
        <%block name="header">
            <header>
                <div>
                    <div class="left">
                        <%block name="lefthead">
                            <a href="/">
                                <img id="corp-masthead" class="aligned" src="${g.eve.image.corp(g.config.get('corp.id'), 256)}"/>
                            </a>
                            <a href="/" class="aligned">${g.config.get("corp.name") | h}</a>
                        </%block>
                    </div><!--
                    --><div class="right">
                        <%block name="righthead"/>
                    </div>
                </div>
            </header>
        </%block>
        <%block name="container">
            <div id="container">
                <div>
                    <main>
                        ${next.body()}
                    </main>
                </div>
            </div>
        </%block>
        <%block name="footer">
            <footer>
                <div>
                    Running <a href="https://github.com/earwig/calefaction">Calefaction</a> ${g.version}
                    &bull;
                    <a href="https://eveonline.com">EVE Online</a> and all related trademarks are property of <a href="https://ccpgames.com">CCP hf</a>.
                </div>
            </footer>
        </%block>
    </body>
</html>
