/* Remove the Running Wild ranks added by F-024: 87840 is the only Running Wild spell left, with speed from riding skill */
DELETE FROM `spell_ranks` WHERE `first_spell_id` IN (@RunningWildMale60, @RunningWildFemale60);
