-- The table F-013's core patch reads (PhaseMgr); F-013 creates it too, so either modpak can come first
CREATE TABLE IF NOT EXISTS `phase_definitions` (
  `zoneId` INT UNSIGNED NOT NULL DEFAULT 0,
  `entry` INT UNSIGNED NOT NULL DEFAULT 0,
  `phaseMask` INT UNSIGNED NOT NULL DEFAULT 0,
  `phaseId` INT UNSIGNED NOT NULL DEFAULT 0,
  `originmap` INT UNSIGNED NOT NULL DEFAULT 0,
  `terrainswapmap` INT UNSIGNED NOT NULL DEFAULT 0,
  `flags` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `comment` TEXT DEFAULT NULL,
  PRIMARY KEY (`zoneId`,`entry`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
