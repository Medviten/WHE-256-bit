-- Copy human
UPDATE `helmetgeosetvisdata` SET `hide_geoset_1` = `hide_geoset_1` | @Gilnean WHERE `hide_geoset_1` & @HumanMask;
UPDATE `helmetgeosetvisdata` SET `hide_geoset_2` = `hide_geoset_2` | @Gilnean WHERE `hide_geoset_2` & @HumanMask;
UPDATE `helmetgeosetvisdata` SET `hide_geoset_3` = `hide_geoset_3` | @Gilnean WHERE `hide_geoset_3` & @HumanMask;
UPDATE `helmetgeosetvisdata` SET `hide_geoset_4` = `hide_geoset_4` | @Gilnean WHERE `hide_geoset_4` & @HumanMask;
UPDATE `helmetgeosetvisdata` SET `hide_geoset_5` = `hide_geoset_5` | @Gilnean WHERE `hide_geoset_5` & @HumanMask;
UPDATE `helmetgeosetvisdata` SET `hide_geoset_6` = `hide_geoset_6` | @Gilnean WHERE `hide_geoset_6` & @HumanMask;
