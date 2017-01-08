<%inherit file="../_default.mako"/>
<%block name="title">
    ${self.support.maketitle("Map")}
</%block>
<%block name="extracss">
    ${self.support.makecss("map.css")}
</%block>
<%block name="extrajs">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/d3/4.4.1/d3.min.js" integrity="sha256-4mL8TQfOJSbg0f42dQw5cKLl2ngQXUSXqfQnvK11M44=" crossorigin="anonymous"></script>
    ${self.support.makejs("map.js")}
</%block>
<div id="map">
    <h2>Map</h2>
    <noscript>
        <p>JavaScript is required to display the galaxy map.</p>
    </noscript>
</div>
