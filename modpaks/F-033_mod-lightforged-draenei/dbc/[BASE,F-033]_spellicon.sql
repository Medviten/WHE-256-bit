-- spellicon: 8 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `spellicon` WHERE `id` IN (
    @LightforgedDraeneiMount1IconID, @LightforgedDraeneiMount2IconID, @LightforgedDraeneiMount3IconID,
    @LightforgedDraeneiRacialIcon1, @LightforgedDraeneiRacialIcon2,
    @LightforgedDraeneiRacialIcon4, @LightforgedDraeneiRacialIcon5, @LightforgedDraeneiRacialIcon6
);
INSERT INTO `spellicon` (`id`, `name`) VALUES
(@LightforgedDraeneiMount1IconID, @LightforgedDraeneiMount1IconPath), -- also used by @LightforgedDraeneiMount4IconID
(@LightforgedDraeneiMount2IconID, @LightforgedDraeneiMount2IconPath),
(@LightforgedDraeneiMount3IconID, @LightforgedDraeneiMount3IconPath),
(@LightforgedDraeneiRacialIcon1,  @LightforgedDraeneiRacialIcon1Path),
(@LightforgedDraeneiRacialIcon2,  @LightforgedDraeneiRacialIcon2Path), -- also used by @LightforgedDraeneiRacialIcon3
(@LightforgedDraeneiRacialIcon4,  @LightforgedDraeneiRacialIcon4Path),
(@LightforgedDraeneiRacialIcon5,  @LightforgedDraeneiRacialIcon5Path),
(@LightforgedDraeneiRacialIcon6,  @LightforgedDraeneiRacialIcon6Path);
