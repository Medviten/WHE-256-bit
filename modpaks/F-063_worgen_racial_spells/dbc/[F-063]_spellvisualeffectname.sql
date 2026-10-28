-- Cataclysm's altered form effects, played by the patched client when a Worgen changes form: the poof of the instant
-- swap and the one that comes with the human-to-Worgen anim. The client finds them by these exact names (its
-- "HARDCODED" special unit effects), so the names must not change. Values are Cataclysm's (4.3.4 ids 5855 and 5870);
-- the models are converted from Cataclysm in patch-A (Spells\Worgen_Combat_Transform_FX.m2, Worgen_Transform_FX.m2)
DELETE FROM `spellvisualeffectname` WHERE `id` IN (@AlteredFormPoofEffect, @AlteredFormAnimationPoofEffect);
INSERT INTO `spellvisualeffectname` (`id`, `name`, `file_name`, `area_effect_size`, `scale`, `min_allowed_scale`, `max_allowed_scale`) VALUES
(@AlteredFormPoofEffect,          'HARDCODED Altered Form Poof',           'spells\\worgen_combat_transform_fx.mdx', 2.0, 1.0, 0.01, 100.0),
(@AlteredFormAnimationPoofEffect, 'HARDCODED Altered Form Animation Poof', 'spells\\worgen_transform_fx.mdx',        0.0, 1.0, 0.1,  10.0);
