/* Update achievement criteria involving interactions with all races to include Drakonid */
REPLACE INTO `achievement_criteria_data` (
    `criteria_id`, -- ID from Achievement_Criteria.dbc
    `type`, -- Determines how value1 and value2 are used (0–23)
    `value1`, -- Depends on type
    `value2`, -- Depends on type
    `ScriptName`
) VALUES
(@DrakonidCriteria2,  2,  0, @Drakonid, ''), -- Achievement 2422 (Shake Your Bunny-Maker)
(@DrakonidCriteria2,  9, 18,       0, ''), -- Achievement 2422 (Shake Your Bunny-Maker)
(@DrakonidCriteria2, 10,  1,       0, ''), -- Achievement 2422 (Shake Your Bunny-Maker)
(@DrakonidCriteria3,  2,  0, @Drakonid, ''), -- Achievement  291 (Check Your Head)
(@DrakonidCriteria4, 21,  0, @Drakonid, ''); -- Achievement 1430* (Realm First! Level 80 Drakonid)
