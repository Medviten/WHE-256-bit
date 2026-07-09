local RUNNING_WILD_TRIGGER = 87840
local JOURNEYMAN_RIDING = 33391
local SPEED_60  = 110010
local SPEED_100 = 110011
local MALE_DISPLAY_QUAD   = 94133
local FEMALE_DISPLAY_QUAD = 94134

local function GetActiveBuff(player)
    if player:HasAura(SPEED_60) then return SPEED_60 end
    if player:HasAura(SPEED_100) then return SPEED_100 end
    return nil
end

local function IsRunningWildActive(player)
    return GetActiveBuff(player) ~= nil
end

local function CancelRunningWild(player)
    if not IsRunningWildActive(player) then return end
    player:RemoveAura(SPEED_60)
    player:RemoveAura(SPEED_100)
    player:SetDisplayId(player:GetNativeDisplayId())
end

local function StartRunningWild(player, spell)
    if spell:GetEntry() ~= RUNNING_WILD_TRIGGER then return end
    if IsRunningWildActive(player) then return end -- already active, don't restack

    if player:GetGender() == 0 then
        player:SetDisplayId(MALE_DISPLAY_QUAD)
    else
        player:SetDisplayId(FEMALE_DISPLAY_QUAD)
    end

    if player:HasSpell(JOURNEYMAN_RIDING) then
        player:AddAura(SPEED_100, player)
    else
        player:AddAura(SPEED_60, player)
    end
end

-- Cast the trigger spell
RegisterPlayerEvent(5, StartRunningWild) -- ON_SPELL_CAST

-- Cancel on casting anything else (mirrors "can't cast while mounted")
RegisterPlayerEvent(5, function(event, player, spell, skipCheck)
    if spell:GetEntry() == RUNNING_WILD_TRIGGER then return end
    CancelRunningWild(player)
end)

-- Cancel on entering combat (covers being attacked and most attack-initiation cases)
RegisterPlayerEvent(33, function(event, player, enemy) -- ON_ENTER_COMBAT
    CancelRunningWild(player)
end)

-- Cancel on looting
RegisterPlayerEvent(32, function(event, player, item, count) CancelRunningWild(player) end) -- ON_LOOT_ITEM
RegisterPlayerEvent(37, function(event, player, amount) CancelRunningWild(player) end)       -- ON_LOOT_MONEY

-- Catch-all: expiry, death, deep water, dispel, anything without a dedicated hook
local function PollRunningWild()
    local players = GetPlayersInWorld()
    for _, player in ipairs(players) do
        if not IsRunningWildActive(player) then goto continue end
        if not player:IsAlive() or player:IsInWater() then
            CancelRunningWild(player)
        elseif not player:HasAura(GetActiveBuff(player) or 0) then
            player:SetDisplayId(player:GetNativeDisplayId())
        end
        ::continue::
    end
    return 500 -- re-run every 500ms
end
CreateLuaEvent(PollRunningWild, 500, 0)