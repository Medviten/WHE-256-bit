-- Altered form transition effects (SpellVisualEffectName). The patched client finds them by name, so the ids only need
-- to be unused; they sit next to F-013's 901xx effect names
SET @AlteredFormPoofEffect              = 90110; -- Cataclysm 5855
SET @AlteredFormAnimationPoofEffect     = 90111; -- Cataclysm 5870

-- Altered form transition sounds (SoundEntries). Also found by name, so the ids only need to be unused; they sit past
-- F-005's 2001xx sounds
SET @AlteredFormSound                   = 200210; -- Cataclysm 16448
SET @AlteredFormAnimationSound          = 200211; -- Cataclysm 16447

-- Running Wild's own spell visual and precast kit (copies of the mount visual 5499 and its kit 159 that play
-- MountSelfStart, then MountSelfIdle, through the cast)
SET @RunningWildVisual                  = 90120;
SET @RunningWildPrecastKit              = 90120;

-- Running Wild's MountSelfSpecial sound (SoundEntries): the Worgen models' $CSD event on that anim plays this id, so it
-- must stay Cataclysm's (free in 3.3.5, whose ids end at 18019)
SET @WorgenMountSpecialSound            = 23767;
