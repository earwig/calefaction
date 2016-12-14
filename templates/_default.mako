<%inherit file="_layout.mako"/>
<%block name="lefthead">
    [CORP_LOGO] CORP_NAME...
    <nav>Campaign: XYZ | Map | Intel | Members</nav>
</%block>
<%block name="righthead-">
    PLAYER_NAME [logout]
</%block>
${next.body()}
