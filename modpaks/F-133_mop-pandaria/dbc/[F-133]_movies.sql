-- MoP's faction intro movies, for the first trip to Pandaria: 119 mop_wra (Varian sends an elite force after Anduin,
-- Alliance), 120 mop_wrh (Garrosh redirects the invasion fleet, Horde), 121 mop_jade_crash (the gunship crashing in
-- the Jade Forest). Movie ids are MoP's own. MoP ships 1280 x 720 VP9 video with the sound in a separate .mp3; the
-- files here are re-encoded to what the 3.3.5a client plays (1024 x 576 MPEG-4, MP3 inside, like Goblin_1024.avi):
-- Interface\Cinematics\<name>_1024.avi in WHE-common's patch-MoP.MPQ. mop_jade (118, the Jade Forest battle) is left
-- out: its downloaded sound is damaged.
--
-- The client builds the file name as Movie.movie_path + "_" + MovieFileData.resolution + ".avi" and skips a
-- variation without a FileData row (see F-013's [F-013]_goblin_cinematic.sql). MoP's subtitles (.sbt) aren't shown.

DELETE FROM `movie` WHERE `id` IN (119, 120, 121);
INSERT INTO `movie` (`id`, `movie_path`, `volume`) VALUES
  (119, 'Interface\Cinematics\mop_wra', 100),
  (120, 'Interface\Cinematics\mop_wrh', 100),
  (121, 'Interface\Cinematics\mop_jade_crash', 100);

DELETE FROM `filedata` WHERE `id` IN (1330119, 1330120, 1330121);
INSERT INTO `filedata` (`id`, `file_name`, `file_path`) VALUES
  (1330119, 'mop_wra_1024.avi', 'Interface\Cinematics\'),
  (1330120, 'mop_wrh_1024.avi', 'Interface\Cinematics\'),
  (1330121, 'mop_jade_crash_1024.avi', 'Interface\Cinematics\');

DELETE FROM `moviefiledata` WHERE `id` IN (1330119, 1330120, 1330121);
INSERT INTO `moviefiledata` (`id`, `resolution`) VALUES (1330119, 1024), (1330120, 1024), (1330121, 1024);

DELETE FROM `movievariation` WHERE `id` IN (1330119, 1330120, 1330121);
INSERT INTO `movievariation` (`id`, `movie_id`, `file_data_id`) VALUES
  (1330119, 119, 1330119), (1330120, 120, 1330120), (1330121, 121, 1330121);
