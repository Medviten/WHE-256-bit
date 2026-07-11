DELETE FROM `skilllineability_dbc` WHERE `ID` IN (590, 592, 727, 3269, 3270, 3271, 3272, 3273, 3274, 5989, 5990, 5991, 5992, 5993, 5994, 13151, 14815, 14816,  14817, 14818, 15040, 15041, 15606, 15607, 16999, 17000, 17003, 17004, 20110, 20283, 20289, 20290, 21723, 21724, 21981, 21982, 21983, 21984, 21985, 21986, 21987, 21988, 21989, 31448, 13338, 14013, 20090, 20092, 31449, 31450, 31451, 31451, 31452, 110001, 110002, 110003, 110004, 110005, 110006, 110007);
INSERT INTO `skilllineability_dbc` (`ID`, `SkillLine`, `Spell`, `RaceMask`, `ClassMask`, `ExcludeRace`, `ExcludeClass`, `MinSkillLineRank`, `SupercededBySpell`, `AcquireMethod`, `TrivialSkillLineRankHigh`, `TrivialSkillLineRankLow`, `CharacterPoints_1`, `CharacterPoints_2`) VALUES
(590, 98, 668, 7245, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- Language Common
(592, 109, 669, 946, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- Language Orcish
(727, 137, 813, 4608, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- Language Thalassian
(3269, 237, 3565, 7245, 128, 0, 0, 1, 0, 0, 0, 0, 0, 0), -- Teleport: Darnassus
(3270, 237, 3562, 7245, 128, 0, 0, 1, 0, 0, 0, 0, 0, 0), -- Teleport: Ironforge
(3271, 237, 3567, 946, 128, 0, 0, 1, 0, 0, 0, 0, 0, 0), -- Teleport: Orgrimmar
(3272, 237, 3561, 7245, 128, 0, 0, 1, 0, 0, 0, 0, 0, 0), -- Teleport: Stormwind
(3273, 237, 3566, 946, 128, 0, 0, 1, 0, 0, 0, 0, 0, 0), -- Teleport: Thunder Bluff
(3274, 237, 3563, 946, 128, 0, 0, 1, 0, 0, 0, 0, 0, 0), -- Teleport: Undercity
(5989, 237, 11419, 7245, 128, 0, 0, 1, 0, 0, 0, 0, 0, 0), -- Portal: Darnassus
(5990, 237, 11416, 7245, 128, 0, 0, 1, 0, 0, 0, 0, 0, 0), -- Portal: Ironforge
(5991, 237, 11417, 946, 128, 0, 0, 1, 0, 0, 0, 0, 0, 0), -- Portal: Orgrimmar
(5992, 237, 10059, 7245, 128, 0, 0, 1, 0, 0, 0, 0, 0, 0), -- Portal: Stormwind
(5993, 237, 11420, 946, 128, 0, 0, 1, 0, 0, 0, 0, 0, 0), -- Portal: Thunder Bluff
(5994, 237, 11418, 946, 128, 0, 0, 1, 0, 0, 0, 0, 0, 0), -- Portal: Undercity
(13151, 373, 2825, 946, 64, 0, 0, 1, 0, 0, 0, 0, 0, 0), -- Bloodlust
(14815, 237, 32271, 7245, 128, 0, 0, 1, 0, 0, 0, 0, 0, 0), -- Teleport: Exodar
(14816, 237, 32272, 946, 128, 0, 0, 1, 0, 0, 0, 0, 0, 0), -- Teleport: Silvermoon
(14817, 237, 32266, 7245, 128, 0, 0, 1, 0, 0, 0, 0, 0, 0), -- Portal: Exodar
(14818, 237, 32267, 946, 128, 0, 0, 1, 0, 0, 0, 0, 0, 0), -- Portal: Silvermoon
(15040, 237, 33690, 7245, 128, 0, 0, 1, 0, 0, 0, 0, 0, 0), -- Teleport: Shattrath
(15041, 237, 33691, 7245, 128, 0, 0, 1, 0, 0, 0, 0, 0, 0), -- Portal: Shattrath
(15606, 237, 35715, 946, 128, 0, 0, 1, 0, 0, 0, 0, 0, 0), -- Teleport: Shattrath
(15607, 237, 35717, 946, 128, 0, 0, 1, 0, 0, 0, 0, 0, 0), -- Portal: Shattrath
(16999, 237, 49359, 7245, 128, 0, 0, 1, 0, 0, 0, 0, 0, 0), -- Teleport: Theramore
(17000, 237, 49358, 946, 128, 0, 0, 1, 0, 0, 0, 0, 0, 0), -- Teleport: Stonard
(17003, 237, 49361, 946, 128, 0, 0, 1, 0, 0, 0, 0, 0, 0), -- Portal: Stonard
(17004, 237, 49360, 7245, 128, 0, 0, 1, 0, 0, 0, 0, 0, 0), -- Portal: Theramore
(20110, 777, 55531, 946, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0), -- Mechano-hog
(20283, 777, 60424, 7245, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0), -- Mekgineer's Chopper
(20289, 202, 60867, 7245, 0, 0, 0, 1, 0, 0, 490, 480, 0, 0), -- Mekgineer's Chopper
(20290, 202, 60866, 946, 0, 0, 0, 1, 0, 0, 490, 480, 0, 0), -- Mechano-hog
(21723, 253, 75460, 8191, 8, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- removed?
(21724, 375, 75461, 8191, 64, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- Flame Shock Passive

/* Worgen Racials */
(21981, 789, 68975, 2048, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- Viciousness
(21982, 789, 68976, 2048, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- Aberration
(21983, 789, 68978, 2048, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- Flayer
(21984, 789, 68992, 2048, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- Darkflight
(31468, 789, 87840, 2048, 32, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- Running Wild
(31469, 789, 68996, 2048, 32, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- Two Forms

/* Goblin Racials */
(21985, 790, 69042, 256, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- Time is Money
(21986, 790, 69045, 256, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- Better Living Through Chemistry
(21987, 790, 69046, 256, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- Pack Hobgoblin
(21988, 790, 69070, 256, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- Rocket Jump
(21989, 790, 69041, 256, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- Rocket Barrage
(31448, 790, 69044, 256, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- Best Deals Anywhere

/* Returned these to Blood Elves alone. */
(13338, 756, 25046, 512, 8, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- Arcane Torrent (energy)
(14013, 756, 28730, 512, 470, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- Arcane Torrent (mana)
(31450, 756, 80866, 512, 1024, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- Arcane Torrent (Feral)
(31451, 756, 80867, 512, 1024, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- Arcane Torrent (Druid)
(31452, 756, 80868, 512, 1, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- Arcane Torrent (rage)

/* Made these Alliance only */
(12518, 594, 23214, 7245, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0), -- Warhorse (Alliance Paladin mount)
(7594, 594, 13819, 7245, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0), -- Charger (fast Alliance Paladin mount)
(20089, 777, 23214, 7245, 2, 0, 0, 1, 0, 0, 0, 0, 0), -- Warhorse (Alliance Paladin mount)
(20091, 777, 13819, 7245, 2, 0, 0, 1, 0, 0, 0, 0, 0), -- Charger (fast Alliance Paladin mount)

/* Made these Horde only */
(15253, 594, 34769, 946, 2, 0, 0, 1, 0, 0, 0, 0, 0), -- Thalassian Warhorse (Horde Paladin mount)
(15252, 594, 34767, 946, 2, 0, 0, 1, 0, 0, 0, 0, 0), -- Thalassian Charger (fast Horde Paladin mount)
(20092, 777, 34769, 946, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0), -- Thalassian Warhorse (Horde Paladin mount)
(20090, 777, 34767, 946, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0), -- Thalassian Charger (fast Horde Paladin mount)

/* New High Elf abilities. */
(31463, 791, 110005, 4096, 1503, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- Quel'dorei Meditation (rage, mana, energy)
(31464, 791, 110006, 4096, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- Swiftness of the Rangers
(31465, 791, 110007, 4096, 32, 0, 0, 1, 0, 2, 0, 0, 0, 0),  -- Quel'dorei Meditation (runic power)
(31466, 791, 110008, 4096, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0), -- Bow Specialization
(31467, 791, 110009, 4096, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0); -- Enchanting Specialization