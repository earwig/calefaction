<%inherit file="../_default.mako"/>
<%block name="title">
    ${campaign["title"] | h} &ndash; Campaign &ndash; ${g.config.get("corp.name") | h}
</%block>
<h2><span class="understate">Campaign:</span> ${campaign["title"] | h}</h2>
<p>Hello! ...</p>
