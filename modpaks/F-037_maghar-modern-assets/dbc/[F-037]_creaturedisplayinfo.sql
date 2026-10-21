-- creaturedisplayinfo: 0 inserts, 2 updates, 0 deletes

-- Changed values
UPDATE `creaturedisplayinfo` SET `model_id` = @MagharOrcModernMaleModel   WHERE `id` = @MagharOrcMaleDisplay;
UPDATE `creaturedisplayinfo` SET `model_id` = @MagharOrcModernFemaleModel WHERE `id` = @MagharOrcFemaleDisplay;
