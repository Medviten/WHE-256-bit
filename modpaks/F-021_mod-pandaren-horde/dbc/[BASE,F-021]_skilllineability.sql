-- skilllineability: Horde Pandaren learn the racials of F-129
UPDATE `skilllineability` SET `required_races` = `required_races` | @HordePandarenMask,
    `required_races_2` = `required_races_2` | @HordePandarenMask_2 WHERE `id` IN (@CoANeutralPandarenSkillLineAbility1, @CoANeutralPandarenSkillLineAbility2, @CoANeutralPandarenSkillLineAbility3, @CoANeutralPandarenSkillLineAbility4);
