--[[
    Worgen "Running Wild" speed-spell teacher
    ------------------------------------------
    Fires whenever a player learns a spell. If the spell learned is one of the
    two native riding-skill spells, and the player is a Worgen, teach the
    correct gendered custom speed spell and drop the old one if upgrading.

    Native riding spells (static WotLK content, do not change per-core):
        33388 = Apprentice Riding   (75 skill,  60% speed)
        33391 = Journeyman Riding   (150 skill, 100% speed)
]]

local RACE_WORGEN = 12

local RIDE_APPRENTICE_SPELL = 33388
local RIDE_JOURNEYMAN_SPELL = 33391

local WORGEN_APPRENTICE_MALE   = 110010
local WORGEN_APPRENTICE_FEMALE = 110012
local WORGEN_JOURNEYMAN_MALE   = 110011
local WORGEN_JOURNEYMAN_FEMALE = 110013

-- GENDER_MALE = 0, GENDER_FEMALE = 1 (standard Eluna/DBC convention)
local function GetGenderedSpells(player)
    local isMale = (player:GetGender() == 0)
    return {
        apprentice = isMale and WORGEN_APPRENTICE_MALE or WORGEN_APPRENTICE_FEMALE,
        journeyman = isMale and WORGEN_JOURNEYMAN_MALE or WORGEN_JOURNEYMAN_FEMALE,
    }
end

-- NOTE: we intentionally never remove the lower-tier spell. WotLK's client
-- keeps lower-rank riding/speed spells and lower mounts around fine (unlike
-- later expansions with a consolidated mount journal), so there's no need to
-- strip it — and trying to do so via RemoveSpell() was what caused the new
-- spell to not show up live in the first place (its resync packet appears to
-- stomp the just-learned spell until the next full login sync).
local function ApplyRunningWildTier(player, tier)
    if player:GetRace() ~= RACE_WORGEN then
        return
    end

    local spells = GetGenderedSpells(player)
    local spellId = spells[tier]

    if spellId and not player:HasSpell(spellId) then
        player:LearnSpell(spellId)
    end
end

local function OnLearnSpell(event, player, spellId)
    if spellId == RIDE_APPRENTICE_SPELL then
        ApplyRunningWildTier(player, "apprentice")
    elseif spellId == RIDE_JOURNEYMAN_SPELL then
        ApplyRunningWildTier(player, "journeyman")
    end
end

-- Safety net: re-sync on login in case a character already knows a riding
-- tier (e.g. granted via SQL/.learn/character import) without ever passing
-- through OnLearnSpell above.
local function OnLogin(event, player)
    if player:GetRace() ~= RACE_WORGEN then
        return
    end

    if player:HasSpell(RIDE_JOURNEYMAN_SPELL) then
        ApplyRunningWildTier(player, "journeyman")
    elseif player:HasSpell(RIDE_APPRENTICE_SPELL) then
        ApplyRunningWildTier(player, "apprentice")
    end
end

RegisterPlayerEvent(44, OnLearnSpell) -- PLAYER_EVENT_ON_LEARN_SPELL
RegisterPlayerEvent(3, OnLogin)       -- PLAYER_EVENT_ON_LOGIN