<%!
    from datetime import datetime
%>\
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>
            <%block name="title">CORP_NAME...</%block>
        </title>
        <link rel="stylesheet" href="${url_for('staticv', filename='style.css')}" type="text/css" />
        <!-- FAVICONS... -->
    </head>
    <body>
        ${next.body()}
        <footer>
            <div>
                <%
                    copyright_year = datetime.now().year
                %>
                Copyright &copy; ${copyright_year} COPYRIGHT_HOLDER...
                &bull;
                Running <a href="https://github.com/earwig/calefaction">Calefaction</a> CALEFACTION_VERSION...
                &bull;
                <a href="https://eveonline.com">EVE Online</a> and all related trademarks are property of <a href="https://ccpgames.com">CCP hf</a>.
            </div>
        </footer>
    </body>
</html>
