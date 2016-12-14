<%inherit file="_base.mako"/>
<%block name="title">
    Error &ndash; ...name...
</%block>
<div id="container">
    <div>
        <main>
            <h1>Error!</h1>
            <p>You may report the following information to the developers:</p>
            <div id="error">
                <pre>${traceback | trim,h}</pre>
            </div>
        </main>
    </div>
</div>
