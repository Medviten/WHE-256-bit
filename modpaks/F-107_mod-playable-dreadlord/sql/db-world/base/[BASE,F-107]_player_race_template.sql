/* The stock races this race copies, see F-091_race-setup. exiles_reach 0: keeps its home race's start with F-137 on */
DELETE FROM `player_race_template` WHERE `race` = @Dreadlord;
INSERT INTO `player_race_template` (`race`, `home_race`, `kin_race`, `shapeshift_skin_color`, `exiles_reach`) VALUES
(@Dreadlord, @Orc, @Undead, 0, 0);
