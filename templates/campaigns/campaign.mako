<%inherit file="../_default.mako"/>
% if current:
    <h2><span class="understate">Campaign:</span> ${current} <!-- select ... --></h2>
    <p>Hello! ...</p>
% else:
    <p>No campaigns currently.</p>
% endif
