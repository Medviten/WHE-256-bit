-- [F-100] hero_class: trainer spells only a Hero gets, one `trainer` row per class. Trainer::GetHeroSpells adds them to
-- that class's trainers. They are what the class otherwise starts with (later ranks need them) or gets from its quests.
-- No creature uses these rows, and no other class can reach them, so stock classes still need their quests.

DELETE FROM `trainer_spell` WHERE `TrainerId` BETWEEN @HeroTrainerBase AND @HeroTrainerBase + 11;
DELETE FROM `trainer` WHERE `Id` BETWEEN @HeroTrainerBase AND @HeroTrainerBase + 11;

INSERT INTO `trainer` (`Id`, `Type`, `Requirement`, `Greeting`) VALUES
(@HeroTrainerBase + @Warrior, 0, @Hero, ''),
(@HeroTrainerBase + @Paladin, 0, @Hero, ''),
(@HeroTrainerBase + @Hunter, 0, @Hero, ''),
(@HeroTrainerBase + @Rogue, 0, @Hero, ''),
(@HeroTrainerBase + @Priest, 0, @Hero, ''),
(@HeroTrainerBase + @DeathKnight, 0, @Hero, ''),
(@HeroTrainerBase + @Shaman, 0, @Hero, ''),
(@HeroTrainerBase + @Mage, 0, @Hero, ''),
(@HeroTrainerBase + @Warlock, 0, @Hero, ''),
(@HeroTrainerBase + @Druid, 0, @Hero, '');

INSERT INTO `trainer_spell` (`TrainerId`, `SpellId`, `MoneyCost`, `ReqLevel`) VALUES
(@HeroTrainerBase + @Warrior, 78, 0, 1), -- Heroic Strike
(@HeroTrainerBase + @Warrior, 2457, 0, 1), -- Battle Stance
(@HeroTrainerBase + @Warrior, 107, 0, 1), -- Block
(@HeroTrainerBase + @Warrior, 71, 0, 10), -- Defensive Stance
(@HeroTrainerBase + @Warrior, 355, 0, 10), -- Taunt
(@HeroTrainerBase + @Warrior, 7386, 0, 10), -- Sunder Armor
(@HeroTrainerBase + @Warrior, 2458, 0, 30), -- Berserker Stance
(@HeroTrainerBase + @Paladin, 635, 0, 1), -- Holy Light
(@HeroTrainerBase + @Paladin, 20154, 0, 1), -- Seal of Righteousness
(@HeroTrainerBase + @Paladin, 7328, 0, 12), -- Redemption
(@HeroTrainerBase + @Hunter, 2973, 0, 1), -- Raptor Strike
(@HeroTrainerBase + @Hunter, 75, 0, 1), -- Auto Shot
(@HeroTrainerBase + @Hunter, 1515, 0, 10), -- Tame Beast
(@HeroTrainerBase + @Hunter, 883, 0, 10), -- Call Pet
(@HeroTrainerBase + @Hunter, 982, 0, 10), -- Revive Pet
(@HeroTrainerBase + @Hunter, 6991, 0, 10), -- Feed Pet
(@HeroTrainerBase + @Hunter, 2641, 0, 10), -- Dismiss Pet
(@HeroTrainerBase + @Rogue, 1752, 0, 1), -- Sinister Strike
(@HeroTrainerBase + @Rogue, 2098, 0, 1), -- Eviscerate
(@HeroTrainerBase + @Priest, 2050, 0, 1), -- Lesser Heal
(@HeroTrainerBase + @Priest, 585, 0, 1), -- Smite
(@HeroTrainerBase + @DeathKnight, 45902, 0, 55), -- Blood Strike
(@HeroTrainerBase + @DeathKnight, 48266, 0, 55), -- Blood Presence
(@HeroTrainerBase + @DeathKnight, 45477, 0, 55), -- Icy Touch
(@HeroTrainerBase + @DeathKnight, 45462, 0, 55), -- Plague Strike
(@HeroTrainerBase + @DeathKnight, 47541, 0, 55), -- Death Coil
(@HeroTrainerBase + @DeathKnight, 49576, 0, 55), -- Death Grip
(@HeroTrainerBase + @DeathKnight, 50977, 0, 55), -- Death Gate
(@HeroTrainerBase + @DeathKnight, 53428, 0, 55), -- Runeforging
(@HeroTrainerBase + @Shaman, 331, 0, 1), -- Healing Wave
(@HeroTrainerBase + @Shaman, 403, 0, 1), -- Lightning Bolt
(@HeroTrainerBase + @Shaman, 8071, 0, 4), -- Stoneskin Totem
(@HeroTrainerBase + @Shaman, 3599, 0, 10), -- Searing Totem
(@HeroTrainerBase + @Shaman, 5394, 0, 20), -- Healing Stream Totem
(@HeroTrainerBase + @Mage, 133, 0, 1), -- Fireball
(@HeroTrainerBase + @Mage, 168, 0, 1), -- Frost Armor
(@HeroTrainerBase + @Warlock, 686, 0, 1), -- Shadow Bolt
(@HeroTrainerBase + @Warlock, 687, 0, 1), -- Demon Skin
(@HeroTrainerBase + @Warlock, 697, 0, 10), -- Summon Voidwalker
(@HeroTrainerBase + @Warlock, 712, 0, 20), -- Summon Succubus
(@HeroTrainerBase + @Warlock, 691, 0, 30), -- Summon Felhunter
(@HeroTrainerBase + @Warlock, 1122, 0, 50), -- Inferno
(@HeroTrainerBase + @Warlock, 18540, 0, 60), -- Ritual of Doom
(@HeroTrainerBase + @Druid, 5176, 0, 1), -- Wrath
(@HeroTrainerBase + @Druid, 5185, 0, 1), -- Healing Touch
(@HeroTrainerBase + @Druid, 5487, 0, 10), -- Bear Form
(@HeroTrainerBase + @Druid, 6807, 0, 10), -- Maul
(@HeroTrainerBase + @Druid, 6795, 0, 10), -- Growl
(@HeroTrainerBase + @Druid, 8946, 0, 14); -- Cure Poison
