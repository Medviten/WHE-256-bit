-- Action bars of @TuskarrHome
DELETE FROM `playercreateinfo_action` WHERE `race` = @Tuskarr;
INSERT INTO `playercreateinfo_action` (`race`, `class`, `button`, `action`, `type`)
SELECT @Tuskarr, `class`, `button`, `action`, `type`
FROM (SELECT * FROM `playercreateinfo_action` WHERE `race` = @TuskarrHome) AS `home`;
