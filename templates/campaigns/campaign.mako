<%inherit file="../_default.mako"/>
<%block name="title">
    ${self.maketitle(campaign["title"], "Campaigns")}
</%block>
<h2>
    <span class="understate">Campaign:</span>
    <span${"" if enabled else ' class="disabled"'}>${campaign["title"] | h}</span>
</h2>
<div id="operations">
    % for section in campaign["layout"]:
        <section>
            % for opname in section:
                <% operation = campaign["operations"][opname] %>
                <div class="operation">
                    <h3><a href="${url_for('campaigns.operation', cname=name, opname=opname)}">${operation["title"] | h}</a></h3>
                    <div class="stats">
                        <!-- ... -->
                        <%
                            random = __import__("random")
                            n = [random.randint(0, 500), random.randint(10000, 500000), random.randint(10000000, 50000000000)][random.randint(0, 2)]
                        %>
                        <%
                            klass = "big" if n < 1000 else "medium" if n < 1000000 else "small"
                        %>
                        <div class="primary">
                            <span class="${klass}">${"{:,}".format(n)}</span>
                        </div>
                        <div class="unit">${"ships" if klass == "big" else "points" if klass == "medium" else "ISK"}</div> <!-- ... plural -->
                    </div>
                </div>
            % endfor
        </section>
    % endfor
</div>
