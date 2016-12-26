<%inherit file="../_default.mako"/>
<%block name="title">
    ${self.maketitle(campaign["title"], "Campaign")}
</%block>
<h2><span class="understate">Campaign:</span> ${campaign["title"] | h}</h2>
<p>Hello! ...</p>
