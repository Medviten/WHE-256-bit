-- Start positions of @EluneChosenHome for every class the race offers (charbaseinfo, ARAC's included). Classes @EluneChosenHome lacks
-- start where its first class does; Death Knights start where its Death Knights do
DELETE FROM `playercreateinfo` WHERE `race` = @EluneChosen;
INSERT INTO `playercreateinfo` (`race`, `class`, `map`, `zone`, `position_x`, `position_y`, `position_z`, `orientation`)
SELECT @EluneChosen, `c`.`class`, `p`.`map`, `p`.`zone`, `p`.`position_x`, `p`.`position_y`, `p`.`position_z`, `p`.`orientation`
FROM (SELECT DISTINCT `class` FROM `dbc_db`.`charbaseinfo` WHERE `race` = @EluneChosen) AS `c`
JOIN `playercreateinfo` AS `p` ON `p`.`race` = @EluneChosenHome AND `p`.`class` = COALESCE(
    (SELECT `h`.`class` FROM `playercreateinfo` AS `h` WHERE `h`.`race` = @EluneChosenHome AND `h`.`class` = `c`.`class`),
    IF(`c`.`class` = @DeathKnight, NULL,
       (SELECT MIN(`h`.`class`) FROM `playercreateinfo` AS `h` WHERE `h`.`race` = @EluneChosenHome AND `h`.`class` <> @DeathKnight))
);
