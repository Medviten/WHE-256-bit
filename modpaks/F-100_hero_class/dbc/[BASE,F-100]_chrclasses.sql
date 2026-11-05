-- [F-100] hero_class: chrclasses: 1 insert, a copy of Paladin with its own name and token

DELETE FROM `chrclasses` WHERE `id` = @Hero;
DROP TEMPORARY TABLE IF EXISTS `hero_chrclass`;
CREATE TEMPORARY TABLE `hero_chrclass` SELECT * FROM `chrclasses` WHERE `id` = @Paladin;
UPDATE `hero_chrclass` SET
    `id` = @Hero,
    `file_name` = 'HERO',
    `spell_class_set` = 0, -- no family of its own: the client reads a Hero's modifiers per spell family instead
    `name_enus` = 'Hero', `name_female_enus` = 'Hero', `name_male_enus` = 'Hero',
    `name_kokr` = '', `name_frfr` = '', `name_dede` = '', `name_zhcn` = '', `name_zhtw` = '', `name_eses` = '', `name_esmx` = '', `name_ruru` = '',
    `name_female_kokr` = '', `name_female_frfr` = '', `name_female_dede` = '', `name_female_zhcn` = '', `name_female_zhtw` = '', `name_female_eses` = '', `name_female_esmx` = '', `name_female_ruru` = '',
    `name_male_kokr` = '', `name_male_frfr` = '', `name_male_dede` = '', `name_male_zhcn` = '', `name_male_zhtw` = '', `name_male_eses` = '', `name_male_esmx` = '', `name_male_ruru` = '';
INSERT INTO `chrclasses` SELECT * FROM `hero_chrclass`;
DROP TEMPORARY TABLE `hero_chrclass`;
