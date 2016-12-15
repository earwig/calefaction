<%inherit file="_layout.mako"/>
<%block name="lefthead">
    [C_LOGO] C_NAME...
</%block>
<%block name="righthead">
    <img id="login-button" src="${url_for('staticv', filename='images/eve-login.png')}"/>
</%block>
<p>Hello, world!</p>
