<%inherit file="_base.mako"/>
<%block name="lefthead">
    ${parent.lefthead()}
    <nav>
        Campaign: XYZ | Map | Intel | Members...
    </nav>
</%block>
<%block name="righthead">
    PLAYER_NAME... [logout]  <!-- use GET /logout here and JS switch it to a POST form -->
</%block>
${next.body()}
