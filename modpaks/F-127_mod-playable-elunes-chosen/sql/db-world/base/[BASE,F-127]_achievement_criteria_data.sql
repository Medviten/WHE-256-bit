/* Update achievement criteria involving interactions with all races to include Elune's Chosen */
REPLACE INTO `achievement_criteria_data` (
    `criteria_id`, -- ID from Achievement_Criteria.dbc
    `type`, -- Determines how value1 and value2 are used (0–23)
    `value1`, -- Depends on type
    `value2`, -- Depends on type
    `ScriptName`
) VALUES
(@EluneChosenCriteria2,  2,  0, @EluneChosen, ''), -- Achievement 2422 (Shake Your Bunny-Maker)
(@EluneChosenCriteria2,  9, 18,       0, ''), -- Achievement 2422 (Shake Your Bunny-Maker)
(@EluneChosenCriteria2, 10,  1,       0, ''), -- Achievement 2422 (Shake Your Bunny-Maker)
(@EluneChosenCriteria3,  2,  0, @EluneChosen, ''), -- Achievement  291 (Check Your Head)
(@EluneChosenCriteria4, 21,  0, @EluneChosen, ''); -- Achievement 1430* (Realm First! Level 80 Elune's Chosen)
