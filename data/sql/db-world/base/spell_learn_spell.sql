/* Learn Running Wild when learning Riding
REPLACE INTO `spell_ranks` (
    `entry`, -- The ID of the spell learned first
    `SpellID`, -- The spell learned afterwards
    `Active` -- Whether the spell is shown in the spell book.
) VALUES
(
    87840, -- Entry: Running Wild (male, 60%)
    33388, -- Spell ID: Apprentice Riding
    1 -- Active: Yes
), (
    87841, -- Entry: Running Wild (female, 60%)
    33388, -- Spell ID: Apprentice Riding
    1 -- Active: Yes
);
*/