% if request.url_rule.endpoint == "intel.intel":
    <strong>Intel</strong>
% else:
    <a href="${url_for('intel.intel')}">Intel</a>
% endif
