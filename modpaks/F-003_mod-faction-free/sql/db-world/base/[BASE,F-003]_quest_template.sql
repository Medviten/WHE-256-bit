/*This will update the quest_template table to allow all races to have access to all quests.*/
UPDATE `quest_template` SET `AllowableRaces` = @PlayableRaceMask,
    `AllowableRaces_2` = @PlayableRaceMask_2 WHERE (`AllowableRaces` & @BaseAllianceMask) OR (`AllowableRaces` & @BaseHordeMask);
