-- Reputation spillover between the capital factions of each side. Stock, each capital gives the four other capitals
-- of its side 25% of its reputation gains, up to Exalted (reputation_spillover_template). This adds the home faction
-- of every playable race to that circle, for any race id (no race masks involved): a race counts when its ChrRaces
-- record exists and is playable (no 0x01 flag, the same test as the core's RaceMgr), and its side is ChrRaces'
-- `alliance` (0 Alliance, 1 Horde). Its faction must exist in Faction.dbc, be listed (reputation_index >= 0) and have
-- a parent faction. Races whose modpak is off, and races without a <Race>Faction variable, drop out on their own.
--
-- Uses reputation_spillover_faction (256-bit core), which has no limit on spillover targets, unlike the 6 slots of
-- reputation_spillover_template, and its rows override the template slot for the same target faction.

-- Same definition as the core's pending update, for world dumps taken before the worldserver created the table
CREATE TABLE IF NOT EXISTS `reputation_spillover_faction` (
    `faction` INT UNSIGNED NOT NULL COMMENT 'faction entry (Faction.dbc) gaining the reputation',
    `spillover_faction` INT UNSIGNED NOT NULL COMMENT 'faction entry (Faction.dbc) that gets spillover',
    `rate` FLOAT NOT NULL DEFAULT '0' COMMENT 'the given rep points * rate',
    `max_rank` TINYINT UNSIGNED NOT NULL DEFAULT '0' COMMENT 'max rank, above this spillover_faction gets no spillover',
    PRIMARY KEY (`faction`, `spillover_faction`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Reputation spillover targets beyond reputation_spillover_template';

DELETE FROM `reputation_spillover_faction` WHERE `faction` IN (
    @HumanFaction, @OrcFaction, @DwarfFaction, @NightElfFaction, @UndeadFaction, @TaurenFaction, @GnomeFaction,
    @TrollFaction, @GoblinFaction, @BloodElfFaction, @DraeneiFaction, @NagaFaction, @BrokenFaction, @TaunkaFaction,
    @WorgenFaction, @GilneanFaction, @AlliancePandarenFaction, @HordePandarenFaction, @NightborneFaction,
    @HighmountainTaurenFaction, @VoidElfFaction, @LightforgedDraeneiFaction, @ZandalariTrollFaction,
    @KulTiranFaction, @DarkIronDwarfFaction, @VulperaFaction, @MagharOrcFaction, @HighElfFaction, @OgreFaction,
    @VrykulFaction, @MechagnomeFaction, @ThinHumanFaction, @TuskarrFaction,
    @AllianceEarthenFaction, @HordeEarthenFaction, @DarkfallenFaction, @MurlocFaction, @FurbolgFaction,
    @FelOrcFaction, @SkeletonFaction, @ForestTrollFaction, @NorthrendSkeletonFaction, @IceTrollFaction, @QirajiFaction,
    @EredarFaction, @ArakkoaFaction, @FelElfFaction, @QuillboarFaction, @CentaurFaction, @DemonFaction, @SatyrFaction,
    @GnollFaction, @BeholderFaction, @ShivanFaction, @HozenFaction, @SylvariFaction, @MantidFaction, @EtherealFaction,
    @KyrianFaction, @VenthyrFaction, @BansheeFaction, @FacelessOneFaction
);

INSERT INTO `reputation_spillover_faction` (`faction`, `spillover_faction`, `rate`, `max_rank`)
WITH `races` (`race`, `faction`) AS (
              SELECT @Human,              @HumanFaction
    UNION ALL SELECT @Orc,                @OrcFaction
    UNION ALL SELECT @Dwarf,              @DwarfFaction
    UNION ALL SELECT @NightElf,           @NightElfFaction
    UNION ALL SELECT @Undead,             @UndeadFaction
    UNION ALL SELECT @Tauren,             @TaurenFaction
    UNION ALL SELECT @Gnome,              @GnomeFaction
    UNION ALL SELECT @Troll,              @TrollFaction
    UNION ALL SELECT @Goblin,             @GoblinFaction
    UNION ALL SELECT @BloodElf,           @BloodElfFaction
    UNION ALL SELECT @Draenei,            @DraeneiFaction
    UNION ALL SELECT @Naga,               @NagaFaction
    UNION ALL SELECT @Broken,             @BrokenFaction
    UNION ALL SELECT @Taunka,             @TaunkaFaction
    UNION ALL SELECT @Worgen,             @WorgenFaction
    UNION ALL SELECT @Gilnean,            @GilneanFaction
    UNION ALL SELECT @AlliancePandaren,   @AlliancePandarenFaction
    UNION ALL SELECT @HordePandaren,      @HordePandarenFaction
    UNION ALL SELECT @Nightborne,         @NightborneFaction
    UNION ALL SELECT @HighmountainTauren, @HighmountainTaurenFaction
    UNION ALL SELECT @VoidElf,            @VoidElfFaction
    UNION ALL SELECT @LightforgedDraenei, @LightforgedDraeneiFaction
    UNION ALL SELECT @ZandalariTroll,     @ZandalariTrollFaction
    UNION ALL SELECT @KulTiran,           @KulTiranFaction
    UNION ALL SELECT @DarkIronDwarf,      @DarkIronDwarfFaction
    UNION ALL SELECT @Vulpera,            @VulperaFaction
    UNION ALL SELECT @MagharOrc,          @MagharOrcFaction
    UNION ALL SELECT @HighElf,            @HighElfFaction
    UNION ALL SELECT @Ogre,               @OgreFaction
    UNION ALL SELECT @Vrykul,             @VrykulFaction
    UNION ALL SELECT @Mechagnome,         @MechagnomeFaction
    UNION ALL SELECT @ThinHuman,          @ThinHumanFaction
    UNION ALL SELECT @Tuskarr,            @TuskarrFaction
    UNION ALL SELECT @AllianceEarthen,    @AllianceEarthenFaction
    UNION ALL SELECT @HordeEarthen,       @HordeEarthenFaction
    UNION ALL SELECT @Darkfallen,         @DarkfallenFaction
    UNION ALL SELECT @Murloc,             @MurlocFaction
    UNION ALL SELECT @Furbolg,            @FurbolgFaction
    UNION ALL SELECT @FelOrc,             @FelOrcFaction
    UNION ALL SELECT @Skeleton,           @SkeletonFaction
    UNION ALL SELECT @ForestTroll,        @ForestTrollFaction
    UNION ALL SELECT @NorthrendSkeleton,  @NorthrendSkeletonFaction
    UNION ALL SELECT @IceTroll,           @IceTrollFaction
    UNION ALL SELECT @Qiraji,             @QirajiFaction
    UNION ALL SELECT @Eredar,             @EredarFaction
    UNION ALL SELECT @Arakkoa,            @ArakkoaFaction
    UNION ALL SELECT @FelElf,             @FelElfFaction
    UNION ALL SELECT @Quillboar,          @QuillboarFaction
    UNION ALL SELECT @Centaur,            @CentaurFaction
    UNION ALL SELECT @Demon,              @DemonFaction
    UNION ALL SELECT @Satyr,              @SatyrFaction
    UNION ALL SELECT @Gnoll,              @GnollFaction
    UNION ALL SELECT @Beholder,           @BeholderFaction
    UNION ALL SELECT @Shivan,             @ShivanFaction
    UNION ALL SELECT @Hozen,              @HozenFaction
    UNION ALL SELECT @Sylvari,            @SylvariFaction
    UNION ALL SELECT @Mantid,             @MantidFaction
    UNION ALL SELECT @Ethereal,           @EtherealFaction
    UNION ALL SELECT @Kyrian,             @KyrianFaction
    UNION ALL SELECT @Venthyr,            @VenthyrFaction
    UNION ALL SELECT @Banshee,            @BansheeFaction
    UNION ALL SELECT @FacelessOne,        @FacelessOneFaction
),
`capitals` AS (
    SELECT DISTINCT
        r.`faction`,
        c.`alliance` AS `side`
    FROM `races` r
    JOIN `dbc_db`.`chrraces` c
      ON c.`id` = r.`race`
     AND (c.`flags` & 1) = 0
     AND c.`alliance` IN (0, 1)
    JOIN `dbc_db`.`faction` f
      ON f.`id` = r.`faction`
     AND f.`reputation_index` >= 0
     AND f.`parent_faction_id` <> 0
    WHERE r.`race` IS NOT NULL
      AND r.`faction` IS NOT NULL
)
SELECT a.`faction`, b.`faction`, @CapitalSpilloverRate, @CapitalSpilloverMaxRank
FROM `capitals` a
JOIN `capitals` b
  ON b.`side` = a.`side`
 AND b.`faction` <> a.`faction`;
