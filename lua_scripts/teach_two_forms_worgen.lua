--[[
    Worgen "Two Forms" fallback teacher
    -----------------------------------
    Worgen get Two Forms in Gilneas, from a quest that not every setup has ported. As a fallback, a Worgen who
    lacks the spell is taught it on logging in or entering a zone anywhere outside Gilneas, so the Gilneas
    questline still teaches it where it exists.

    Two Forms (68996) applies the altered form aura (F-063), so both genders use it.
]]

local RACE_WORGEN = 22 -- retail ID, fixed in modpaks/config.sql

local TWO_FORMS = 68996 -- @SpellTwoFormsMale in modpaks/config.sql

local GILNEAS_ZONES = {
    [4714] = true, -- Gilneas (@Gilneas)
    [4755] = true, -- Gilneas City (@GilneasCity)
}

local function GrantTwoForms(player, zoneId)
    if player:GetRace() ~= RACE_WORGEN or player:HasSpell(TWO_FORMS) then
        return
    end

    if GILNEAS_ZONES[zoneId] then
        return -- still in the starting area: the questline teaches it
    end

    player:LearnSpell(TWO_FORMS)
end

RegisterPlayerEvent(3, function(event, player) -- PLAYER_EVENT_ON_LOGIN
    GrantTwoForms(player, player:GetZoneId())
end)

RegisterPlayerEvent(27, function(event, player, newZone, newArea) -- PLAYER_EVENT_ON_UPDATE_ZONE
    GrantTwoForms(player, newZone)
end)
