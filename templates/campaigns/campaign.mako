<%!
    from calefaction.format import format_isk
%>
<%inherit file="../_default.mako"/>
<%namespace file="renderers.mako" import="render_summary"/>
<%block name="title">
    ${self.maketitle(campaign["title"], "Campaigns")}
</%block>
<h2>
    <span class="understate">Campaign:</span>
    <span${"" if enabled else ' class="disabled"'}>${campaign["title"] | h}</span>
    % if not enabled:
        <abbr class="disabled-info" title="Campaign inactive">&#10008;</abbr>
    % endif
</h2>
<% mod = g.config.modules.campaigns %>
<div id="operations">
    % for section in campaign["layout"]:
        <% klass = "loose" if len(section) < 3 else "tight" %>
        <section class="${klass}">
            % for opname in section:
                <%
                    operation = campaign["operations"][opname]
                    primary, secondary = mod.get_overview(name, opname)
                    summary, renderer = mod.get_summary(name, opname, limit=5)
                    klass = "big" if primary < 1000 else "medium" if primary < 1000000 else "small"
                    punit = mod.get_unit(operation, primary)
                    sunit = mod.get_unit(operation, secondary, primary=False)
                %>
                <div class="operation">
                    <h3>
                        <a href="${url_for('campaigns.operation', cname=name, opname=opname)}">${operation["title"] | h}</a>
                    </h3>
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
                            ${render_summary(renderer, summary)}
                        </div>
                    % endif
                </div>
            % endfor
        </section>
    % endfor
</div>
