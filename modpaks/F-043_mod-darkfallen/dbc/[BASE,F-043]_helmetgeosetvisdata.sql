-- [F-043] mod-darkfallen: helmetgeosetvisdata: 0 inserts, 8 updates, 0 deletes

-- Changed values
UPDATE `helmetgeosetvisdata` SET `hide_geoset_5` = `hide_geoset_5` & ~@DarkfallenHelmetMask WHERE `id` = 246; -- -darkfallen
UPDATE `helmetgeosetvisdata` SET `hide_geoset_1` = `hide_geoset_1` |  @DarkfallenHelmetMask WHERE `id` = 285; -- +darkfallen
UPDATE `helmetgeosetvisdata` SET `hide_geoset_1` = `hide_geoset_1` |  @DarkfallenHelmetMask WHERE `id` = 305; -- +darkfallen
UPDATE `helmetgeosetvisdata` SET `hide_geoset_1` = `hide_geoset_1` |  @DarkfallenHelmetMask WHERE `id` = 306; -- +darkfallen
UPDATE `helmetgeosetvisdata` SET `hide_geoset_1` = `hide_geoset_1` |  @DarkfallenHelmetMask WHERE `id` = 307; -- +darkfallen
UPDATE `helmetgeosetvisdata` SET `hide_geoset_1` = `hide_geoset_1` |  @DarkfallenHelmetMask WHERE `id` = 345; -- +darkfallen
UPDATE `helmetgeosetvisdata` SET `hide_geoset_1` = `hide_geoset_1` |  @DarkfallenHelmetMask WHERE `id` = 366; -- +darkfallen
UPDATE `helmetgeosetvisdata` SET `hide_geoset_1` = `hide_geoset_1` |  @DarkfallenHelmetMask WHERE `id` = 367; -- +darkfallen

-- Mirroring blood elf, it looks like this bit should include darkfallen
UPDATE `helmetgeosetvisdata` SET `hide_geoset_6` = `hide_geoset_6` | @DarkfallenHelmetMask WHERE `id` = 376; -- +darkfallen
