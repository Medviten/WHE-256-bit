-- Modern (BfA) Mag'har models: new model IDs, so stock orcs keep models 51/52
SET @MagharOrcModernMaleModel           = @NextModelID := @NextModelID +1;
SET @MagharOrcModernFemaleModel         = @NextModelID := @NextModelID +1;
SET @MagharOrcModernMaleModelPath       = 'Character\\magharorc\\male\\orcmaleupright.mdx'; -- or orcmale_hd.mdx (hunched stance)
SET @MagharOrcModernFemaleModelPath     = 'Character\\magharorc\\female\\orcfemale_hd.mdx';
