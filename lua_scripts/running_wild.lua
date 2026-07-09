local RUNNING_WILD_TRIGGER = 87840

local JOURNEYMAN_RIDING = 33391

local SPEED_60  = 110010
local SPEED_100 = 110011

local MALE_DISPLAY_QUAD   = 94133
local FEMALE_DISPLAY_QUAD = 94134

local function IsRunningWild(player)
    local display = player:GetDisplayId()

    return display == MALE_DISPLAY_QUAD
        or display == FEMALE_DISPLAY_QUAD
end

local function CancelRunningWild(player)

    player:RemoveAura(SPEED_60)
    player:RemoveAura(SPEED_100)

    player:DeMorph()
end

local function StartRunningWild(player)

    if IsRunningWild(player) then
        return
    end

    if player:GetGender() == 0 then
        player:SetDisplayId(MALE_DISPLAY_QUAD)
    else
        player:SetDisplayId(FEMALE_DISPLAY_QUAD)
    end

    if player:HasSpell(JOURNEYMAN_RIDING) then
        player:CastSpell(SPEED_100, player)
    else
        player:CastSpell(SPEED_60, player)
    end
end

----------------------------------------------------
-- SPELL CAST
----------------------------------------------------

local function OnSpellCast(event, player, spell)

    local id = spell:GetEntry()

    if id == RUNNING_WILD_TRIGGER then

        if IsRunningWild(player) then
            CancelRunningWild(player)
        else
            StartRunningWild(player)
        end

        return
    end

    if IsRunningWild(player) then
        CancelRunningWild(player)
    end
end

RegisterPlayerEvent(5, OnSpellCast)

----------------------------------------------------
-- COMBAT
----------------------------------------------------

RegisterPlayerEvent(33, function(event, player)
    if IsRunningWild(player) then
        CancelRunningWild(player)
    end
end)

----------------------------------------------------
-- LOOT
----------------------------------------------------

RegisterPlayerEvent(32, function(event, player)
    if IsRunningWild(player) then
        CancelRunningWild(player)
    end
end)

RegisterPlayerEvent(37, function(event, player)
    if IsRunningWild(player) then
        CancelRunningWild(player)
    end
end)

----------------------------------------------------
-- SAFETY POLL
----------------------------------------------------

local function Poll()

    for _, player in ipairs(GetPlayersInWorld()) do

        local hasAura = player:HasAura(SPEED_60) or player:HasAura(SPEED_100)
        local morphed = IsRunningWild(player)

        -- Conditions that always cancel Running Wild
        if hasAura and (not player:IsAlive() or player:IsInWater()) then
            CancelRunningWild(player)

        -- Aura exists but player isn't morphed (login, .reload ale, etc.)
        elseif hasAura and not morphed then

            if player:GetGender() == 0 then
                player:SetDisplayId(MALE_DISPLAY_QUAD)
            else
                player:SetDisplayId(FEMALE_DISPLAY_QUAD)
            end

        -- Morphed but aura disappeared
        elseif morphed and not hasAura then
            CancelRunningWild(player)
        end
    end

    return 500
end

CreateLuaEvent(Poll, 500, 0)