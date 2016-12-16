<%!
    from datetime import datetime
%>\
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>
            <%block name="title">${g.config.get("corp.name")}</%block>
        </title>
        <link rel="stylesheet" type="text/css" href="${url_for('staticv', filename='main.css')}" />
        <link rel="stylesheet" type="text/css" href="${url_for('staticv', filename='styles/minmatar.css')}" />
        % for size in g.eve.image.corp_widths:
            <link rel="icon" type="image/png" sizes="${size}x${size}" href="${g.eve.image.corp(g.config.get('corp.id'), size)}" />
        % endfor
    </head>
    <body>
        ${next.body()}
        <footer>
            <div>
                <% copyright_year = datetime.now().year %>
                Copyright &copy; ${copyright_year} ${g.config.get("corp.copyright")}
                &bull;
                Running <a href="https://github.com/earwig/calefaction">Calefaction</a> ${g.version}
                &bull;
                <a href="https://eveonline.com">EVE Online</a> and all related trademarks are property of <a href="https://ccpgames.com">CCP hf</a>.
            </div>
        </footer>
    </body>
</html>
