-- Start positions of @StormforgedHome for every class the race offers (charbaseinfo, ARAC's included). Classes @StormforgedHome lacks
-- start where its first class does; Death Knights start where its Death Knights do
DELETE FROM `playercreateinfo` WHERE `race` = @Stormforged;
INSERT INTO `playercreateinfo` (`race`, `class`, `map`, `zone`, `position_x`, `position_y`, `position_z`, `orientation`)
SELECT @Stormforged, `c`.`class`, `p`.`map`, `p`.`zone`, `p`.`position_x`, `p`.`position_y`, `p`.`position_z`, `p`.`orientation`
FROM (SELECT DISTINCT `class` FROM `dbc_db`.`charbaseinfo` WHERE `race` = @Stormforged) AS `c`
JOIN `playercreateinfo` AS `p` ON `p`.`race` = @StormforgedHome AND `p`.`class` = COALESCE(
    (SELECT `h`.`class` FROM `playercreateinfo` AS `h` WHERE `h`.`race` = @StormforgedHome AND `h`.`class` = `c`.`class`),
    IF(`c`.`class` = @DeathKnight, NULL,
       (SELECT MIN(`h`.`class`) FROM `playercreateinfo` AS `h` WHERE `h`.`race` = @StormforgedHome AND `h`.`class` <> @DeathKnight))
);
