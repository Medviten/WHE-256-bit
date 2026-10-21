UPDATE `quest_template` INNER JOIN `quest_template_addon` 
	ON `quest_template_addon`.`id` = `quest_template`.`id`
		SET `AllowableRaces` = @PlayableRaceMask,
		    `AllowableRaces_2` = @PlayableRaceMask_2
			WHERE `quest_template_addon`.`allowableclasses` != 0 AND `AllowableRaces` != 0;
