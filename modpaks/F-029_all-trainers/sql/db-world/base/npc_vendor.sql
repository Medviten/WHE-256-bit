DELETE FROM `npc_vendor` WHERE (`entry` BETWEEN 142024 AND 142042);

-- Jewelcrafting Supplies

SET @JC_Sup := 17512;

INSERT INTO `npc_vendor` (entry, slot, item, maxcount, incrtime, ExtendedCost, VerifiedBuild)
SELECT 142024, slot, item, maxcount, incrtime, ExtendedCost, VerifiedBuild
FROM `npc_vendor`
WHERE entry = @JC_Sup;

INSERT INTO `npc_vendor` (entry, slot, item, maxcount, incrtime, ExtendedCost, VerifiedBuild)
SELECT 142026, slot, item, maxcount, incrtime, ExtendedCost, VerifiedBuild
FROM `npc_vendor`
WHERE entry = @JC_Sup;

INSERT INTO `npc_vendor` (entry, slot, item, maxcount, incrtime, ExtendedCost, VerifiedBuild)
SELECT 142034, slot, item, maxcount, incrtime, ExtendedCost, VerifiedBuild
FROM `npc_vendor`
WHERE entry = @JC_Sup;

INSERT INTO `npc_vendor` (entry, slot, item, maxcount, incrtime, ExtendedCost, VerifiedBuild)
SELECT 142038, slot, item, maxcount, incrtime, ExtendedCost, VerifiedBuild
FROM `npc_vendor`
WHERE entry = @JC_Sup;

INSERT INTO `npc_vendor` (entry, slot, item, maxcount, incrtime, ExtendedCost, VerifiedBuild)
SELECT 142040, slot, item, maxcount, incrtime, ExtendedCost, VerifiedBuild
FROM `npc_vendor`
WHERE entry = @JC_Sup;

INSERT INTO `npc_vendor` (entry, slot, item, maxcount, incrtime, ExtendedCost, VerifiedBuild)
SELECT 142042, slot, item, maxcount, incrtime, ExtendedCost, VerifiedBuild
FROM `npc_vendor`
WHERE entry = @JC_Sup;

-- Mining Supplies

SET @Mine_Sup := 16751;

INSERT INTO `npc_vendor` (entry, slot, item, maxcount, incrtime, ExtendedCost, VerifiedBuild)
SELECT 142028, slot, item, maxcount, incrtime, ExtendedCost, VerifiedBuild
FROM `npc_vendor`
WHERE entry = @Mine_Sup;

-- Blacksmithing Supplies

SET @BS_Sup := 17655;

INSERT INTO `npc_vendor` (entry, slot, item, maxcount, incrtime, ExtendedCost, VerifiedBuild)
SELECT 142030, slot, item, maxcount, incrtime, ExtendedCost, VerifiedBuild
FROM `npc_vendor`
WHERE entry = @BS_Sup;

-- Engineering Supplies

SET @Eng_Sup := 16782;

INSERT INTO `npc_vendor` (entry, slot, item, maxcount, incrtime, ExtendedCost, VerifiedBuild)
SELECT 142032, slot, item, maxcount, incrtime, ExtendedCost, VerifiedBuild
FROM `npc_vendor`
WHERE entry = @Eng_Sup;

INSERT INTO `npc_vendor` (entry, slot, item, maxcount, incrtime, ExtendedCost, VerifiedBuild)
SELECT 142036, slot, item, maxcount, incrtime, ExtendedCost, VerifiedBuild
FROM `npc_vendor`
WHERE entry = @Eng_Sup;