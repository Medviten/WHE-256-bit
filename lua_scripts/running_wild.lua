local RUNNING_WILD_TRIGGER = 87840
local JOURNEYMAN_RIDING = 33391
local SPEED_60  = 110010
local SPEED_100 = 110011
local MALE_DISPLAY_QUAD   = 94133
local FEMALE_DISPLAY_QUAD = 94134

local NATIVE_DISPLAY = {
    -- [raceId] = { [genderId] = displayId }
    [1] = { [0] = 19723, [1] = 19724 }, -- Human: male, female
    [2] = { [0] = 22, [1] = 20316 }, -- Orc: male*, female
    [3] = { [0] = 20317, [1] = 22 }, -- Dwarf: male, female*
    [4] = { [0] = 20318, [1] = 22 }, -- Night Elf: male, female*
    [5] = { [0] = 22, [1] = 22 }, -- Undead: male*, female*
    [6] = { [0] = 20585, [1] = 20584 }, -- Tauren: male, female
    [7] = { [0] = 20580, [1] = 20320 }, -- Gnome: male, female
    [8] = { [0] = 20321, [1] = 22 }, -- Troll: male, female*
    [9] = { [0] = 20582, [1] = 20583 }, -- Goblin: male, female
    [10] = { [0] = 20578, [1] = 20579 }, -- Blood Elf: male, female
    [11] = { [0] = 22, [1] = 20323 }, -- Draenei: male*, female
    [12] = { [0] = 29422, [1] = 29423 }, -- Worgen: male, female
    [13] = { [0] = 22, [1] = 22 }, -- High Elf: male*, female*
    [14] = { [0] = 22, [1] = 22 }, -- Mag'har Orc: male*, female*
}

local function GetNativeDisplay(player)
    local race = player:GetRace()
    local gender = player:GetGender()
    local raceTable = NATIVE_DISPLAY[race]
    if raceTable and raceTable[gender] then
        return raceTable[gender]
    end
    return nil -- fall through / log a warning if a race is missing an entry
end

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
    player:SetDisplayId(GetNativeDisplay(player))
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
            player:SetDisplayId(GetNativeDisplay(player))
        end
        ::continue::
    end
    return 500 -- re-run every 500ms
end
CreateLuaEvent(PollRunningWild, 500, 0)