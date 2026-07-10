local RUNNING_WILD_TRIGGER = 87840

local JOURNEYMAN_RIDING = 33391

local SPEED_60_MALE  = 110010
local SPEED_100_MALE = 110011
local SPEED_60_FEMALE  = 110012
local SPEED_100_FEMALE = 110013

local TWO_FORMS_TRIGGER = 68996

local TWO_FORMS_MALE = 68994
local TWO_FORMS_FEMALE = 68995

local function IsRunningWild(player)
    return player:HasAura(SPEED_60_MALE) or player:HasAura(SPEED_100_MALE)
        or player:HasAura(SPEED_60_FEMALE) or player:HasAura(SPEED_100_FEMALE)
end

local function IsHumanForm(player)
    return player:HasAura(TWO_FORMS_MALE) or player:HasAura(TWO_FORMS_FEMALE)
end

local function CancelRunningWild(player)

    player:RemoveAura(SPEED_60_MALE)
    player:RemoveAura(SPEED_100_MALE)
    player:RemoveAura(SPEED_60_FEMALE)
    player:RemoveAura(SPEED_100_FEMALE)

end

local function CancelTwoForms(player)

    player:RemoveAura(TWO_FORMS_MALE)
    player:RemoveAura(TWO_FORMS_FEMALE)

end

local function StartRunningWild(player)

    if player:HasSpell(JOURNEYMAN_RIDING) then
        if player:GetGender() == 0 then
            player:CastSpell(player, SPEED_100_MALE, false)
        else
            player:CastSpell(player, SPEED_100_FEMALE, false)
        end

    else
        if player:GetGender() == 0 then
            player:CastSpell(player, SPEED_60_MALE, false)
        else
            player:CastSpell(player, SPEED_60_FEMALE, false)
        end
    end
end

local function StartTwoForms(player)

    if player:GetGender() == 0 then
        player:CastSpell(player, TWO_FORMS_MALE, false)

    else
        player:CastSpell(player, TWO_FORMS_FEMALE, false)

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

    elseif id == TWO_FORMS_TRIGGER then

        if IsHumanForm(player) then
            CancelTwoForms(player)
        else
            StartTwoForms(player)
        end
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

    if IsHumanForm(player) then
        CancelTwoForms(player)
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
