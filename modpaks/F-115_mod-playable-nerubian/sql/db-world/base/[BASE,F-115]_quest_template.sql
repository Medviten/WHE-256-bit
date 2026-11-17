/* Ensures that race-restricted quests include Nerubians (as Undead) */
UPDATE `quest_template` SET `AllowableRaces` = `AllowableRaces` | @NerubianMask,
    `AllowableRaces_2` = `AllowableRaces_2` | @NerubianMask_2 WHERE `AllowableRaces` & @UndeadMask AND `AllowableRaces` != -1;

/* Allows any race to complete any class-specific quest (ARAC, sweeping approach) */
UPDATE `quest_template` INNER JOIN `quest_template_addon`
	ON `quest_template_addon`.id = `quest_template`.`id`
		SET `AllowableRaces` = `AllowableRaces` | @NerubianMask
			WHERE `quest_template_addon`.`allowableclasses` != 0 AND `AllowableRaces` != 0;
