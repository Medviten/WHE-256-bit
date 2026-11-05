-- [F-100] hero_class: charbaseinfo: Hero for every playable race (keep after the race modpaks)

DELETE FROM `charbaseinfo` WHERE `class` = @Hero;
INSERT INTO `charbaseinfo` (`race`, `class`) SELECT DISTINCT `race`, @Hero FROM `charbaseinfo`;
