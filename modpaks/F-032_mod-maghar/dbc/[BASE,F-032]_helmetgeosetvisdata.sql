-- [F-032] mod-maghar: helmetgeosetvisdata: 0 inserts, 11 updates, 0 deletes

-- Changed values
UPDATE `helmetgeosetvisdata` SET `hide_geoset_4` = `hide_geoset_4` | 16384 WHERE `id` = 246; -- +mag'har orc
UPDATE `helmetgeosetvisdata` SET `hide_geoset_5` = `hide_geoset_5` & ~16384 WHERE `id` = 265; -- -mag'har orc
UPDATE `helmetgeosetvisdata` SET `hide_geoset_1` = `hide_geoset_1` | 16384, `hide_geoset_2` = `hide_geoset_2` | 16384, `hide_geoset_3` = `hide_geoset_3` | 16384, `hide_geoset_4` = `hide_geoset_4` | 16384, `hide_geoset_5` = `hide_geoset_5` | 16384 WHERE `id` = 285;
UPDATE `helmetgeosetvisdata` SET `hide_geoset_1` = `hide_geoset_1` | 16384, `hide_geoset_4` = `hide_geoset_4` | 16384 WHERE `id` = 305;
UPDATE `helmetgeosetvisdata` SET `hide_geoset_1` = `hide_geoset_1` | 16384, `hide_geoset_2` = `hide_geoset_2` | 16384, `hide_geoset_3` = `hide_geoset_3` | 16384, `hide_geoset_4` = `hide_geoset_4` | 16384, `hide_geoset_5` = `hide_geoset_5` | 16384 WHERE `id` = 306;
UPDATE `helmetgeosetvisdata` SET `hide_geoset_1` = `hide_geoset_1` | 16384, `hide_geoset_4` = `hide_geoset_4` | 16384, `hide_geoset_5` = `hide_geoset_5` | 16384 WHERE `id` = 307;
UPDATE `helmetgeosetvisdata` SET `hide_geoset_1` = `hide_geoset_1` | 16384, `hide_geoset_4` = `hide_geoset_4` | 16384 WHERE `id` = 325;
UPDATE `helmetgeosetvisdata` SET `hide_geoset_1` = `hide_geoset_1` | 16384, `hide_geoset_3` = `hide_geoset_3` | 16384, `hide_geoset_4` = `hide_geoset_4` | 16384, `hide_geoset_5` = `hide_geoset_5` | 16384 WHERE `id` = 345;
UPDATE `helmetgeosetvisdata` SET `hide_geoset_1` = `hide_geoset_1` | 16384, `hide_geoset_4` = `hide_geoset_4` | 16384 WHERE `id` = 366;
UPDATE `helmetgeosetvisdata` SET `hide_geoset_1` = `hide_geoset_1` | 16384, `hide_geoset_4` = `hide_geoset_4` | 16384 WHERE `id` = 367;
UPDATE `helmetgeosetvisdata` SET `hide_geoset_4` = `hide_geoset_4` | 16384 WHERE `id` = 376;
