Campaign:
% if request.url_rule.endpoint == "campaigns.campaign":
    <form id="campaigns-select" action="${url_for('campaigns.set_campaign')}" method="post" class="styled-border">
        <select name="campaign">
            <% config = g.config.modules.campaigns.config %>
            % for name in config["enabled"]:
                <% params = config["campaigns"][name] %>
                <option value="${name | h}"${" selected" if name == current else ""}>${params["title"] | h}</option>
            % endfor
        </select>
        <input type="submit" value="Change">
    </form>
% else:
    <% campaign = g.config.modules.campaigns.config["campaigns"][current] %>
    <a href="${url_for('campaigns.campaign')}">${campaign["title"]}</a>
% endif
