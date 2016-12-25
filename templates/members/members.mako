<%inherit file="../_default.mako"/>
<h2>Members</h2>
<!-- ... handle case where members is empty - means something went wrong -->
<ul>
    % for member in members:
        <li>
            <img title="${member.name}" alt="${member.name}'s Portrait" src="${g.eve.image.character(member.id, 256)}"/>
            ${member.name}
        </li>
    % endfor
</ul>
