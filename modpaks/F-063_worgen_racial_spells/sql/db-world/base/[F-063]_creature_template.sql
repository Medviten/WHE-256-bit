/* Remove the Running Wild transform NPCs added by F-024 */
DELETE FROM `creature_template` WHERE `entry` IN (@WorgenWildMaleCreatureID, @WorgenWildFemaleCreatureID);
