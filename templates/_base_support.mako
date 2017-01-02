<%! import markupsafe %>
<%def name="maketitle(*parts)" filter="trim">
    <%
        if request.url_rule and request.url_rule.endpoint == "index":
            parts = ()
    %>
    ${" | ".join(parts + (g.config.get("corp.name"),)) | h}
</%def>
<%def name="makecss(filename, id_=None)" filter="trim">
    <link ${'id="{}" '.format(markupsafe.escape(id_)) if id_ else ""}rel="stylesheet" type="text/css" href="${url_for('staticv', filename=filename)}"/>
</%def>
<%def name="makejs(filename)" filter="trim">
    <script src="${url_for('staticv', filename=filename)}"></script>
</%def>
