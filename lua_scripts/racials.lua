local WORGEN = 12
local LEVEL = 20

local function OnFirstLogin(event, player)
    if player:GetLevel() ~= 1 then
        player:RemoveSpell(87840)
    end
end

RegisterPlayerEvent(30, OnFirstLogin)

function OnLevelChange(event, player, oldLevel)
    if oldLevel < LEVEL and player:GetLevel() >= LEVEL then
        if player:GetRace() == WORGEN then
            if not player:HasSpell(33388) then
                player:LearnSpell(33388)
            end

            if not player:HasSpell(87840) then
                player:LearnSpell(87840)

            end
        end
    end
end

RegisterPlayerEvent(13, OnLevelChange)