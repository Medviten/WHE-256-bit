-- F-100_hero_class
SET @Hero                                                      =     10; -- the class id stock leaves unused
SET @HeroMask                                                  =    512; -- 1 << (@Hero - 1)
SET @HeroTrainerBase                                           = 190000; -- Trainer::HERO_SPELLS_TRAINER_BASE in the core patch
