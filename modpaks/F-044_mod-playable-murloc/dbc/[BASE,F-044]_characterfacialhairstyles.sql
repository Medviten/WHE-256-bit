-- characterfacialhairstyles: 2 inserts, 0 updates, 0 deletes (donor client: none)

-- New entries
DELETE FROM `characterfacialhairstyles` WHERE `race` = @Murloc;
INSERT INTO `characterfacialhairstyles` (`race`, `gender`, `variation_id`, `geoset_1`, `geoset_2`, `geoset_3`, `geoset_4`, `geoset_5`) VALUES
(@Murloc, @Male,   0, 0, 0, 0, 0, 0),
(@Murloc, @Female, 0, 0, 0, 0, 0, 0);
