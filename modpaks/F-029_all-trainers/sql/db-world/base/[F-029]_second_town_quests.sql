/* The second towns' new class trainers ([F-029]_second_town_trainers.sql, and Cataclysm's in zz_[AUTO,F-029]_*)
   also start their faction's level 10-20 class breadcrumbs, the quests the stock second-town trainers of their class
   give, which send the class on to its capital trainer or its next chain. Only the giver is added: the quests stay
   stock's, so their texts don't name the trainer (where the stock one does, as the night elf and human rogue letters,
   the generic dwarf one is used). ARAC (F-002) opens them to every race.
   Warlocks and priests get none: stock's second towns have no warlock quests, and their priest quests are local
   (Garments, which F-029 retires, Help Tavara, Cleansing the Scar). The hunters' Taming the Beast chains depend on the
   town's own beasts and rods, so aren't given here. */
DELETE FROM `creature_queststarter` WHERE `id` IN (142044, 142045, 142046, 142047, 142048, 142049, 142051, 142052,
  142053, 142054, 142055, 142057, 142058, 142059, 142060, 142061, 43464, 44380, 43013, 43012);
INSERT INTO `creature_queststarter` (`id`, `quest`) VALUES
-- Druid: Heeding the Call (Alliance to Darnassus, Horde to Thunder Bluff)
(142045, 5923), -- Faerin Dawnleaf, Goldshire
(142046, 5923), -- Theron Mossbrook, Kharanos
(142051, 5923), -- Ilthas Starbough, Azure Watch
(44380, 5926),  -- Jabul, Razor Hill
(142059, 5926), -- Halani Rainmane, Brill
(142061, 5926), -- Kaya Mistrunner, Falconwing Square
-- Shaman: Call of Fire (Alliance: Temper on Azuremyst; Horde: Kranal Fiss in the Barrens), Horde Call of Water
(142044, 9464), -- Haruun, Goldshire
(43464, 9464),  -- Halbin Frosthammer, Kharanos
(142048, 9464), -- Kaarun, Dolanaar
(142058, 2983), (142058, 2985), -- Dorgal Stormtongue, Brill
(142060, 2983), (142060, 2985), -- Throm Earthcaller, Falconwing Square
-- Paladin: Jol in the Exodar (Alliance), Knight-Lord Bloodvalor in Silvermoon (Horde)
(142047, 10366), -- Vaelura, Dolanaar
(142052, 9677),  -- Liriel Dawnward, Razor Hill
(43013, 9677),   -- Sunwalker Iopi, Bloodhoof Village
(142057, 9677),  -- Saelia Brightvow, Brill
-- Rogue: Road to Salvation / To Hulfdan! (Ironforge), Therzok / To Orgrimmar!
(142049, 2218), (142049, 2299), -- Elarion Duskstep, Azure Watch
(142054, 1859), (142054, 2380), -- Grutok, Bloodhoof Village
-- Mage: Speak with Anastasia / Report to Anastasia (Undercity)
(142053, 1881), (142053, 1959), -- Zun'jaka, Razor Hill
(142055, 1881), (142055, 1959), -- Aelynna Sunwhisper, Bloodhoof Village
-- Warrior: Speak with Dillinger (Brill)
(43012, 1818); -- Lothan Silverblade, Falconwing Square
