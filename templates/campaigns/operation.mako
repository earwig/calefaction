<%inherit file="../_default.mako"/>
<%block name="title">
    ${self.support.maketitle(operation["title"], campaign["title"], "Campaigns")}
</%block>
<%block name="extracss">
    ${self.support.makecss("campaigns.css")}
</%block>
<%block name="extrajs">
    ${self.support.makejs("campaigns.js")}
</%block>
<h2> <!-- ... breadcrumb -->
    <span class="understate">Operation:</span>
    <span${"" if enabled else ' class="disabled"'}>${operation["title"] | h}</span>
</h2>
<p>...</p>
