/* Allows any race to complete any class-specific quest (ARAC, sweeping approach) */
UPDATE `quest_template` INNER JOIN `quest_template_addon`
	ON `quest_template_addon`.id = `quest_template`.id
		SET `AllowableRaces` = `AllowableRaces` | 1 | 2 | 4 | 8 | 16 | 32 | 64 | 128 | 512 | 1024
			WHERE `quest_template_addon`.allowableclasses != 0 AND AllowableRaces != 0;
