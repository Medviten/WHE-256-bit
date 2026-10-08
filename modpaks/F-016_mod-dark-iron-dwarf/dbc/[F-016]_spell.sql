-- spell: 0 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `spell` WHERE `id` IN (
	@SpellMoleMachine,    @SpellFireblood,     @SpellForgedInFlames,
	@SpellMassProduction, @SpellDungeonDelver, @BuffDungeonDelver
);
INSERT INTO `spell` (`id`, `category`, `dispel`, `mechanic`, `attributes`, `attributes_ex_1`, `attributes_ex_2`, `attributes_ex_3`, `attributes_ex_4`, `attributes_ex_5`, `attributes_ex_6`, `attributes_ex_7`, `stances`, `unk_1`, `excluded_stances`, `unk_2`, `targets`, `target_creature_type`, `spell_focus_object`, `facing_caster_flags`, `caster_aura_state`, `target_aura_state`, `excluded_caster_aura_state`, `excluded_target_aura_state`, `caster_aura_spell`, `target_aura_spell`, `excluded_caster_aura_spell`, `excluded_target_aura_spell`, `cast_time_index`, `recovery_time`, `category_recovery_time`, `interrupt_flags`, `aura_interrupt_flags`, `channel_interrupt_flags`, `proc_flags`, `proc_chance`, `proc_charges`, `max_level`, `base_level`, `spell_level`, `duration_index`, `power_type`, `power_cost`, `power_cost_per_level`, `power_per_second`, `power_per_second_per_level`, `range_index`, `speed`, `modal_next_spell`, `stack_amount`, `totem_1`, `totem_2`, `reagent_1`, `reagent_2`, `reagent_3`, `reagent_4`, `reagent_5`, `reagent_6`, `reagent_7`, `reagent_8`, `reagent_count_1`, `reagent_count_2`, `reagent_count_3`, `reagent_count_4`, `reagent_count_5`, `reagent_count_6`, `reagent_count_7`, `reagent_count_8`, `equipped_item_class`, `equipped_item_subclass_mask`, `equipped_item_inventorytype_mask`, `effect_1`, `effect_2`, `effect_3`, `effect_die_sides_1`, `effect_die_sides_2`, `effect_die_sides_3`, `effect_real_points_per_level_1`, `effect_real_points_per_level_2`, `effect_real_points_per_level_3`, `effect_base_points_1`, `effect_base_points_2`, `effect_base_points_3`, `effect_mechanic_1`, `effect_mechanic_2`, `effect_mechanic_3`, `effect_implicit_target_a_1`, `effect_implicit_target_a_2`, `effect_implicit_target_a_3`, `effect_implicit_target_b_1`, `effect_implicit_target_b_2`, `effect_implicit_target_b_3`, `effect_radius_index_1`, `effect_radius_index_2`, `effect_radius_index_3`, `effect_apply_aura_name_1`, `effect_apply_aura_name_2`, `effect_apply_aura_name_3`, `effect_amplitude_1`, `effect_amplitude_2`, `effect_amplitude_3`, `effect_multiple_value_1`, `effect_multiple_value_2`, `effect_multiple_value_3`, `effect_chain_target_1`, `effect_chain_target_2`, `effect_chain_target_3`, `effect_item_type_1`, `effect_item_type_2`, `effect_item_type_3`, `effect_misc_value_a_1`, `effect_misc_value_a_2`, `effect_misc_value_a_3`, `effect_misc_value_b_1`, `effect_misc_value_b_2`, `effect_misc_value_b_3`, `effect_trigger_spell_1`, `effect_trigger_spell_2`, `effect_trigger_spell_3`, `effect_points_per_combo_point_1`, `effect_points_per_combo_point_2`, `effect_points_per_combo_point_3`, `effect_spell_class_mask_a_1`, `effect_spell_class_mask_a_2`, `effect_spell_class_mask_a_3`, `effect_spell_class_mask_b_1`, `effect_spell_class_mask_b_2`, `effect_spell_class_mask_b_3`, `effect_spell_class_mask_c_1`, `effect_spell_class_mask_c_2`, `effect_spell_class_mask_c_3`, `spell_visual_1`, `spell_visual_2`, `spell_icon_id`, `active_icon_id`, `spell_priority`, `spell_name_enus`, `spell_name_kokr`, `spell_name_frfr`, `spell_name_dede`, `spell_name_zhcn`, `spell_name_zhtw`, `spell_name_eses`, `spell_name_esmx`, `spell_name_ruru`, `spell_name_jajp`, `spell_name_ptpt`, `spell_name_itit`, `spell_name_unused_1`, `spell_name_unused_2`, `spell_name_unused_3`, `spell_name_unused_4`, `spell_name_flags`, `spell_subtext_enus`, `spell_subtext_kokr`, `spell_subtext_frfr`, `spell_subtext_dede`, `spell_subtext_zhcn`, `spell_subtext_zhtw`, `spell_subtext_eses`, `spell_subtext_esmx`, `spell_subtext_ruru`, `spell_subtext_jajp`, `spell_subtext_ptpt`, `spell_subtext_itit`, `spell_subtext_unused_1`, `spell_subtext_unused_2`, `spell_subtext_unused_3`, `spell_subtext_unused_4`, `spell_subtext_flags`, `spell_desc_enus`, `spell_desc_kokr`, `spell_desc_frfr`, `spell_desc_dede`, `spell_desc_zhcn`, `spell_desc_zhtw`, `spell_desc_eses`, `spell_desc_esmx`, `spell_desc_ruru`, `spell_desc_jajp`, `spell_desc_ptpt`, `spell_desc_itit`, `spell_desc_unused_1`, `spell_desc_unused_2`, `spell_desc_unused_3`, `spell_desc_unused_4`, `spell_desc_flags`, `spell_tooltip_enus`, `spell_tooltip_kokr`, `spell_tooltip_frfr`, `spell_tooltip_dede`, `spell_tooltip_zhcn`, `spell_tooltip_zhtw`, `spell_tooltip_eses`, `spell_tooltip_esmx`, `spell_tooltip_ruru`, `spell_tooltip_jajp`, `spell_tooltip_ptpt`, `spell_tooltip_itit`, `spell_tooltip_unused_1`, `spell_tooltip_unused_2`, `spell_tooltip_unused_3`, `spell_tooltip_unused_4`, `spell_tooltip_flags`, `power_cost_percentage`, `start_recovery_category`, `start_recovery_time`, `maximum_target_level`, `spell_class_set`, `spell_class_mask_1`, `spell_class_mask_2`, `spell_class_mask_3`, `max_affected_targets`, `damage_class`, `prevention_type`, `stance_bar_order`, `effect_damage_multiplier_1`, `effect_damage_multiplier_2`, `effect_damage_multiplier_3`, `min_faction_id`, `min_reputation`, `req_aura_vision`, `totem_category_1`, `totem_category_2`, `area_group_id`, `school_mask`, `rune_cost_id`, `spell_missile_id`, `power_display_id`, `effect_bonus_multiplier_1`, `effect_bonus_multiplier_2`, `effect_bonus_multiplier_3`, `spell_desc_variable_id`, `spell_difficulty_id`) VALUES
(@SpellDungeonDelver, 0, 0, 0,
 64|16384, -- Attributes: 64 = SPELL_ATTR0_PASSIVE, 16384 = SPELL_ATTR0_ONLY_INDOORS
 0, 0, 0, 0, 0, 0, 0,      -- AttributesEx 1-7
 0, 0, 0, 0,               -- Stances, unk_1, ExcludedStances, unk_2
 0, 0, 0, 0,               -- Targets, TargetCreatureType, SpellFocusObject, FacingCasterFlags
 0, 0, 0, 0,               -- CasterAuraState, TargetAuraState, ExcludedCasterAuraState, ExcludedTargetAuraState
 0, 0, 0, 0,               -- CasterAuraSpell, TargetAuraSpell, ExcludedCasterAuraSpell, ExcludedTargetAuraSpell
 1, 0, 0,                  -- CastTimeIndex (Instant), RecoveryTime, CategoryRecoveryTime
 0, 0, 0,                  -- InterruptFlags, AuraInterruptFlags, ChannelInterruptFlags — nothing should interrupt a passive
 0, 0, 0,                  -- ProcFlags, ProcChance, ProcCharges — not proc-based
 0, 0, 0,                  -- MaxLevel, BaseLevel, SpellLevel
 21,                       -- DurationIndex — Permanent (matches the convention your own Running Wild spell uses)
 0, 0, 0, 0, 0,            -- PowerType, ManaCost, ManaCostPerLevel, ManaPerSecond, ManaPerSecondPerLevel
 1, 0, 0, 0,               -- RangeIndex (Self), Speed, ModalNextSpell, StackAmount
 0, 0,                     -- Totem 1/2
 0, 0, 0, 0, 0, 0, 0, 0,   -- Reagents 1-8
 0, 0, 0, 0, 0, 0, 0, 0,   -- ReagentCounts 1-8
 -1, 0, 0,                 -- EquippedItemClass, EquippedItemSubclassMask, EquippedItemInventoryTypeMask
 6, 0, 0,                  -- Effect_1 = SPELL_EFFECT_APPLY_AURA, Effect_2/3 unused
 1, 0, 0,                  -- EffectDieSides 1-3
 0, 0, 0,                  -- EffectRealPointsPerLevel 1-3
 93, 0, 0,                  -- EffectBasePoints_1 = 3 (real value = base+1 = 4%), 2/3 unused
 0, 0, 0,                  -- EffectMechanic 1-3
 1, 0, 0,                  -- ImplicitTargetA_1 = TARGET_UNIT_CASTER (self)
 0, 0, 0,                  -- ImplicitTargetB 1-3
 0, 0, 0,                  -- EffectRadiusIndex 1-3 (not needed for a self-target)
 31, 0, 0,                 -- EffectApplyAuraName_1 = SPELL_AURA_MOD_INCREASE_SPEED
 0, 0, 0,                  -- EffectAmplitude 1-3 — not periodic, no tick needed
 0, 0, 0,                  -- EffectMultipleValue 1-3
 0, 0, 0,                  -- EffectChainTarget 1-3
 0, 0, 0,                  -- EffectItemType 1-3
 0, 0, 0,                  -- EffectMiscValueA 1-3
 0, 0, 0,                  -- EffectMiscValueB 1-3
 0, 0, 0,                  -- EffectTriggerSpell 1-3
 0, 0, 0,                  -- EffectPointsPerComboPoint 1-3
 0, 0, 0, 0, 0, 0, 0, 0, 0,-- EffectSpellClassMask A/B/C, 1-3
 0, 0,                     -- SpellVisual 1/2 — no visible cast effect, it's silent
 @IconDungeonDelver, 0, 0,                  -- SpellIconID, ActiveIconID (pick a movement/boot-themed icon you already have — see note below), SpellPriority
 'Dungeon Delver', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 16712190,
 'Racial', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 16712172,
 'While indoors, movement speed increased by $s1%.', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 16712190,
 'Movement speed increased.', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 16712190,
 0, 0, 0, 0,               -- PowerCostPct, StartRecoveryCategory, StartRecoveryTime, MaxTargetLevel
 0, 0, 0, 0,               -- SpellClassSet, SpellClassMask 1-3
 0, 2, 0, 0,               -- MaxAffectedTargets, DamageClass (2 = DAMAGE_CLASS_NONE... see note), PreventionType, StanceBarOrder
 '1.0000000000000000', '1.0000000000000000', '1.0000000000000000', -- EffectDamageMultiplier 1-3
 0, 0, 0,                  -- MinFactionId, MinReputation, RequiredAuraVision
 0, 0, 0,                  -- TotemCategory 1/2, AreaGroupId
 1,                        -- SchoolMask = Physical
 0, 0, 0,                  -- RuneCostID, SpellMissileID, PowerDisplayID
 '0E-16', '0E-16', '0E-16',-- EffectBonusMultiplier 1-3
 0, 0);                    -- SpellDescriptionVariableID, SpellDifficultyID
