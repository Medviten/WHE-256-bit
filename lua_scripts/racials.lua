local function OnLevelChange(event, player, oldLevel)
    if oldLevel < LEVEL and player:GetLevel() >= 20 then
        if player:GetRace() == 12 then
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