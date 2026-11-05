-- [F-100] hero_class: the game tables have rows for class 10, with placeholder values (melee crit 0.01 per Agility at any
-- level, and no regeneration). A Hero uses Paladin's. Rows are 100 per class, or 32 per class for the rating scalars;
-- `auto_id` and `id` start at 1.

UPDATE `gtchancetomeleecrit` h INNER JOIN `gtchancetomeleecrit` p ON h.`auto_id` = p.`auto_id` + 800 SET h.`data` = p.`data` WHERE p.`auto_id` BETWEEN 101 AND 200;
UPDATE `gtchancetospellcrit` h INNER JOIN `gtchancetospellcrit` p ON h.`auto_id` = p.`auto_id` + 800 SET h.`data` = p.`data` WHERE p.`auto_id` BETWEEN 101 AND 200;
UPDATE `gtoctregenhp` h INNER JOIN `gtoctregenhp` p ON h.`auto_id` = p.`auto_id` + 800 SET h.`data` = p.`data` WHERE p.`auto_id` BETWEEN 101 AND 200;
UPDATE `gtoctregenmp` h INNER JOIN `gtoctregenmp` p ON h.`auto_id` = p.`auto_id` + 800 SET h.`data` = p.`data` WHERE p.`auto_id` BETWEEN 101 AND 200;
UPDATE `gtregenhpperspt` h INNER JOIN `gtregenhpperspt` p ON h.`auto_id` = p.`auto_id` + 800 SET h.`data` = p.`data` WHERE p.`auto_id` BETWEEN 101 AND 200;
UPDATE `gtregenmpperspt` h INNER JOIN `gtregenmpperspt` p ON h.`auto_id` = p.`auto_id` + 800 SET h.`data` = p.`data` WHERE p.`auto_id` BETWEEN 101 AND 200;

UPDATE `gtchancetomeleecritbase` h INNER JOIN `gtchancetomeleecritbase` p ON h.`auto_id` = 10 AND p.`auto_id` = 2 SET h.`data` = p.`data`;
UPDATE `gtchancetospellcritbase` h INNER JOIN `gtchancetospellcritbase` p ON h.`auto_id` = 10 AND p.`auto_id` = 2 SET h.`data` = p.`data`;

UPDATE `gtoctclasscombatratingscalar` h INNER JOIN `gtoctclasscombatratingscalar` p ON h.`id` = p.`id` + 256 SET h.`data` = p.`data` WHERE p.`id` BETWEEN 33 AND 64;
