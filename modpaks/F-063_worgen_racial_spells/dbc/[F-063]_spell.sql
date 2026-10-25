-- Two Forms (male) applies the altered form aura instead of a transform; the patched client draws the player's own
-- character as the altered race while it is up, so the spell no longer depends on gender (testing; female still transforms)
UPDATE `spell` SET `effect_apply_aura_name_1` = @SPELL_AURA_ALTERED_FORM, `effect_misc_value_a_1` = 0 WHERE `id` = @TwoFormsMale;

-- Running Wild (87840, previously only for male worgen) becomes a real mount on which the Worgen is its own mount, for both genders: a mounted aura
-- with no creature (spell_worgen_running_wild mounts the player's native display; requires patched client) and a
-- mounted speed aura whose amount the script sets from riding skill (60% or 100%). Flags as on ground mounts (e.g. 458).
UPDATE `spell` SET
    `mechanic` = 21, -- MECHANIC_MOUNT
    `attributes` = @SPELL_ATTR0_IS_ABILITY | @SPELL_ATTR0_DO_NOT_LOG | @SPELL_ATTR0_OUTDOORS_ONLY | @SPELL_ATTR0_NOT_SHAPESHIFTED | @SPELL_ATTR0_DO_NOT_SHEATH | @SPELL_ATTR0_CANCELS_AUTO_ATTACK_COMBAT | @SPELL_ATTR0_NOT_IN_COMBAT_ONLY_PEACEFUL,
    `aura_interrupt_flags` = 0,
    `effect_apply_aura_name_1` = @SPELL_AURA_MOUNTED,
    `effect_misc_value_a_1` = 0,
    `effect_apply_aura_name_2` = 32 -- SPELL_AURA_MOD_INCREASE_MOUNTED_SPEED
WHERE `id` = @RunningWildMale60;

-- Remove superfluous spells
DELETE FROM `spell` WHERE `id` IN (
	@RunningWildMale100,
	@RunningWildFemale60,
	@RunningWildFemale100
); 