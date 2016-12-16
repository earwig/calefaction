<%inherit file="_base.mako"/>
<%block name="lefthead">
    ${parent.lefthead()}
    <nav>
        Campaign: XYZ | Map | Intel | Members...
    </nav>
</%block>
<%block name="righthead">
    PLAYER_NAME... [logout]
</%block>
${next.body()}
