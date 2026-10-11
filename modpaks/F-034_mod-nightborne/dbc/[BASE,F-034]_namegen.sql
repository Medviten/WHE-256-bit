-- namegen: 24 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `namegen` WHERE `race_id` = @Nightborne;
SET @NameGenID = (SELECT COALESCE(MAX(id), 0) FROM `namegen`);
INSERT INTO `namegen` (`id`, `name`, `race_id`, `sex`) VALUES
(@NameGenID := @NameGenID +1, 'Grok',    @Nightborne, @Male),
(@NameGenID := @NameGenID +1, 'Mogor',   @Nightborne, @Male),
(@NameGenID := @NameGenID +1, 'Tharg',   @Nightborne, @Male),
(@NameGenID := @NameGenID +1, 'Krol',    @Nightborne, @Male),
(@NameGenID := @NameGenID +1, 'Gorlash', @Nightborne, @Male),
(@NameGenID := @NameGenID +1, 'Brugor',  @Nightborne, @Male),
(@NameGenID := @NameGenID +1, 'Dorgok',  @Nightborne, @Male),
(@NameGenID := @NameGenID +1, 'Krosh',   @Nightborne, @Male),
(@NameGenID := @NameGenID +1, 'Grimnok', @Nightborne, @Male),
(@NameGenID := @NameGenID +1, 'Lunk',    @Nightborne, @Male),
(@NameGenID := @NameGenID +1, 'Urok',    @Nightborne, @Male),
(@NameGenID := @NameGenID +1, 'Zorbo',   @Nightborne, @Male),
(@NameGenID := @NameGenID +1, 'Chogara', @Nightborne, @Female),
(@NameGenID := @NameGenID +1, 'Mogra',   @Nightborne, @Female),
(@NameGenID := @NameGenID +1, 'Urda',    @Nightborne, @Female),
(@NameGenID := @NameGenID +1, 'Grulla',  @Nightborne, @Female),
(@NameGenID := @NameGenID +1, 'Zogra',   @Nightborne, @Female),
(@NameGenID := @NameGenID +1, 'Karga',   @Nightborne, @Female),
(@NameGenID := @NameGenID +1, 'Maghara', @Nightborne, @Female),
(@NameGenID := @NameGenID +1, 'Brogga',  @Nightborne, @Female),
(@NameGenID := @NameGenID +1, 'Gorma',   @Nightborne, @Female),
(@NameGenID := @NameGenID +1, 'Hargala', @Nightborne, @Female),
(@NameGenID := @NameGenID +1, 'Thokra',  @Nightborne, @Female),
(@NameGenID := @NameGenID +1, 'Wulgra',  @Nightborne, @Female);