UPDATE `spell` SET
    `effect_1` = 6,                              -- SPELL_EFFECT_APPLY_AURA
    `effect_apply_aura_name_1` = 23,              -- SPELL_AURA_PERIODIC_TRIGGER_SPELL
    `effect_trigger_spell_1` = @BuffDungeonDelver,
    `effect_amplitude_1` = 2000,                  -- re-check every 2 seconds
    `effect_base_points_1` = 0,
    `effect_implicit_target_a_1` = 1,             -- TARGET_UNIT_CASTER
    `attributes` = 64                             -- SPELL_ATTR0_PASSIVE only — no location gate here
WHERE `id` = @SpellDungeonDelver;
INSERT INTO `spell` (`id`, `category`, `dispel`, `mechanic`, `attributes`, `attributes_ex_1`, `attributes_ex_2`, `attributes_ex_3`, `attributes_ex_4`, `attributes_ex_5`, `attributes_ex_6`, `attributes_ex_7`, `stances`, `unk_1`, `excluded_stances`, `unk_2`, `targets`, `target_creature_type`, `spell_focus_object`, `facing_caster_flags`, `caster_aura_state`, `target_aura_state`, `excluded_caster_aura_state`, `excluded_target_aura_state`, `caster_aura_spell`, `target_aura_spell`, `excluded_caster_aura_spell`, `excluded_target_aura_spell`, `cast_time_index`, `recovery_time`, `category_recovery_time`, `interrupt_flags`, `aura_interrupt_flags`, `channel_interrupt_flags`, `proc_flags`, `proc_chance`, `proc_charges`, `max_level`, `base_level`, `spell_level`, `duration_index`, `power_type`, `power_cost`, `power_cost_per_level`, `power_per_second`, `power_per_second_per_level`, `range_index`, `speed`, `modal_next_spell`, `stack_amount`, `totem_1`, `totem_2`, `reagent_1`, `reagent_2`, `reagent_3`, `reagent_4`, `reagent_5`, `reagent_6`, `reagent_7`, `reagent_8`, `reagent_count_1`, `reagent_count_2`, `reagent_count_3`, `reagent_count_4`, `reagent_count_5`, `reagent_count_6`, `reagent_count_7`, `reagent_count_8`, `equipped_item_class`, `equipped_item_subclass_mask`, `equipped_item_inventorytype_mask`, `effect_1`, `effect_2`, `effect_3`, `effect_die_sides_1`, `effect_die_sides_2`, `effect_die_sides_3`, `effect_real_points_per_level_1`, `effect_real_points_per_level_2`, `effect_real_points_per_level_3`, `effect_base_points_1`, `effect_base_points_2`, `effect_base_points_3`, `effect_mechanic_1`, `effect_mechanic_2`, `effect_mechanic_3`, `effect_implicit_target_a_1`, `effect_implicit_target_a_2`, `effect_implicit_target_a_3`, `effect_implicit_target_b_1`, `effect_implicit_target_b_2`, `effect_implicit_target_b_3`, `effect_radius_index_1`, `effect_radius_index_2`, `effect_radius_index_3`, `effect_apply_aura_name_1`, `effect_apply_aura_name_2`, `effect_apply_aura_name_3`, `effect_amplitude_1`, `effect_amplitude_2`, `effect_amplitude_3`, `effect_multiple_value_1`, `effect_multiple_value_2`, `effect_multiple_value_3`, `effect_chain_target_1`, `effect_chain_target_2`, `effect_chain_target_3`, `effect_item_type_1`, `effect_item_type_2`, `effect_item_type_3`, `effect_misc_value_a_1`, `effect_misc_value_a_2`, `effect_misc_value_a_3`, `effect_misc_value_b_1`, `effect_misc_value_b_2`, `effect_misc_value_b_3`, `effect_trigger_spell_1`, `effect_trigger_spell_2`, `effect_trigger_spell_3`, `effect_points_per_combo_point_1`, `effect_points_per_combo_point_2`, `effect_points_per_combo_point_3`, `effect_spell_class_mask_a_1`, `effect_spell_class_mask_a_2`, `effect_spell_class_mask_a_3`, `effect_spell_class_mask_b_1`, `effect_spell_class_mask_b_2`, `effect_spell_class_mask_b_3`, `effect_spell_class_mask_c_1`, `effect_spell_class_mask_c_2`, `effect_spell_class_mask_c_3`, `spell_visual_1`, `spell_visual_2`, `spell_icon_id`, `active_icon_id`, `spell_priority`, `spell_name_enus`, `spell_name_kokr`, `spell_name_frfr`, `spell_name_dede`, `spell_name_zhcn`, `spell_name_zhtw`, `spell_name_eses`, `spell_name_esmx`, `spell_name_ruru`, `spell_name_jajp`, `spell_name_ptpt`, `spell_name_itit`, `spell_name_unused_1`, `spell_name_unused_2`, `spell_name_unused_3`, `spell_name_unused_4`, `spell_name_flags`, `spell_subtext_enus`, `spell_subtext_kokr`, `spell_subtext_frfr`, `spell_subtext_dede`, `spell_subtext_zhcn`, `spell_subtext_zhtw`, `spell_subtext_eses`, `spell_subtext_esmx`, `spell_subtext_ruru`, `spell_subtext_jajp`, `spell_subtext_ptpt`, `spell_subtext_itit`, `spell_subtext_unused_1`, `spell_subtext_unused_2`, `spell_subtext_unused_3`, `spell_subtext_unused_4`, `spell_subtext_flags`, `spell_desc_enus`, `spell_desc_kokr`, `spell_desc_frfr`, `spell_desc_dede`, `spell_desc_zhcn`, `spell_desc_zhtw`, `spell_desc_eses`, `spell_desc_esmx`, `spell_desc_ruru`, `spell_desc_jajp`, `spell_desc_ptpt`, `spell_desc_itit`, `spell_desc_unused_1`, `spell_desc_unused_2`, `spell_desc_unused_3`, `spell_desc_unused_4`, `spell_desc_flags`, `spell_tooltip_enus`, `spell_tooltip_kokr`, `spell_tooltip_frfr`, `spell_tooltip_dede`, `spell_tooltip_zhcn`, `spell_tooltip_zhtw`, `spell_tooltip_eses`, `spell_tooltip_esmx`, `spell_tooltip_ruru`, `spell_tooltip_jajp`, `spell_tooltip_ptpt`, `spell_tooltip_itit`, `spell_tooltip_unused_1`, `spell_tooltip_unused_2`, `spell_tooltip_unused_3`, `spell_tooltip_unused_4`, `spell_tooltip_flags`, `power_cost_percentage`, `start_recovery_category`, `start_recovery_time`, `maximum_target_level`, `spell_class_set`, `spell_class_mask_1`, `spell_class_mask_2`, `spell_class_mask_3`, `max_affected_targets`, `damage_class`, `prevention_type`, `stance_bar_order`, `effect_damage_multiplier_1`, `effect_damage_multiplier_2`, `effect_damage_multiplier_3`, `min_faction_id`, `min_reputation`, `req_aura_vision`, `totem_category_1`, `totem_category_2`, `area_group_id`, `school_mask`, `rune_cost_id`, `spell_missile_id`, `power_display_id`, `effect_bonus_multiplier_1`, `effect_bonus_multiplier_2`, `effect_bonus_multiplier_3`, `spell_desc_variable_id`, `spell_difficulty_id`) VALUES
(@BuffDungeonDelver, 0, 0, 0,
 16384,                    -- Attributes: SPELL_ATTR0_ONLY_INDOORS — NOT passive this time; relies on a fresh CheckCast every trigger tick, not the stateful toggle
 0, 0, 0, 0, 0, 0, 0,
 0, 0, 0, 0,
 0, 0, 0, 0,
 0, 0, 0, 0,
 0, 0, 0, 0,
 1, 0, 0,                  -- CastTimeIndex (Instant), RecoveryTime, CategoryRecoveryTime
 0, 0, 0,
 0, 0, 0,
 0, 0, 0,
 1,                        -- DurationIndex — 10 seconds. Refreshed every 2s while indoors, so it never visibly expires; fades within ~10s of leaving
 0, 0, 0, 0, 0,
 1, 0, 0, 0,               -- RangeIndex (Self)
 0, 0,
 0, 0, 0, 0, 0, 0, 0, 0,
 0, 0, 0, 0, 0, 0, 0, 0,
 -1, 0, 0,
 6, 0, 0,                  -- Effect_1 = SPELL_EFFECT_APPLY_AURA
 1, 0, 0,
 0, 0, 0,
 93, 0, 0,                  -- EffectBasePoints_1 = 3 (real value = base+1 = 4%)
 0, 0, 0,
 1, 0, 0,                  -- ImplicitTargetA_1 = TARGET_UNIT_CASTER
 0, 0, 0,
 0, 0, 0,
 31, 0, 0,                 -- EffectApplyAuraName_1 = SPELL_AURA_MOD_INCREASE_SPEED
 0, 0, 0,                  -- not periodic itself — the holder's trigger drives the refresh
 0, 0, 0,
 0, 0, 0,
 0, 0, 0,
 0, 0, 0,
 0, 0, 0,
 0, 0, 0,
 0, 0, 0,
 0, 0, 0, 0, 0, 0, 0, 0, 0,
 0, 0,
 @IconDungeonDelver, 0, 0,
 'Dungeon Delver', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 16712190,
 'Racial', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 16712172,
 'While indoors, movement speed increased by $s1%.', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 16712190,
 'Movement speed increased.', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 16712190,
 0, 0, 0, 0,
 0, 0, 0, 0,
 0, 2, 0, 0,
 '1.0000000000000000', '1.0000000000000000', '1.0000000000000000',
 0, 0, 0,
 0, 0, 0,
 1,
 0, 0, 0,
 '0E-16', '0E-16', '0E-16',
 0, 0);