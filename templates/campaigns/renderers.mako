<%!
    from calefaction.format import (
        format_quantity, format_isk_compact, format_utctime_compact,
        format_security, get_security_class)
%>
<%def name="_killboard_kill(kill, detail, any_alliances, any_factions)">
    <%
        victim = kill["victim"]
        system = g.eve.universe.system(kill["system"])
        killed = g.eve.universe.killable(victim["ship_id"])
    %>
    <tr>
        <td class="fluid">
            <abbr title="${kill["date"].strftime("%Y-%m-%d %H:%M")}">${format_utctime_compact(kill["date"]) | h}</abbr><br/>
            <a href="https://zkillboard.com/kill/${kill['id']}/">
                <abbr title="${"{:,.2f}".format(kill["value"])} ISK">${format_isk_compact(kill["value"]) | h}</abbr>
            </a>
        </td>
        <td class="fluid extra">
            <a href="https://zkillboard.com/system/${system.id}/">${system.name | h}</a> <abbr title="${system.security}" class="${get_security_class(system.security)}">${format_security(system.security)}</abbr><br/>
            <a href="https://zkillboard.com/region/${system.region.id}/">${system.region.name | h}</a>
        </td>
        <td class="icon">
            <a href="https://zkillboard.com/kill/${kill['id']}/">
                <img title="Kill ${kill['id']}: ${killed.name | h}" alt="Kill ${kill['id']}: ${killed.name | h}" src="${g.eve.image.inventory(victim["ship_id"], 64)}"/>
            </a>
        </td>
        <td class="icon extra">
            <a href="https://zkillboard.com/character/${victim['char_id']}/">
                <img title="${victim['char_name'] | h}" alt="${victim['char_name'] | h}" src="${g.eve.image.character(victim["char_id"], 128)}"/>
            </a>
        </td>
        % if detail:
            <td class="detail-item">
                <a href="https://zkillboard.com/character/${victim['char_id']}/">${victim['char_name'] | h}</a>
                (${killed.name | h})
            </td>
        % endif
        <td class="icon${' extra' if victim["alliance_id"] and victim["faction_id"] else ''}">
            <a href="https://zkillboard.com/corporation/${victim['corp_id']}/">
                <img title="${victim['corp_name'] | h}" alt="${victim['corp_name'] | h}" src="${g.eve.image.corp(victim["corp_id"], 128)}"/>
            </a>
        </td>
        % if any_alliances:
            <td class="icon${'' if victim["alliance_id"] else ' extra'}">
            % if victim["alliance_id"]:
                <a href="https://zkillboard.com/alliance/${victim['alliance_id']}/">
                    <img title="${victim['alliance_name'] | h}" alt="${victim['alliance_name'] | h}" src="${g.eve.image.alliance(victim["alliance_id"], 128)}"/>
                </a>
            % endif
            </td>
        % endif
        % if any_factions:
            <td class="icon${'' if victim["faction_id"] else ' extra'}">
            % if victim["faction_id"]:
                <a href="https://zkillboard.com/faction/${victim['faction_id']}/">
                    <img title="${victim['faction_name'] | h}" alt="${victim['faction_name'] | h}" src="${g.eve.image.faction(victim["faction_id"], 128)}"/>
                </a>
            % endif
            </td>
        % endif
        % if not detail and (any_alliances or any_factions) and not victim["alliance_id"] and not victim["faction_id"]:
            <td class="icon spacer"></td>
        % endif
        % if detail:
            <td class="detail-item">
                <ul class="detail-list">
                    <li><a href="https://zkillboard.com/corporation/${victim['corp_id']}/">${victim['corp_name'] | h}</a></li>
                    % if victim['alliance_name']:
                        <li><a href="https://zkillboard.com/alliance/${victim['alliance_id']}/">${victim['alliance_name'] | h}</a></li>
                    % endif
                    % if victim['faction_name']:
                        <li><a href="https://zkillboard.com/faction/${victim['faction_id']}/">${victim['faction_name'] | h}</a></li>
                    % endif
                </ul>
            </td>
        % endif
    </tr>
</%def>
<%def name="_itemboard_item(item)">
    <%
        type_id, count, value = item
        type = g.eve.universe.type(type_id)
    %>
    <tr>
        <td class="icon">
            <img title="${type.name | h}" alt="" src="${g.eve.image.inventory(type_id, 64)}"/>
        </td>
        <td>
            <a href="https://eve-central.com/home/quicklook.html?typeid=${type_id | u}">${type.name | h}</a>
        </td>
        <td>
            <span class="count">${format_quantity(count) | h}</span><br/>
            <abbr class="price" title="${"{:,.2f}".format(value)} ISK">${format_isk_compact(value) | h}</abbr>
        </td>
    </tr>
</%def>
<%def name="_build_sort_changer(keys, descriptors, sortby)">
    % if keys:
        <ul class="change-sort">
            % for key in keys:
                % if key == sortby:
                    <li class="cur">${descriptors[key]}</li>
                % else:
                    <li><a href="${url_for('.operation', cname=cname, opname=opname, sort=key)}">${descriptors[key]}</a></li>
                % endif
            % endfor
        </ul>
    % endif
</%def>
<%def name="_killboard_recent(summary, detail, sortby)">
    % if detail:
        <%
            descriptors = {
                "new": "most recent first",
                "old": "most recent last",
                "value": "most valuable first"
            }
            if sortby not in descriptors:
                sortby = "new"
        %>
        <h3 class="head">Kills:</h3>
        ${_build_sort_changer(["new", "old", "value"], descriptors, sortby)}
    % else:
        <div class="head">Most recent kills:</div>
    % endif
    <%
        any_alliances = any(kill["victim"]["alliance_id"] for kill in summary)
        any_factions = any(kill["victim"]["faction_id"] for kill in summary)
    %>
    <div class="contents">
        <table class="board killboard">
            % for kill in summary:
                ${_killboard_kill(kill, detail, any_alliances, any_factions)}
            % endfor
        </table>
    </div>
</%def>
<%def name="_collection_items(summary, detail, sortby)">
    % if detail:
        <%
            descriptors = {
                "value": "most valuable first",
                "quantity": "greatest quantity first",
                "price": "most expensive first"
            }
            if sortby not in descriptors:
                sortby = "value"
        %>
        <h3 class="head">Items:</h3>
        ${_build_sort_changer(["value", "quantity", "price"], descriptors, sortby)}
    % else:
        <div class="head">Top items:</div>
    % endif
    <div class="contents">
        <table class="board itemboard">
            % for item in summary:
                ${_itemboard_item(item)}
            % endfor
        </table>
    </div>
</%def>

<%def name="render_summary(renderer, summary, detail=False, sortby=None)"><%
    if renderer == "killboard_recent":
        return _killboard_recent(summary, detail, sortby)
    if renderer == "collection_items":
        return _collection_items(summary, detail, sortby)
    raise RuntimeError("Unknown renderer: %s" % renderer)
%></%def>
