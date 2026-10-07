/* Add two ranks for Running Wild */
DELETE FROM `spell_ranks` WHERE `first_spell_id` IN (@RunningWildMale60, @RunningWildFemale60);
INSERT INTO `spell_ranks` (`first_spell_id`, `spell_id`, `rank`) VALUES
(@RunningWildMale60, @RunningWildMale60, 1), -- baseline
(@RunningWildMale60, @RunningWildMale100, 2), -- upgrade
(@RunningWildFemale60, @RunningWildFemale60, 1), -- baseline
(@RunningWildFemale60, @RunningWildFemale100, 2); -- upgrade
