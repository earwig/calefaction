<%inherit file="../_default.mako"/>
<%block name="title">
    ${self.support.maketitle("Map")}
</%block>
<%block name="extracss">
    ${self.support.makecss("map.css")}
</%block>
<%block name="extrajs">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/d3/4.4.1/d3.min.js" integrity="sha256-4mL8TQfOJSbg0f42dQw5cKLl2ngQXUSXqfQnvK11M44=" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/string.js/3.3.3/string.min.js" integrity="sha256-0AbuA3ySKKYec199lOYKxEcX6NdOl8CeRhquNfddzfs=" crossorigin="anonymous"></script>
    ${self.support.makejs("map.js")}
</%block>
<div id="map">
    <div class="preload">
        <h2>Map</h2>
        <noscript>
            <p>JavaScript is required to display the galaxy map.</p>
        </noscript>
    </div>
    <div class="controls">
        <div>
            <label for="map-scale">Scale</label>
            <input id="map-scale" type="range" min="1" max="6" step="0.1" value="1">
        </div>
        <div>
            Color
            <input id="map-color-sec" type="radio" name="color" value="sec">
            <label class="label" for="map-color-sec">Security</label>
            <input id="map-color-faction" type="radio" name="color" value="faction">
            <label class="label" for="map-color-faction">Faction</label>
        </div>
    </div>
</div>
