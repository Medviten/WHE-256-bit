/* Update achievement criteria involving interactions with all races to include Gilneans */
REPLACE INTO `achievement_criteria_data` (
    `criteria_id`, -- ID from Achievement_Criteria.dbc
    `type`, -- Determines how value1 and value2 are used (0–23)
    `value1`, -- Depends on type
    `value2`, -- Depends on type
    `ScriptName`
) VALUES
(@GilneanCriteria2,  2,  0, @Gilnean, ''), -- Achievement 2422 (Shake Your Bunny-Maker)
(@GilneanCriteria2,  9, 18,       0, ''), -- Achievement 2422 (Shake Your Bunny-Maker)
(@GilneanCriteria2, 10,  1,       0, ''), -- Achievement 2422 (Shake Your Bunny-Maker)
(@GilneanCriteria3,  2,  0, @Gilnean, ''), -- Achievement  291 (Check Your Head)
(@GilneanCriteria4,  2,  0, @Gilnean, ''); -- Achievement 1441* (Realm First! Level 80 Gilnean)
