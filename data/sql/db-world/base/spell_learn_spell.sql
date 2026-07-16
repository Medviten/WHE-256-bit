/* Learn Running Wild when learning Riding */
REPLACE INTO `spell_ranks` (
    `entry`, -- The ID of the spell learned first
    `SpellID`, -- The spell learned afterwards
    `Active` -- Whether the spell is shown in the spell book.
) VALUES
(
    33388, -- Entry: Apprentice Riding
    87840, -- Spell ID: Running Wild (rank 1)
    1 -- Active: Yes
), (
    33391, -- Entry: Journeyman Riding
    87841, -- Spell ID: Running Wild (rank 2) 
    1 -- Active: Yes
);