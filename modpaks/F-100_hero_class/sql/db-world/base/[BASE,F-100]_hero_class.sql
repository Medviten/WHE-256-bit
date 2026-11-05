-- [F-100] hero_class: the class itself. Keep after the race modpaks, F-002 and anything that moves a race's start.

-- Base stats and mana are Paladin's
DELETE FROM `player_class_stats` WHERE `Class` = @Hero;
INSERT INTO `player_class_stats` (`Class`, `Level`, `BaseHP`, `BaseMana`, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit`)
SELECT @Hero, `Level`, `BaseHP`, `BaseMana`, `Strength`, `Agility`, `Stamina`, `Intellect`, `Spirit` FROM `player_class_stats` WHERE `Class` = @Paladin;

-- Starts where its race's other classes do (Death Knights start somewhere else)
DELETE FROM `playercreateinfo` WHERE `class` = @Hero;
INSERT INTO `playercreateinfo` (`race`, `class`, `map`, `zone`, `position_x`, `position_y`, `position_z`, `orientation`)
SELECT p.`race`, @Hero, p.`map`, p.`zone`, p.`position_x`, p.`position_y`, p.`position_z`, p.`orientation`
FROM `playercreateinfo` p
INNER JOIN (SELECT `race`, MIN(`class`) AS `first_class` FROM `playercreateinfo` WHERE `class` != @DeathKnight AND `class` != @Hero GROUP BY `race`) f
    ON p.`race` = f.`race` AND p.`class` = f.`first_class`;

-- Everything else on the bar comes from trainers
DELETE FROM `playercreateinfo_action` WHERE `class` = @Hero;
INSERT INTO `playercreateinfo_action` (`race`, `class`, `button`, `action`, `type`)
SELECT `race`, @Hero, @Row1Button1, @SpellAutoAttack, @ActionbarSpell FROM `playercreateinfo` WHERE `class` = @Hero;

-- On top of what every class starts with (Defense, Unarmed, Cloth, ...). The rest comes from weapon masters and class
-- trainers, as for anyone: Mail from a Hunter or Shaman trainer at 40, Plate from a Warrior or Paladin trainer at 40.
DELETE FROM `playercreateinfo_skills` WHERE `classMask` = @HeroMask;
INSERT INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(0, @HeroMask,  43, 0, 'Hero - Swords'),
(0, @HeroMask, 414, 0, 'Hero - Leather'),
(0, @HeroMask, 433, 0, 'Hero - Shield');

-- Gossip that depends on the class, e.g. a class trainer's offer to train you
UPDATE IGNORE `conditions` SET `ConditionValue1` = `ConditionValue1` | @HeroMask
WHERE `SourceTypeOrReferenceId` IN (14, 15) AND `ConditionTypeOrReference` = 15 AND `ConditionValue1` != 0;
