<%! import humanize %>
<%def name="_killboard_recent(summary)">
    <ul class="summary">
        % for kill in summary:
            <li>
                <a href="https://zkillboard.com/kill/${kill['id']}/">${kill["id"]}</a>
                ${kill["system"]}
                <abbr title="${kill["date"].strftime("%Y-%m-%d %H:%M")}">${humanize.naturaltime(kill["date"]) | h}</abbr>
                <img src="${g.eve.image.render(kill["victim"]["ship_id"], 128)}"/>
                <img src="${g.eve.image.character(kill["victim"]["char_id"], 128)}"/>
                <img src="${g.eve.image.corp(kill["victim"]["corp_id"], 128)}"/>
                <img src="${g.eve.image.alliance(kill["victim"]["alliance_id"], 128)}"/>
                <img src="${g.eve.image.faction(kill["victim"]["faction_id"], 128)}"/>
                <abbr title="${"{:,.2f}".format(kill["value"])} ISK">${humanize.intword(kill["value"]) | h} ISK</abbr>
            </li>
        % endfor
    </ul>
</%def>

<%def name="render_summary(renderer, summary)"><%
    if renderer == "killboard_recent":
        return _killboard_recent(summary)
    else:
        raise RuntimeError("Unknown renderer: %s" % renderer)
%></%def>
