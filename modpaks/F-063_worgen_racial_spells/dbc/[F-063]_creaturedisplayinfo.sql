-- Remove the quadrupedal Running Wild displays added by F-024; Running Wild now mounts the Worgen's own display
DELETE FROM `creaturedisplayinfo` WHERE `id` IN (@WorgenWildMaleDisplay, @WorgenWildFemaleDisplay);
