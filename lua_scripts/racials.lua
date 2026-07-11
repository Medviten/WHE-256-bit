local WORGEN = 3
local LEVEL = 20

local RUNNING_WILD = 87840
local TWO_FORMS = 68996

local function OnFirstLogin(event, player)
    if player:GetLevel() ~= 1 then
        player:RemoveSpell(87840)
        player:RemoveSpell(68996)
    end
end

RegisterPlayerEvent(30, OnFirstLogin)

function OnLevelChange(event, player, oldLevel)
    if oldLevel < LEVEL and player:GetLevel() >= LEVEL then
        if player:GetRace() == WORGEN then
            if not player:HasSpell(33388) then
                player:LearnSpell(33388)
            end

            if not player:HasSpell(RUNNING_WILD) then
                player:LearnSpell(RUNNING_WILD)
            end

            if not player:HasSpell(TWO_FORMS) then
                player:LearnSpell(TWO_FORMS)
            end
        end
    end
end

RegisterPlayerEvent(13, OnLevelChange)