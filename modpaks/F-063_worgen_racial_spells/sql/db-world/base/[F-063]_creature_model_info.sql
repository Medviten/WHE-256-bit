/* Remove model info for the Running Wild displays added by F-024 */
DELETE FROM `creature_model_info` WHERE `DisplayID` IN (@WorgenWildMaleDisplay, @WorgenWildFemaleDisplay);
