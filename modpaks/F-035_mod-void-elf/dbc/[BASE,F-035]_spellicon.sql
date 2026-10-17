-- spellicon: 6 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `spellicon` WHERE `id` IN (
    @VoidElfMount1IconID,
    @VoidElfRacialIcon1, @VoidElfRacialIcon2, @VoidElfRacialIcon3, @VoidElfRacialIcon4, @VoidElfRacialIcon5
);
INSERT INTO `spellicon` (`id`, `name`) VALUES
(@VoidElfMount1IconID, @VoidElfMount1IconPath),
(@VoidElfRacialIcon1, @VoidElfRacialIcon1Path),
(@VoidElfRacialIcon2, @VoidElfRacialIcon2Path),
(@VoidElfRacialIcon3, @VoidElfRacialIcon3Path),
(@VoidElfRacialIcon4, @VoidElfRacialIcon4Path),
(@VoidElfRacialIcon5, @VoidElfRacialIcon5Path);
