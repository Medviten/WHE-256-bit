-- [F-130] The Worgen cinematic (Cataclysm's movie 21: the cure, "Look at what you've become"), played when Last Stand
-- (14222) is turned in. Cataclysm plays it through spell 93477's effect 45 (PLAY_MOVIE), which is ADD_HONOR in
-- AzerothCore, so cata_gilneas_port.py has the quest ender's SmartAI play the movie instead (MOVIE_SPELLS).
--
-- Ids are Cataclysm's: movie 21, variation 122, file 455943. The file is Interface\Cinematics\Worgen_1024.avi in
-- WHE-common's patch-A.MPQ (shipped as patch-WHE-cinematics.MPQ), re-encoded from MoP Classic's 1280 x 720 VP9 video
-- and separate MP3 to the 1024 x 576 MPEG-4 the 3.3.5a client plays. The client builds the name as
-- Movie.movie_path + "_" + MovieFileData.resolution + ".avi" and skips a variation without a FileData row (see F-013's
-- [F-013]_goblin_cinematic.sql). The subtitles (.sbt) aren't shown.

DELETE FROM `movie` WHERE `id` = 21;
INSERT INTO `movie` (`id`, `movie_path`, `volume`) VALUES (21, 'Interface\\Cinematics\\Worgen', 100);

DELETE FROM `filedata` WHERE `id` = 455943;
INSERT INTO `filedata` (`id`, `file_name`, `file_path`) VALUES (455943, 'Worgen_1024.avi', 'Interface\\Cinematics\\');

DELETE FROM `moviefiledata` WHERE `id` = 455943;
INSERT INTO `moviefiledata` (`id`, `resolution`) VALUES (455943, 1024);

DELETE FROM `movievariation` WHERE `id` = 122;
INSERT INTO `movievariation` (`id`, `movie_id`, `file_data_id`) VALUES (122, 21, 455943);
