-- spell: 0 inserts, 2 updates, 0 deletes

-- Change human form to Gilnean
UPDATE `spell` SET `effect_misc_value_a_1` = @GilneanMaleTemplate   WHERE `id` IN (@TwoFormsMale,   @HumanFormMale);
UPDATE `spell` SET `effect_misc_value_a_1` = @GilneanFemaleTemplate WHERE `id` IN (@TwoFormsFemale, @HumanFormFemale);
