% if request.url_rule.endpoint == "members.members":
    <strong>Members</strong>
% else:
    <a href="${url_for('members.members')}">Members</a>
% endif
