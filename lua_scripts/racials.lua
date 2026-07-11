local WORGEN = 3
local LEVEL = 20

void OnFirstLogin(Player* player) override
{
    player->RemoveSpell(87840);
    player->RemoveSpell(68996);
}

function OnLevelChange(event, player, oldLevel)
    if oldLevel < LEVEL and player:GetLevel() >= LEVEL then
        if player:GetRace() == WORGEN then
            if not player:HasSpell(33388) then
                player:LearnSpell(33388)
            end

            if not player:HasSpell(87840) then
                player:LearnSpell(87840)
            end

            if not player:HasSpell(68996) then
                player:LearnSpell(68996)
            end
        end
    end
end

RegisterPlayerEvent(13, OnLevelChange)