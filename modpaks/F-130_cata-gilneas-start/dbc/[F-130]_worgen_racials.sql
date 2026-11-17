-- [F-130] Worgen learn their racials in Gilneas
--
-- As in Cataclysm, only Death Knights learn the Worgen racials and Two Forms with the racial skill line (F-024's rows).
-- The others start as humans (Human Form, cast by gilneas_start.cpp until "Last Stand" is rewarded) and are taught
-- Viciousness, Aberration, Flayer and Darkflight when Last Stand's cutscene turns them (also gilneas_start.cpp), and
-- Two Forms by "Neither Human Nor Beast" (24593: 72829 forcecasts 72857, Learn Two Forms). Running Wild stays
-- src/Worgoblin.cpp's, at level 20.

UPDATE `skilllineability` SET `required_classes` = @DeathKnightMask
WHERE `id` IN (@WorgenSkillLineAbility1, @WorgenSkillLineAbility2, @WorgenSkillLineAbility3, @WorgenSkillLineAbility4,
               @WorgenSkillLineAbility6);
