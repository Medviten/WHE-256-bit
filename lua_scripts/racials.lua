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
local CLASS_DEATH_KNIGHT = 6

local RIDE_APPRENTICE_SPELL = 33388
local RIDE_JOURNEYMAN_SPELL = 33391

local WORGEN_APPRENTICE_MALE   = 87840
local WORGEN_APPRENTICE_FEMALE = 87841
local WORGEN_JOURNEYMAN_MALE   = 110010
local WORGEN_JOURNEYMAN_FEMALE = 110011

-- GENDER_MALE = 0, GENDER_FEMALE = 1 (standard Eluna/DBC convention)
local function GetGenderedSpells(player)
    local isMale = (player:GetGender() == 0)
    return {
        apprentice = isMale and WORGEN_APPRENTICE_MALE or WORGEN_APPRENTICE_FEMALE,
        journeyman = isMale and WORGEN_JOURNEYMAN_MALE or WORGEN_JOURNEYMAN_FEMALE,
    }
end

local function ApplyRunningWildTier(player, tier)
    if player:GetRace() ~= RACE_WORGEN then
        return
    end

    -- Death Knights start with 150 riding skill innately and should go
    -- straight to Journeyman-tier Running Wild; they never need (and never
    -- naturally receive) the Apprentice-tier custom spell, so skip only
    -- that tier for them instead of bailing out of every tier.
    if tier == "apprentice" and player:GetClass() == CLASS_DEATH_KNIGHT then
        return
    end

    local spells = GetGenderedSpells(player)
    local spellId = spells[tier]

    if tier == "journeyman" and player:HasSpell(spells.apprentice) then
        player:RemoveSpell(spells.apprentice)
    end

    if spellId and not player:HasSpell(spellId) then
        player:RegisterEvent(function(eventId, delay, repeats, plr)
            if plr and plr:IsInWorld() and not plr:HasSpell(spellId) then
                plr:LearnSpell(spellId)
            end
        end, 250, 1)
    end
end

local function OnLearnSpell(event, player, spellId)
    if spellId == RIDE_APPRENTICE_SPELL then
        ApplyRunningWildTier(player, "apprentice")
    elseif spellId == RIDE_JOURNEYMAN_SPELL then
        ApplyRunningWildTier(player, "journeyman")
    end
end

-- Primary trigger: hook the actual spell CAST rather than the generic
-- "learn spell" player event. PLAYER_EVENT_ON_LEARN_SPELL turned out not to
-- fire reliably for Journeyman Riding — most likely because that spell's
-- skill-line auto-grant path doesn't route through the same internal call
-- as a normal LearnSpell(). Hooking SPELL_EVENT_ON_CAST on the two riding
-- spell IDs directly sidesteps that: it fires whenever the player casts
-- (i.e. trains) that spell, full stop, regardless of the internal path.
local function OnCastRidingSpell(tier)
    return function(event, caster, spell, skipCheck)
        local player = caster
        if player.ToPlayer then
            player = caster:ToPlayer()
        end
        if player then
            ApplyRunningWildTier(player, tier)
        end
    end
end

RegisterSpellEvent(RIDE_APPRENTICE_SPELL, 2, OnCastRidingSpell("apprentice")) -- SPELL_EVENT_ON_CAST
RegisterSpellEvent(RIDE_JOURNEYMAN_SPELL, 2, OnCastRidingSpell("journeyman")) -- SPELL_EVENT_ON_CAST


-- Safety net: re-sync on login in case a character already knows a riding
-- tier (e.g. granted via SQL/.learn/character import) without ever passing
-- through OnLearnSpell above.
--
-- Also handles the Death Knight edge case: DKs get 150 riding skill for
-- free at creation, but only Apprentice Riding (33388) is ever cast via
-- playercreateinfo_cast_spell — Journeyman Riding (33391) is never cast, so
-- it never reaches our spell-cast hook, and these characters get stuck on
-- the 60%-speed custom Apprentice Running Wild spell despite already having
-- full 150 skill, with Journeyman Riding then wrongly showing as purchasable
-- at trainers. We cast it here — after full player load, rather than via
-- playercreateinfo_cast_spell at creation time, which is what was unlearning
-- Apprentice for you — and then explicitly re-sync the tier immediately
-- after, rather than relying solely on the cast hook firing for a triggered
-- cast.
local function OnLogin(event, player)
    if player:GetRace() ~= RACE_WORGEN then
        return
    end

    if player:GetClass() == CLASS_DEATH_KNIGHT and not player:HasSpell(RIDE_JOURNEYMAN_SPELL) then
        player:CastSpell(player, RIDE_JOURNEYMAN_SPELL, true)
    end

    if player:HasSpell(RIDE_JOURNEYMAN_SPELL) then
        ApplyRunningWildTier(player, "journeyman")
    elseif player:HasSpell(RIDE_APPRENTICE_SPELL) then
        ApplyRunningWildTier(player, "apprentice")
    end
end

local function OnLogin(event, player)
    if player:GetRace() ~= RACE_WORGEN then
        return
    end

    if player:GetClass() == CLASS_DEATH_KNIGHT and not player:HasSpell(RIDE_JOURNEYMAN_SPELL) then
        player:CastSpell(player, RIDE_JOURNEYMAN_SPELL, true)

        -- Casting Journeyman Riding triggers the engine's normal
        -- "supersede the lower rank" behavior, which strips 33388 from the
        -- spellbook exactly like it would for a leveling character who just
        -- trained Journeyman naturally. That's correct engine behavior, but
        -- it leaves DKs with no record of ever knowing Apprentice, so the
        -- riding trainer wrongly still offers to sell it to them.
        --
        -- Fix: re-add 33388 directly into the spellbook via LearnSpell
        -- (not CastSpell) once the Journeyman cast's own effects have
        -- finished resolving. LearnSpell just writes the character_spell
        -- row without running the spell's effect script, so it won't
        -- retrigger the removal logic that's tied to *casting* 33391.
        player:RegisterEvent(function(eventId, delay, repeats, plr)
            if plr and plr:IsInWorld() and not plr:HasSpell(RIDE_APPRENTICE_SPELL) then
                plr:LearnSpell(RIDE_APPRENTICE_SPELL)
            end
        end, 250, 1)
    end

    if player:HasSpell(RIDE_JOURNEYMAN_SPELL) then
        ApplyRunningWildTier(player, "journeyman")
    elseif player:HasSpell(RIDE_APPRENTICE_SPELL) then
        ApplyRunningWildTier(player, "apprentice")
    end
end

RegisterPlayerEvent(44, OnLearnSpell) -- PLAYER_EVENT_ON_LEARN_SPELL
RegisterPlayerEvent(3, OnLogin)       -- PLAYER_EVENT_ON_LOGIN