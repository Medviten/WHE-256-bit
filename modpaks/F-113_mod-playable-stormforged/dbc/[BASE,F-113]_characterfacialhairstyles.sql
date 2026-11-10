-- characterfacialhairstyles: 2 inserts, 0 updates, 0 deletes (from the skin colours (option 0) of CoA's appearance catalog EsteriaStormforged.bin)

-- New entries
DELETE FROM `characterfacialhairstyles` WHERE `race` = @Stormforged;
INSERT INTO `characterfacialhairstyles` (`race`, `gender`, `variation_id`, `geoset_1`, `geoset_2`, `geoset_3`, `geoset_4`, `geoset_5`) VALUES
(@Stormforged, @Male,    0, 0, 0, 0, 0, 0),
(@Stormforged, @Female,  0, 0, 0, 0, 0, 0);
