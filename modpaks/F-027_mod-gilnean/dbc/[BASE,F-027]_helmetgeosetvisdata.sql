-- Copy human, so helmets hide hair and ears on the altered form as they do on a human (this DBC indexes by race id itself)
UPDATE `helmetgeosetvisdata` SET `hide_geoset_1` = `hide_geoset_1` | @GilneanHelmetMask WHERE `hide_geoset_1` & @HumanHelmetMask;
UPDATE `helmetgeosetvisdata` SET `hide_geoset_2` = `hide_geoset_2` | @GilneanHelmetMask WHERE `hide_geoset_2` & @HumanHelmetMask;
UPDATE `helmetgeosetvisdata` SET `hide_geoset_3` = `hide_geoset_3` | @GilneanHelmetMask WHERE `hide_geoset_3` & @HumanHelmetMask;
UPDATE `helmetgeosetvisdata` SET `hide_geoset_4` = `hide_geoset_4` | @GilneanHelmetMask WHERE `hide_geoset_4` & @HumanHelmetMask;
UPDATE `helmetgeosetvisdata` SET `hide_geoset_5` = `hide_geoset_5` | @GilneanHelmetMask WHERE `hide_geoset_5` & @HumanHelmetMask;
UPDATE `helmetgeosetvisdata` SET `hide_geoset_6` = `hide_geoset_6` | @GilneanHelmetMask WHERE `hide_geoset_6` & @HumanHelmetMask;
