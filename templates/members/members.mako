<%inherit file="../_default.mako"/>
<%block name="title">
    ${self.support.maketitle("Members")}
</%block>
<%block name="extracss">
    ${self.support.makecss("members.css")}
</%block>
<h2>Members</h2>
% if members:
    <ul id="members-list">
        % for member in members:
            <li>
                <a href="${g.eve.image.character(member.id, 1024)}">
                    <img class="styled-border" title="${member.name}" alt="${member.name}'s Portrait" src="${g.eve.image.character(member.id, 128)}"/>
                </a>
                % if member.roles:
                    <span>${member.name}<em>${member.roles}</em></span>
                % else:
                    <span>${member.name}</span>
                % endif
            </li>
        % endfor
    </ul>
% else:
    <p>You don't have access to the members list.</p>
% endif
