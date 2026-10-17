-- [F-005] mod-azerothcore-high-elf: helmetgeosetvisdata: 0 inserts, 8 updates, 0 deletes

-- Changed values
UPDATE `helmetgeosetvisdata` SET `hide_geoset_5` = `hide_geoset_5` & ~@VoidElfHelmetMask WHERE `id` = 246; -- -high elf
UPDATE `helmetgeosetvisdata` SET `hide_geoset_1` = `hide_geoset_1` |  @VoidElfHelmetMask WHERE `id` = 285; -- +high elf
UPDATE `helmetgeosetvisdata` SET `hide_geoset_1` = `hide_geoset_1` |  @VoidElfHelmetMask WHERE `id` = 305; -- +high elf
UPDATE `helmetgeosetvisdata` SET `hide_geoset_1` = `hide_geoset_1` |  @VoidElfHelmetMask WHERE `id` = 306; -- +high elf
UPDATE `helmetgeosetvisdata` SET `hide_geoset_1` = `hide_geoset_1` |  @VoidElfHelmetMask WHERE `id` = 307; -- +high elf
UPDATE `helmetgeosetvisdata` SET `hide_geoset_1` = `hide_geoset_1` |  @VoidElfHelmetMask WHERE `id` = 345; -- +high elf
UPDATE `helmetgeosetvisdata` SET `hide_geoset_1` = `hide_geoset_1` |  @VoidElfHelmetMask WHERE `id` = 366; -- +high elf
UPDATE `helmetgeosetvisdata` SET `hide_geoset_1` = `hide_geoset_1` |  @VoidElfHelmetMask WHERE `id` = 367; -- +high elf

-- Mirroring blood elf, it looks like this bit should include high elf
UPDATE `helmetgeosetvisdata` SET `hide_geoset_6` = `hide_geoset_6` | @VoidElfHelmetMask WHERE `id` = 376; -- +high elf
