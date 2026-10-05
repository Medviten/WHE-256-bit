-- characterfacialhairstyles: 16 inserts, 0 updates, 0 deletes

-- Insertions
DELETE FROM `characterfacialhairstyles` WHERE `race` = (@Vulpera);
INSERT INTO `characterfacialhairstyles` (`race`, `gender`, `variation_id`, `geoset_1`, `geoset_2`, `geoset_3`, `geoset_4`, `geoset_5`) VALUES
(@Vulpera, @Male,    1, 1, 0, 2, 0, 0), -- favourite
(@Vulpera, @Male,    2, 1, 0, 3, 0, 0), -- short and cute
(@Vulpera, @Male,    3, 1, 0, 4, 0, 0), -- long and pointy
(@Vulpera, @Male,    4, 1, 0, 5, 0, 0), -- horn-like pointy
(@Vulpera, @Male,    5, 1, 0, 6, 0, 0), -- big and long
(@Vulpera, @Male,    6, 2, 0, 2, 0, 0), -- favourite, left earring
(@Vulpera, @Male,    7, 2, 0, 3, 0, 0), -- short and cute, left earring
(@Vulpera, @Male,    8, 2, 0, 4, 0, 0), -- long and pointy, left earring
(@Vulpera, @Male,    9, 2, 0, 5, 0, 0), -- horn-like pointy, left earring
(@Vulpera, @Male,   10, 2, 0, 6, 0, 0), -- big and long, left earring
(@Vulpera, @Male,   11, 3, 0, 2, 0, 0), -- favourite, two right earrings
(@Vulpera, @Male,   12, 3, 0, 3, 0, 0), -- short and cute, two right earrings (fit)
(@Vulpera, @Male,   13, 3, 0, 4, 0, 0), -- long and pointy, two right earrings (barely touch)
(@Vulpera, @Male,   14, 3, 0, 5, 0, 0), -- horn-like pointy, two right earrings (barely fit)
(@Vulpera, @Male,   15, 3, 0, 6, 0, 0), -- big and long, two right earrings (fit)
(@Vulpera, @Male,   16, 4, 0, 2, 0, 0), -- favourite, one ring either side (barely fit)
(@Vulpera, @Male,   17, 4, 0, 3, 0, 0), -- short and cute, one ring either side (barely fit)
(@Vulpera, @Male,   18, 4, 0, 4, 0, 0), -- long and pointy, one ring either side (fit)
(@Vulpera, @Male,   19, 4, 0, 5, 0, 0), -- horn-like pointy, one ring either side (barely fit)
(@Vulpera, @Male,   20, 4, 0, 6, 0, 0), -- big and long, one ring either side (fit)
(@Vulpera, @Male,   21, 5, 0, 2, 0, 0), -- favourite, right earring (fit)
(@Vulpera, @Male,   22, 5, 0, 3, 0, 0), -- short and cute, right earring (fit)
(@Vulpera, @Male,   23, 5, 0, 4, 0, 0), -- long and pointy, right earring (barely touches)
(@Vulpera, @Male,   24, 5, 0, 5, 0, 0), -- horn-like pointy, right earring (fit)
(@Vulpera, @Male,   25, 5, 0, 6, 0, 0), -- big and long, right earring (fit)
(@Vulpera, @Male,   26, 6, 0, 6, 0, 0), -- big and long, three left earrings (fit)
(@Vulpera, @Female, 27, 1, 0, 2, 0, 0), -- big and long
(@Vulpera, @Female, 28, 1, 0, 3, 0, 0), -- short and pointy
(@Vulpera, @Female, 29, 1, 0, 4, 0, 0), -- big and round
(@Vulpera, @Female, 30, 1, 0, 5, 0, 0), -- bent forward
(@Vulpera, @Female, 31, 1, 0, 6, 0, 0), -- tube-curled
(@Vulpera, @Female, 32, 1, 0, 7, 0, 0), -- sharp and curled
(@Vulpera, @Female, 33, 1, 0, 8, 0, 0), -- one tip missing
(@Vulpera, @Female, 34, 2, 0, 2, 0, 0), -- big and long, three rings (2–1, fit)
(@Vulpera, @Female, 35, 2, 0, 4, 0, 0), -- long and round, three rings (2–1, fit)
(@Vulpera, @Female, 36, 2, 0, 6, 0, 0), -- tube-curled, three rings (2–1, barely touching)
(@Vulpera, @Female, 37, 2, 0, 7, 0, 0), -- sharp and curled, three rings (2–1, barely touching)
(@Vulpera, @Female, 38, 3, 0, 3, 0, 0), -- short and pointy, three rings bent up (2–1, fit)
(@Vulpera, @Female, 39, 3, 0, 8, 0, 0), -- one tip missing, three rings bent up (2–1, barely fit)
(@Vulpera, @Female, 40, 4, 0, 2, 0, 0), -- big and long, four rings (2–2, fit)
(@Vulpera, @Female, 41, 4, 0, 3, 0, 0), -- short and pointy, four rings (2–2, fit)
(@Vulpera, @Female, 42, 4, 0, 4, 0, 0), -- big and round, four rings (2–2, fit)
(@Vulpera, @Female, 43, 4, 0, 5, 0, 0), -- bent forward, four rings (2–2, barely touch)
(@Vulpera, @Female, 44, 4, 0, 6, 0, 0), -- tube-curled, four rings (2–2, barely touch)
(@Vulpera, @Female, 45, 4, 0, 7, 0, 0), -- sharp and curled, four rings (2–2, barely fit)
(@Vulpera, @Female, 46, 4, 0, 8, 0, 0), -- one tip missing, four rings (2–2, barely fit)
(@Vulpera, @Female, 47, 5, 0, 3, 0, 0), -- short and pointy, two rings (1–1, fit)
(@Vulpera, @Female, 48, 5, 0, 4, 0, 0), -- big and round, two rings (1–1, fit)
(@Vulpera, @Female, 49, 5, 0, 5, 0, 0), -- bent forward, two rings (1–1, fit)
(@Vulpera, @Female, 50, 5, 0, 6, 0, 0), -- tube-curled, two rings (1–1, fit)
(@Vulpera, @Female, 51, 5, 0, 7, 0, 0), -- sharp and curled, two rings (1–1, barely fit)
(@Vulpera, @Female, 52, 5, 0, 8, 0, 0), -- one tip missing, two rings (1–1, fit)
(@Vulpera, @Female, 53, 6, 0, 6, 0, 0); -- tube-curled, three rings left (fit)
