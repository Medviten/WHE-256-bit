-- Race ID
SET @Ogre                          := @NextRace := @NextRace +1; -- default: 15
SET @OgreMask                       = 1 << (@Ogre - 1);          -- race ID 15 → 16384
SET @OgreHelmetMask                 = 1 << @Ogre;                -- race ID 15 → 32768

-- Important variable updates (Alliance vs. Horde)
SET @HordeMask                      = @HordeMask    | @OgreMask;
SET @BarrensBros                    = @HordeMask    & ~@UndercityMask; -- important if Horde
SET @PlayableRaceMask               = @AllianceMask | @HordeMask;
SET @BowHunters                     = @BowHunters   | @OgreMask;
SET @OgreLanguage                   = 1; -- 7 for Alliance, 1 for Horde (ChrRaces.dbc)
SET @OgreAlliance                   = 1; -- 0 for Alliance, 1 for Horde (ChrRaces.dbc)
SET @OgreKnowThyEnemy               = @KnowThyEnemyHorde;

-- Miscellaneous
SET @OgreExplorationSound           = @OrcExplorationSound;
SET @OgreCinematicSequence          = @OrcCinematicSequence;
SET @OgreBlood                      = 1;
SET @OgreMaleModelPath              = 'Character\\Ogre\\Male\\OgrePC.mdx';
SET @OgreFemaleModelPath            = 'Character\\Ogre\\Female\\OgreMagePC.mdx';
SET @OgreMaleFootprint              = @FootprintShoe;
SET @OgreFemaleFootprint            = @FootprintShoe;

-- Strings
SET @OgreClientPrefix               = 'Og';
SET @OgreClientString               = 'Ogre';

-- Localization Strings
SET @OgreenUS                       = 'Ogre';
SET @OgrekoKR                       = '오우거';
SET @OgrefrFR                       = 'Ogre';
SET @OgredeDE                       = 'Oger';
SET @OgrezhCN                       = '食人魔';
SET @OgrezhTW                       = '巨魔';
SET @OgreesES                       = 'ogro';
SET @OgreesMX                       = 'ogro';
SET @OgreruRU                       = 'огр';
SET @OgrejaJP                       = '';
SET @OgreptPT                       = '';
SET @OgreitIT                       = '';

SET @OgreFemaleenUS                 = '';
SET @OgreFemalekoKR                 = '';
SET @OgreFemalefrFR                 = '';
SET @OgreFemaledeDE                 = '';
SET @OgreFemalezhCN                 = '';
SET @OgreFemalezhTW                 = '';
SET @OgreFemaleesES                 = '';
SET @OgreFemaleesMX                 = '';
SET @OgreFemaleruRU                 = '';
SET @OgreFemalejaJP                 = '';
SET @OgreFemaleptPT                 = '';
SET @OgreFemaleitIT                 = '';

SET @OgreMaleenUS                   = '';
SET @OgreMalekoKR                   = '';
SET @OgreMalefrFR                   = '';
SET @OgreMaledeDE                   = '';
SET @OgreMalezhCN                   = '';
SET @OgreMalezhTW                   = '';
SET @OgreMaleesES                   = '';
SET @OgreMaleesMX                   = '';
SET @OgreMaleruRU                   = '';
SET @OgreMalejaJP                   = '';
SET @OgreMaleptPT                   = '';
SET @OgreMaleitIT                   = '';

SET @OgreRacialNameenUS             = 'Racial - Ogre';
SET @OgreRacialNamekoKR             = '';
SET @OgreRacialNamefrFR             = '';
SET @OgreRacialNamedeDE             = '';
SET @OgreRacialNamezhCN             = '';
SET @OgreRacialNamezhTW             = '';
SET @OgreRacialNameesES             = '';
SET @OgreRacialNameesMX             = '';
SET @OgreRacialNameruRU             = '';
SET @OgreRacialNamejaJP             = '';
SET @OgreRacialNameptPT             = '';
SET @OgreRacialNameitIT             = '';

