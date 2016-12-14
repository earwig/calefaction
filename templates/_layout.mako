<%inherit file="_base.mako"/>
<header>
    <div>
        <div class="left"><%block name="lefthead"/></div><!--
        --><div class="right"><%block name="righthead"/></div>
    </div>
</header>
<div id="container">
    <div>
        <main>
            ${next.body()}
        </main>
    </div>
</div>
