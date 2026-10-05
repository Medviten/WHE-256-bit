-- characterfacialhairstyles: 16 inserts, 0 updates, 0 deletes

-- Insertions
DELETE FROM `characterfacialhairstyles` WHERE `race` = (@Vulpera);
INSERT INTO `characterfacialhairstyles` (`race`, `gender`, `variation_id`, `geoset_1`, `geoset_2`, `geoset_3`, `geoset_4`, `geoset_5`) VALUES
(@Vulpera, @Male,    2, 1, 0, 2, 0, 0), -- favourite
(@Vulpera, @Male,    4, 1, 0, 3, 0, 0), -- short and cute
(@Vulpera, @Male,    6, 1, 0, 4, 0, 0), -- long and pointy
(@Vulpera, @Male,    8, 1, 0, 5, 0, 0), -- horn-like pointy
(@Vulpera, @Male,   10, 1, 0, 6, 0, 0), -- big and long
(@Vulpera, @Male,   14, 2, 0, 2, 0, 0), -- favourite, left earring
(@Vulpera, @Male,   16, 2, 0, 3, 0, 0), -- short and cute, left earring
(@Vulpera, @Male,   18, 2, 0, 4, 0, 0), -- long and pointy, left earring
(@Vulpera, @Male,   20, 2, 0, 5, 0, 0), -- horn-like pointy, left earring
(@Vulpera, @Male,   22, 2, 0, 6, 0, 0), -- big and long, left earring
(@Vulpera, @Male,   26, 3, 0, 2, 0, 0), -- favourite, two right earrings
(@Vulpera, @Male,   28, 3, 0, 3, 0, 0), -- short and cute, two right earrings (fit)
(@Vulpera, @Male,   30, 3, 0, 4, 0, 0), -- long and pointy, two right earrings (barely touch)
(@Vulpera, @Male,   32, 3, 0, 5, 0, 0), -- horn-like pointy, two right earrings (barely fit)
(@Vulpera, @Male,   34, 3, 0, 6, 0, 0), -- big and long, two right earrings (fit)
(@Vulpera, @Male,   38, 4, 0, 2, 0, 0), -- favourite, one ring either side (barely fit)
(@Vulpera, @Male,   40, 4, 0, 3, 0, 0), -- short and cute, one ring either side (barely fit)
(@Vulpera, @Male,   42, 4, 0, 4, 0, 0), -- long and pointy, one ring either side (fit)
(@Vulpera, @Male,   44, 4, 0, 5, 0, 0), -- horn-like pointy, one ring either side (barely fit)
(@Vulpera, @Male,   46, 4, 0, 6, 0, 0), -- big and long, one ring either side (fit)
(@Vulpera, @Male,   50, 5, 0, 2, 0, 0), -- favourite, right earring (fit)
(@Vulpera, @Male,   52, 5, 0, 3, 0, 0), -- short and cute, right earring (fit)
(@Vulpera, @Male,   54, 5, 0, 4, 0, 0), -- long and pointy, right earring (barely touches)
(@Vulpera, @Male,   56, 5, 0, 5, 0, 0), -- horn-like pointy, right earring (fit)
(@Vulpera, @Male,   58, 5, 0, 6, 0, 0), -- big and long, right earring (fit)
(@Vulpera, @Male,   70, 6, 0, 6, 0, 0), -- big and long, three left earrings (fit)
(@Vulpera, @Female,  2, 1, 0, 2, 0, 0), -- big and long
(@Vulpera, @Female,  4, 1, 0, 3, 0, 0), -- short and pointy
(@Vulpera, @Female,  6, 1, 0, 4, 0, 0), -- big and round
(@Vulpera, @Female,  8, 1, 0, 5, 0, 0), -- bent forward
(@Vulpera, @Female, 10, 1, 0, 6, 0, 0), -- tube-curled
(@Vulpera, @Female, 12, 1, 0, 7, 0, 0), -- sharp and curled
(@Vulpera, @Female, 14, 1, 0, 8, 0, 0), -- one tip missing
(@Vulpera, @Female, 18, 2, 0, 2, 0, 0), -- big and long, three rings (2–1, fit)
(@Vulpera, @Female, 22, 2, 0, 4, 0, 0), -- long and round, three rings (2–1, fit)
(@Vulpera, @Female, 26, 2, 0, 6, 0, 0), -- tube-curled, three rings (2–1, barely touching)
(@Vulpera, @Female, 28, 2, 0, 7, 0, 0), -- sharp and curled, three rings (2–1, barely touching)
(@Vulpera, @Female, 36, 3, 0, 3, 0, 0), -- short and pointy, three rings bent up (2–1, fit)
(@Vulpera, @Female, 46, 3, 0, 8, 0, 0), -- one tip missing, three rings bent up (2–1, barely fit)
(@Vulpera, @Female, 50, 4, 0, 2, 0, 0), -- big and long, four rings (2–2, fit)
(@Vulpera, @Female, 52, 4, 0, 3, 0, 0), -- short and pointy, four rings (2–2, fit)
(@Vulpera, @Female, 54, 4, 0, 4, 0, 0), -- big and round, four rings (2–2, fit)
(@Vulpera, @Female, 56, 4, 0, 5, 0, 0), -- bent forward, four rings (2–2, barely touch)
(@Vulpera, @Female, 58, 4, 0, 6, 0, 0), -- tube-curled, four rings (2–2, barely touch)
(@Vulpera, @Female, 60, 4, 0, 7, 0, 0), -- sharp and curled, four rings (2–2, barely fit)
(@Vulpera, @Female, 62, 4, 0, 8, 0, 0), -- one tip missing, four rings (2–2, barely fit)
(@Vulpera, @Female, 68, 5, 0, 3, 0, 0), -- short and pointy, two rings (1–1, fit)
(@Vulpera, @Female, 70, 5, 0, 4, 0, 0), -- big and round, two rings (1–1, fit)
(@Vulpera, @Female, 72, 5, 0, 5, 0, 0), -- bent forward, two rings (1–1, fit)
(@Vulpera, @Female, 74, 5, 0, 6, 0, 0), -- tube-curled, two rings (1–1, fit)
(@Vulpera, @Female, 76, 5, 0, 7, 0, 0), -- sharp and curled, two rings (1–1, barely fit)
(@Vulpera, @Female, 78, 5, 0, 8, 0, 0), -- one tip missing, two rings (1–1, fit)
(@Vulpera, @Female, 90, 6, 0, 6, 0, 0), -- tube-curled, three rings left (fit)
