-- spellicon: 3 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `spellicon` WHERE `id` IN (
    @IconDarkflight, @IconWorgenAchievement, @IconRunningWild
);
INSERT INTO `spellicon` (`id`, `name`) VALUES
(@IconDarkflight, 'Interface\\Icons\\ability_racial_darkflight'),
(@IconWorgenAchievement, 'Interface\\Icons\\achievement_worganhead'),
(@IconRunningWild, 'Interface\\Icons\\ability_racial_runningwild');
