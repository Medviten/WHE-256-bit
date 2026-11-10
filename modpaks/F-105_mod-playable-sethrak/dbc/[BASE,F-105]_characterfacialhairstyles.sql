-- characterfacialhairstyles: 2 inserts, 0 updates, 0 deletes (from the skin colours (option 0) of CoA's appearance catalog EsteriaSethrak.bin)

-- New entries
DELETE FROM `characterfacialhairstyles` WHERE `race` = @Sethrak;
INSERT INTO `characterfacialhairstyles` (`race`, `gender`, `variation_id`, `geoset_1`, `geoset_2`, `geoset_3`, `geoset_4`, `geoset_5`) VALUES
(@Sethrak, @Male,    0, 0, 0, 0, 0, 0),
(@Sethrak, @Female,  0, 0, 0, 0, 0, 0);
