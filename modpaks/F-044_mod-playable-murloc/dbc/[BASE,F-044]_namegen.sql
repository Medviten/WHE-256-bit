-- namegen: 32 inserts, 0 updates, 0 deletes
-- Murloc-ish names that pass the client name check (no three identical letters in a row, no apostrophes)

-- New entries
DELETE FROM `namegen` WHERE `race_id` = @Murloc;
SET @NameGenID = (SELECT COALESCE(MAX(id), 0) FROM `namegen`);
INSERT INTO `namegen` (`id`, `name`, `race_id`, `sex`) VALUES
(@NameGenID := @NameGenID +1, 'Mrgl',     @Murloc, @Male),
(@NameGenID := @NameGenID +1, 'Murky',    @Murloc, @Male),
(@NameGenID := @NameGenID +1, 'Gurky',    @Murloc, @Male),
(@NameGenID := @NameGenID +1, 'Grrgl',    @Murloc, @Male),
(@NameGenID := @NameGenID +1, 'Blurgl',   @Murloc, @Male),
(@NameGenID := @NameGenID +1, 'Murgle',   @Murloc, @Male),
(@NameGenID := @NameGenID +1, 'Flurgl',   @Murloc, @Male),
(@NameGenID := @NameGenID +1, 'Glurk',    @Murloc, @Male),
(@NameGenID := @NameGenID +1, 'Mrrgal',   @Murloc, @Male),
(@NameGenID := @NameGenID +1, 'Grimgel',  @Murloc, @Male),
(@NameGenID := @NameGenID +1, 'Burgl',    @Murloc, @Male),
(@NameGenID := @NameGenID +1, 'Skrlgl',   @Murloc, @Male),
(@NameGenID := @NameGenID +1, 'Gorrgl',   @Murloc, @Male),
(@NameGenID := @NameGenID +1, 'Murkeye',  @Murloc, @Male),
(@NameGenID := @NameGenID +1, 'Glubtok',  @Murloc, @Male),
(@NameGenID := @NameGenID +1, 'Mrrlok',   @Murloc, @Male),
(@NameGenID := @NameGenID +1, 'Mrgla',    @Murloc, @Female),
(@NameGenID := @NameGenID +1, 'Murla',    @Murloc, @Female),
(@NameGenID := @NameGenID +1, 'Gurgla',   @Murloc, @Female),
(@NameGenID := @NameGenID +1, 'Blubba',   @Murloc, @Female),
(@NameGenID := @NameGenID +1, 'Glimmra',  @Murloc, @Female),
(@NameGenID := @NameGenID +1, 'Sirrgla',  @Murloc, @Female),
(@NameGenID := @NameGenID +1, 'Flurgla',  @Murloc, @Female),
(@NameGenID := @NameGenID +1, 'Murrella', @Murloc, @Female),
(@NameGenID := @NameGenID +1, 'Glurpi',   @Murloc, @Female),
(@NameGenID := @NameGenID +1, 'Mrrbelle', @Murloc, @Female),
(@NameGenID := @NameGenID +1, 'Shelli',   @Murloc, @Female),
(@NameGenID := @NameGenID +1, 'Brinna',   @Murloc, @Female),
(@NameGenID := @NameGenID +1, 'Kelpie',   @Murloc, @Female),
(@NameGenID := @NameGenID +1, 'Gilla',    @Murloc, @Female),
(@NameGenID := @NameGenID +1, 'Splasha',  @Murloc, @Female),
(@NameGenID := @NameGenID +1, 'Mrrwa',    @Murloc, @Female);
