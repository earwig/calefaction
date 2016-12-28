<%inherit file="../_default.mako"/>
<%block name="title">
    ${self.maketitle(campaign["title"], "Campaigns")}
</%block>
<h2>
    <span class="understate">Campaign:</span>
    <span${"" if enabled else ' class="disabled"'}>${campaign["title"] | h}</span>
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
                    summary = mod.get_summary(name, opname, limit=5)
                    klass = "big" if primary < 1000 else "medium" if primary < 1000000 else "small"
                %>
                <div class="operation">
                    <h3>
                        <a href="${url_for('campaigns.operation', cname=name, opname=opname)}">${operation["title"] | h}</a>
                    </h3>
                    <div class="overview">
                        <div class="primary ${klass}">${"{:,}".format(primary)}</div>
                        <div class="unit">${mod.get_unit(operation, primary)}</div>
                        % if secondary is not None:
                            <div class="secondary">${"{:,}".format(secondary)}</div>
                            <div class="unit">${mod.get_unit(operation, secondary, primary=False)}</div>
                        % endif
                    </div>
                    % if summary:
                        <ul class="summary">
                            % for item in summary:
                                <li>${item}</li>
                            % endfor
                        </ul>
                    % endif
                </div>
            % endfor
        </section>
    % endfor
</div>
