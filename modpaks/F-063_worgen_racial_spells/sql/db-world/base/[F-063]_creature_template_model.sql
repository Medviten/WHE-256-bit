/* Remove the models of the Running Wild transform NPCs added by F-024 */
DELETE FROM `creature_template_model` WHERE `CreatureID` IN (@WorgenWildMaleCreatureID, @WorgenWildFemaleCreatureID);
