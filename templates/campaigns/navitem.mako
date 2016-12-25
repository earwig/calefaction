Campaign:
% if request.url_rule.endpoint == "campaigns.campaign":
    <strong>${current}</strong>
% else:
    <a href="${url_for('campaigns.campaign')}">${current}</a>
% endif
