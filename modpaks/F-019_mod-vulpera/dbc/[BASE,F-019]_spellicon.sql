-- spellicon: 7 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `spellicon` WHERE `id` IN (
    @IconAlpacaSaddlebags, @IconBagOfTricks, @IconFireResistance, @IconMakeCamp, @IconNoseForTrouble, @IconReturnToCamp, @IconRummageYourBag
);
INSERT INTO `spellicon` (`id`, `name`) VALUES
(@IconAlpacaSaddlebags, 'Interface\\Icons\\ability_racial_rummageyourbag'),
(@IconBagOfTricks,      'Interface\\Icons\\ability_racial_bagoftricks'),
(@IconFireResistance,   'Interface\\Icons\\ability_racial_fireresist'),
(@IconMakeCamp,         'Interface\\Icons\\ability_racial_makecamp'),
(@IconNoseForTrouble,   'Interface\\Icons\\ability_racial_nosefortrouble'),
(@IconReturnToCamp,     'Interface\\Icons\\ability_racial_returntocamp'),
(@IconRummageYourBag,   'Interface\\Icons\\ability_racial_vulperasurvivalkit');
