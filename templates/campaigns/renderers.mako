<%!
    from calefaction.format import (
        format_isk_compact, format_utctime_compact, format_security,
        get_security_class)
%>
<%def name="_killboard_kill(kill)">
    <%
        victim = kill["victim"]
        system = g.eve.universe.system(kill["system"])
    %>
    <tr>
        <td class="fluid">
            <abbr title="${kill["date"].strftime("%Y-%m-%d %H:%M")}">${format_utctime_compact(kill["date"]) | h}</abbr><br/>
            <a href="https://zkillboard.com/kill/${kill['id']}/">
                <abbr title="${"{:,.2f}".format(kill["value"])} ISK">${format_isk_compact(kill["value"]) | h}</abbr>
            </a>
        </td>
        <td class="fluid extra">
            <a href="https://zkillboard.com/system/${system.id}/">${system.name}</a> <abbr title="${system.security}" class="${get_security_class(system.security)}">${format_security(system.security)}</abbr><br/>
            <a href="https://zkillboard.com/region/${system.region.id}/">${system.region.name}</a>
        </td>
        <td class="icon">
            <a href="https://zkillboard.com/kill/${kill['id']}/">
                <img title="Kill ${kill['id']}: ..." alt="Kill ${kill['id']}: ..." src="${g.eve.image.inventory(victim["ship_id"], 64)}"/>
            </a>
        </td>
        <td class="icon extra">
            <a href="https://zkillboard.com/character/${victim['char_id']}/">
                <img title="${victim['char_name']}" alt="${victim['char_name']}" src="${g.eve.image.character(victim["char_id"], 128)}"/>
            </a>
        </td>
        <td class="icon${' extra' if victim["alliance_id"] and victim["faction_id"] else ''}">
            <a href="https://zkillboard.com/corporation/${victim['corp_id']}/">
                <img title="${victim['corp_name']}" alt="${victim['corp_name']}" src="${g.eve.image.corp(victim["corp_id"], 128)}"/>
            </a>
        </td>
        <td class="icon${'' if victim["alliance_id"] else ' extra'}">
        % if victim["alliance_id"]:
            <a href="https://zkillboard.com/alliance/${victim['alliance_id']}/">
                <img title="${victim['alliance_name']}" alt="${victim['alliance_name']}" src="${g.eve.image.alliance(victim["alliance_id"], 128)}"/>
            </a>
        % endif
        </td>
        <td class="icon${'' if victim["faction_id"] else ' extra'}">
        % if victim["faction_id"]:
            <a href="https://zkillboard.com/faction/${victim['faction_id']}/">
                <img title="${victim['faction_name']}" alt="${victim['faction_name']}" src="${g.eve.image.faction(victim["faction_id"], 128)}"/>
            </a>
        % endif
        </td>
        % if not victim["alliance_id"] and not victim["faction_id"]:
            <td class="icon spacer"></td>
        % endif
    </tr>
</%def>
<%def name="_killboard_recent(summary)">
    <div class="head">Most recent kills:</div>
    <div class="contents">
        <table class="killboard">
            % for kill in summary:
                ${_killboard_kill(kill)}
            % endfor
        </table>
    </div>
</%def>
<%def name="render_summary(renderer, summary)"><%
    if renderer == "killboard_recent":
        return _killboard_recent(summary)
    raise RuntimeError("Unknown renderer: %s" % renderer)
%></%def>
