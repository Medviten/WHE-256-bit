/* Update achievement criteria involving interactions with all races to include Saberon */
REPLACE INTO `achievement_criteria_data` (
    `criteria_id`, -- ID from Achievement_Criteria.dbc
    `type`, -- Determines how value1 and value2 are used (0–23)
    `value1`, -- Depends on type
    `value2`, -- Depends on type
    `ScriptName`
) VALUES
(@SaberonCriteria2,  2,  0, @Saberon, ''), -- Achievement 2422 (Shake Your Bunny-Maker)
(@SaberonCriteria2,  9, 18,       0, ''), -- Achievement 2422 (Shake Your Bunny-Maker)
(@SaberonCriteria2, 10,  1,       0, ''), -- Achievement 2422 (Shake Your Bunny-Maker)
(@SaberonCriteria3,  2,  0, @Saberon, ''), -- Achievement  291 (Check Your Head)
(@SaberonCriteria4, 21,  0, @Saberon, ''); -- Achievement 1430* (Realm First! Level 80 Saberon)
