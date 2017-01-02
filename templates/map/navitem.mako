% if request.url_rule.endpoint == "map.map":
    <strong>Map</strong>
% else:
    <a href="${url_for('map.map')}">Map</a>
% endif
