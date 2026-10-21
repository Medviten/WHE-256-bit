-- helmetgeosetvisdata: 0 inserts, 27 updates, 0 deletes
-- Taken from Kalibros' Vrykul DBCs (race 16): only the cells where the Vrykul bit differs from stock

-- Changed values
UPDATE `helmetgeosetvisdata` SET `hide_geoset_1` = `hide_geoset_1` & ~@VrykulHelmetMask WHERE `id` = 249; -- -vrykul
UPDATE `helmetgeosetvisdata` SET `hide_geoset_1` = `hide_geoset_1` & ~@VrykulHelmetMask WHERE `id` = 265; -- -vrykul
UPDATE `helmetgeosetvisdata` SET `hide_geoset_5` = `hide_geoset_5` & ~@VrykulHelmetMask WHERE `id` = 265; -- -vrykul
UPDATE `helmetgeosetvisdata` SET `hide_geoset_1` = `hide_geoset_1` |  @VrykulHelmetMask WHERE `id` = 285; -- +vrykul
UPDATE `helmetgeosetvisdata` SET `hide_geoset_2` = `hide_geoset_2` |  @VrykulHelmetMask WHERE `id` = 285; -- +vrykul
UPDATE `helmetgeosetvisdata` SET `hide_geoset_3` = `hide_geoset_3` |  @VrykulHelmetMask WHERE `id` = 285; -- +vrykul
UPDATE `helmetgeosetvisdata` SET `hide_geoset_4` = `hide_geoset_4` |  @VrykulHelmetMask WHERE `id` = 285; -- +vrykul
UPDATE `helmetgeosetvisdata` SET `hide_geoset_5` = `hide_geoset_5` |  @VrykulHelmetMask WHERE `id` = 285; -- +vrykul
UPDATE `helmetgeosetvisdata` SET `hide_geoset_1` = `hide_geoset_1` |  @VrykulHelmetMask WHERE `id` = 305; -- +vrykul
UPDATE `helmetgeosetvisdata` SET `hide_geoset_1` = `hide_geoset_1` |  @VrykulHelmetMask WHERE `id` = 306; -- +vrykul
UPDATE `helmetgeosetvisdata` SET `hide_geoset_2` = `hide_geoset_2` |  @VrykulHelmetMask WHERE `id` = 306; -- +vrykul
UPDATE `helmetgeosetvisdata` SET `hide_geoset_3` = `hide_geoset_3` |  @VrykulHelmetMask WHERE `id` = 306; -- +vrykul
UPDATE `helmetgeosetvisdata` SET `hide_geoset_4` = `hide_geoset_4` |  @VrykulHelmetMask WHERE `id` = 306; -- +vrykul
UPDATE `helmetgeosetvisdata` SET `hide_geoset_5` = `hide_geoset_5` |  @VrykulHelmetMask WHERE `id` = 306; -- +vrykul
UPDATE `helmetgeosetvisdata` SET `hide_geoset_1` = `hide_geoset_1` |  @VrykulHelmetMask WHERE `id` = 307; -- +vrykul
UPDATE `helmetgeosetvisdata` SET `hide_geoset_5` = `hide_geoset_5` |  @VrykulHelmetMask WHERE `id` = 307; -- +vrykul
UPDATE `helmetgeosetvisdata` SET `hide_geoset_1` = `hide_geoset_1` |  @VrykulHelmetMask WHERE `id` = 325; -- +vrykul
UPDATE `helmetgeosetvisdata` SET `hide_geoset_4` = `hide_geoset_4` |  @VrykulHelmetMask WHERE `id` = 325; -- +vrykul
UPDATE `helmetgeosetvisdata` SET `hide_geoset_1` = `hide_geoset_1` |  @VrykulHelmetMask WHERE `id` = 345; -- +vrykul
UPDATE `helmetgeosetvisdata` SET `hide_geoset_3` = `hide_geoset_3` |  @VrykulHelmetMask WHERE `id` = 345; -- +vrykul
UPDATE `helmetgeosetvisdata` SET `hide_geoset_5` = `hide_geoset_5` |  @VrykulHelmetMask WHERE `id` = 345; -- +vrykul
UPDATE `helmetgeosetvisdata` SET `hide_geoset_1` = `hide_geoset_1` |  @VrykulHelmetMask WHERE `id` = 366; -- +vrykul
UPDATE `helmetgeosetvisdata` SET `hide_geoset_1` = `hide_geoset_1` |  @VrykulHelmetMask WHERE `id` = 367; -- +vrykul
UPDATE `helmetgeosetvisdata` SET `hide_geoset_4` = `hide_geoset_4` |  @VrykulHelmetMask WHERE `id` = 367; -- +vrykul
UPDATE `helmetgeosetvisdata` SET `hide_geoset_2` = `hide_geoset_2` |  @VrykulHelmetMask WHERE `id` = 369; -- +vrykul
UPDATE `helmetgeosetvisdata` SET `hide_geoset_3` = `hide_geoset_3` |  @VrykulHelmetMask WHERE `id` = 369; -- +vrykul
UPDATE `helmetgeosetvisdata` SET `hide_geoset_4` = `hide_geoset_4` |  @VrykulHelmetMask WHERE `id` = 369; -- +vrykul
