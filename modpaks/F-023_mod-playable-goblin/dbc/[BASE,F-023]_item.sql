-- item: 26 inserts, 0 updates, 0 deletes

-- New entries
DELETE FROM `item` WHERE `id` IN (
    @GoblinBrawlersHarnessItem, @GoblinBrawlersBootsItem,    @GoblinBrawlersGreavesItem, @GoblinBrawlersGauntletsItem,
    @GoblinTrappersShirtItem,   @GoblinTrappersPantsItem,    @GoblinTrappersBootsItem,
    @GoblinThugsTunicItem,      @GoblinThugsPantsItem,       @GoblinThugsBootsItem,
    @GoblinNeophytesRobeItem,   @GoblinNeophytesPantsItem,   @GoblinNeophytesShoesItem,
    @PrimalShirtItem,           @PrimalPantsItem,            @PrimalBootsItem,
    @GoblinApprenticesRobeItem, @GoblinApprenticesPantsItem, @GoblinApprenticesBootsItem,
    @GoblinAcolytesRobeItem,    @GoblinAcolytesPantsItem,    @GoblinAcolytesShoesItem,
    @GoblinTrikeItem,           @GoblinTurboTrikeItem,
    @WornWoodChopperItem,
    90000
);
INSERT INTO `item` (`id`, `class`, `subclass`, `sound_override_subclass`, `material`, `display_id`, `inventory_type`, `sheath`) VALUES
(@GoblinBrawlersHarnessItem,   4, 3, -1,   7,  @GoblinBrawlersHarnessItemDisplay,    5, 0), -- Goblin Brawler's Harness
(@GoblinBrawlersBootsItem,     4, 3, -1,   7,  @GoblinBrawlersBootsItemDisplay,      8, 0), -- Goblin Brawler's Boots
(@GoblinBrawlersGreavesItem,   4, 3, -1,   7,  @GoblinBrawlersGreavesItemDisplay,    7, 0), -- Goblin Brawler's Greaves
(@GoblinBrawlersGauntletsItem, 4, 3, -1,   7,  @GoblinBrawlersGauntletsItemDisplay, 10, 0), -- Goblin Brawler's Gauntlets
(@GoblinTrappersShirtItem,     4, 2, -1,   7,  @GoblinTrappersShirtItemDisplay,      5, 0), -- Goblin Trapper's Shirt
(@GoblinTrappersPantsItem,     4, 2, -1,   7,  @GoblinTrappersPantsItemDisplay,      7, 0), -- Goblin Trapper's Pants
(@GoblinTrappersBootsItem,     4, 2, -1,   7,  @GoblinTrappersBootsItemDisplay,      8, 0), -- Goblin Trapper's Boots
(@WornWoodChopperItem,         2, 1, -1,   1,  @WornWoodChopperItemDisplay,         17, 1), -- Worn Wood Chopper
(@GoblinThugsTunicItem,        4, 2, -1,   7,  @GoblinThugsTunicItemDisplay,         5, 0), -- Goblin Thug's Tunic
(@GoblinThugsPantsItem,        4, 2, -1,   7,  @GoblinThugsPantsItemDisplay,         7, 0), -- Goblin Thug's Pants
(@GoblinThugsBootsItem,        4, 2, -1,   7,  @GoblinThugsBootsItemDisplay,         8, 0), -- Goblin Thug's Boots
(@GoblinNeophytesRobeItem,     4, 1, -1,   7,  @GoblinNeophytesRobeItemDisplay,     20, 0), -- Goblin Neophyte's Robe
(@GoblinNeophytesPantsItem,    4, 1, -1,   7,  @GoblinNeophytesPantsItemDisplay,     7, 0), -- Goblin Neophyte's Pants
(@GoblinNeophytesShoesItem,    4, 1, -1,   7,  @GoblinNeophytesShoesItemDisplay,     8, 0), -- Goblin Neophyte's Shoes
(@PrimalShirtItem,             4, 2, -1,   7,  @PrimalShirtItemDisplay,              5, 0), -- Primal Shirt
(@PrimalPantsItem,             4, 2, -1,   7,  @PrimalPantsItemDisplay,              7, 0), -- Primal Pants
(@PrimalBootsItem,             4, 2, -1,   7,  @PrimalBootsItemDisplay,              8, 0), -- Primal Boots
(@GoblinApprenticesRobeItem,   4, 1, -1,   7,  @GoblinApprenticesRobeItemDisplay,   20, 0), -- Goblin Apprentice's Robe
(@GoblinApprenticesPantsItem,  4, 1, -1,   7,  @GoblinApprenticesPantsItemDisplay,   7, 0), -- Goblin Apprentice's Pants
(@GoblinApprenticesBootsItem,  4, 1, -1,   7,  @GoblinApprenticesBootsItemDisplay,   8, 0), -- Goblin Apprentice's Boots
(@GoblinAcolytesRobeItem,      4, 1, -1,   7,  @GoblinAcolytesRobeItemDisplay,      20, 0), -- Goblin Acolyte's Robe
(@GoblinAcolytesPantsItem,     4, 1, -1,   7,  @GoblinAcolytesPantsItemDisplay,      7, 0), -- Goblin Acolyte's Pants
(@GoblinAcolytesShoesItem,     4, 1, -1,   7,  @GoblinAcolytesShoesItemDisplay,      8, 0), -- Goblin Acolyte's Shoes
(@GoblinTrikeItem,            15, 5, -1,   4,  @GoblinTrikeItemDisplay,              0, 0), -- Goblin Trike Key
(@GoblinTurboTrikeItem,       15, 5, -1,   4,  @GoblinTurboTrikeItemDisplay,         0, 0); -- Goblin Turbo-Trike Key
