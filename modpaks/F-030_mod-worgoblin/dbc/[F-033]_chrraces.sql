-- chrraces: 0 inserts, 1 updates, 0 deletes

SET @Goblin = 9;
SET @Worgen = 12;

-- New entries
UPDATE `chrraces` SET `faction_id` = 2238 WHERE `id` = @Goblin;
UPDATE `chrraces` SET `faction_id` = 2239 WHERE `id` = @Worgen;