SET @OgrePlayerenUS                 = '"PLAYER", Ogre';
SET @OgrePlayerkoKR                 = '플레이어 - 오우거';
SET @OgrePlayerfrFR                 = '"JOUEUR", Ogre';
SET @OgrePlayerdeDE                 = '"SPIELER", Oger';
SET @OgrePlayerzhCN                 = '食人魔(玩家)';
SET @OgrePlayerzhTW                 = '巨魔(玩家)';
SET @OgrePlayeresES                 = '"JUGADOR", ogro';
SET @OgrePlayeresMX                 = '"JUGADOR", ogro';
SET @OgrePlayerruRU                 = 'ИГРОК: огр';
SET @OgrePlayerjaJP                 = '';
SET @OgrePlayerptPT                 = '';
SET @OgrePlayeritIT                 = '';

SET @OgreFactionNameenUS            = 'Stonemaul Clan';
SET @OgreFactionNamekoKR            = '돌망치 부족';
SET @OgreFactionNamefrFR            = 'Clan Cognepierre';
SET @OgreFactionNamedeDE            = 'Steinbrecherklan';
SET @OgreFactionNamezhCN            = '石槌氏族';
SET @OgreFactionNamezhTW            = '石槌氏族';
SET @OgreFactionNameesES            = 'Clan Quebrantarrocas';
SET @OgreFactionNameesMX            = 'Clan Quebrantarrocas';
SET @OgreFactionNameruRU            = 'Клан Каменного Молота';
SET @OgreFactionNamejaJP            = '';
SET @OgreFactionNameptPT            = '';
SET @OgreFactionNameitIT            = '';

SET @OgreFactionDescriptionenUS     = 'Ogres of the Stonemaul clan, sworn to the Horde.';
SET @OgreFactionDescriptionkoKR     = '호드에 충성을 맹세한 돌망치 부족 오우거입니다.';
SET @OgreFactionDescriptionfrFR     = 'Ogres du clan Cognepierre ayant juré fidélité à la Horde.';
SET @OgreFactionDescriptiondeDE     = 'Oger des Steinbrecherklans, die der Horde die Treue geschworen haben.';
SET @OgreFactionDescriptionzhCN     = '效忠部落的石槌氏族食人魔。';
SET @OgreFactionDescriptionzhTW     = '效忠部落的石槌氏族巨魔。';
SET @OgreFactionDescriptionesES     = 'Ogros del clan Quebrantarrocas que juraron lealtad a la Horda.';
SET @OgreFactionDescriptionesMX     = 'Ogros del clan Quebrantarrocas que juraron lealtad a la Horda.';
SET @OgreFactionDescriptionruRU     = 'Огры клана Каменного Молота, присягнувшие Орде.';
SET @OgreFactionDescriptionjaJP     = '';
SET @OgreFactionDescriptionptPT     = '';
SET @OgreFactionDescriptionitIT     = '';

SET @OgreAchievementenUS            = 'Realm First! Level 80 Ogre';
SET @OgreAchievementkoKR            = '';
SET @OgreAchievementfrFR            = '';
SET @OgreAchievementdeDE            = '';
SET @OgreAchievementzhCN            = '';
SET @OgreAchievementzhTW            = '';
SET @OgreAchievementesES            = '';
SET @OgreAchievementesMX            = '';
SET @OgreAchievementruRU            = '';
SET @OgreAchievementjaJP            = '';
SET @OgreAchievementptPT            = '';
SET @OgreAchievementitIT            = '';

SET @OgreAchievementDescriptionenUS = 'First Ogre on the realm to achieve level 80.';
SET @OgreAchievementDescriptionkoKR = '';
SET @OgreAchievementDescriptionfrFR = '';
SET @OgreAchievementDescriptiondeDE = '';
SET @OgreAchievementDescriptionzhCN = '';
SET @OgreAchievementDescriptionzhTW = '';
SET @OgreAchievementDescriptionesES = '';
SET @OgreAchievementDescriptionesMX = '';
SET @OgreAchievementDescriptionruRU = '';
SET @OgreAchievementDescriptionjaJP = '';
SET @OgreAchievementDescriptionptPT = '';
SET @OgreAchievementDescriptionitIT = '';
