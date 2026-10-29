-- Altered form transition effects (SpellVisualEffectName). The patched client finds them by name, so the ids only need
-- to be unused; they sit next to F-013's 901xx effect names
SET @AlteredFormPoofEffect              = 90110; -- Cataclysm 5855
SET @AlteredFormAnimationPoofEffect     = 90111; -- Cataclysm 5870

-- Altered form transition sounds (SoundEntries). Also found by name, so the ids only need to be unused; they sit past
-- F-005's 2001xx sounds
SET @AlteredFormSound                   = 200210; -- Cataclysm 16448
SET @AlteredFormAnimationSound          = 200211; -- Cataclysm 16447
