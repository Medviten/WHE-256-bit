-- Remove the quadrupedal Running Wild models added by F-024; Running Wild now plays the Worgen models' own MountSelf anims
DELETE FROM `creaturemodeldata` WHERE `id` IN (@WorgenWildMaleModel, @WorgenWildFemaleModel);
