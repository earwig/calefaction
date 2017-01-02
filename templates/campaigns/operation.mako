<%!
    from calefaction.format import format_isk
%>
<%inherit file="../_default.mako"/>
<%namespace file="renderers.mako" import="render_summary"/>
<%block name="title">
    ${self.support.maketitle(operation["title"], campaign["title"], "Campaigns")}
</%block>
<%block name="extracss">
    ${self.support.makecss("campaigns.css")}
</%block>
<%block name="extrajs">
    ${self.support.makejs("campaigns.js")}
</%block>
<div class="breadcrumb">
    Campaign: <a href="${url_for('.campaign', name=cname)}">${campaign["title"] | h}</a>
</div>
<h2>
    <span class="understate">Operation:</span>
    <span${"" if enabled else ' class="disabled"'}>${operation["title"] | h}</span>
    % if not enabled:
        <abbr class="disabled-info" title="Operation inactive">&#10008;</abbr>
    % endif
</h2>
<div class="operation detail">
    <%
        mod = g.config.modules.campaigns
        primary, secondary = mod.get_overview(cname, opname)
        summary, renderer = mod.get_summary(cname, opname, limit=-1)
        klass = "big" if primary < 1000 else "medium" if primary < 1000000 else "small"
        punit = mod.get_unit(operation, primary)
        sunit = mod.get_unit(operation, secondary, primary=False)
    %>
    <div class="overview">
        <div class="primary">
            <span class="num ${klass}">${"{:,}".format(primary)}</span>
            <div class="unit">${punit}</div>
        </div>
        % if secondary is not None:
            <div class="secondary">
                <abbr title="${"{:,.2f}".format(secondary)} ${sunit}">
                    <span class="num">${format_isk(secondary) | h}</span>
                    <span class="unit">${sunit}</span>
                </abbr>
            </div>
        % endif
    </div>
    % if summary:
        <div class="summary">
            ${render_summary(renderer, summary, detail=True)}
        </div>
    % endif
</div>
