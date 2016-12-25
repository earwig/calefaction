<%inherit file="../_default.mako"/>
<h2>Members</h2>
<!-- ... handle case where members is empty - means something went wrong -->
<ul id="members-list">
    % for member in members:
        <li>
            <a href="${g.eve.image.character(member.id, 1024)}">
                <img class="styled-border" title="${member.name}" alt="${member.name}'s Portrait" src="${g.eve.image.character(member.id, 256)}"/>
            </a>
            <span>${member.name}</span>
        </li>
    % endfor
</ul>
