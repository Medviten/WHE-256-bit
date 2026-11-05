-- [F-100] hero_class: opens everything that's limited by class to a Hero. A mask of 0 already means every class.

-- Every class's skills and spells. Both the core and the client's spellbook tabs read these.
UPDATE `skillraceclassinfo` SET `class_mask` = `class_mask` | @HeroMask WHERE `class_mask` != 0;
UPDATE `skilllineability` SET `required_classes` = `required_classes` | @HeroMask WHERE `required_classes` != 0;

-- Every class's talent trees. The client shows them three at a time, and pet trees have no class mask.
UPDATE `talenttab` SET `class_mask` = `class_mask` | @HeroMask WHERE `class_mask` != 0;
