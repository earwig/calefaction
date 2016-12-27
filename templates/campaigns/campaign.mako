<%inherit file="../_default.mako"/>
<%block name="title">
    ${self.maketitle(campaign["title"], "Campaigns")}
</%block>
<h2>
    <span class="understate">Campaign:</span>
    <span${"" if enabled else ' class="disabled"'}>${campaign["title"] | h}</span>
</h2>
<p>Hello! ...</p>
