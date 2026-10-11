-- characterfacialhairstyles: 53 inserts, 0 updates, 0 deletes

-- Insertions
DELETE FROM `characterfacialhairstyles` WHERE `race` = (@Nightborne);
INSERT INTO `characterfacialhairstyles` (`race`, `gender`, `variation_id`, `geoset_1`, `geoset_2`, `geoset_3`, `geoset_4`, `geoset_5`) VALUES
(@Nightborne, @Male,    1, 1, 0, 2, 0, 0), -- favourite
(@Nightborne, @Male,    2, 1, 0, 3, 0, 0), -- short and cute
(@Nightborne, @Male,    3, 1, 0, 4, 0, 0), -- long and pointy
(@Nightborne, @Male,    4, 1, 0, 5, 0, 0), -- horn-like pointy
(@Nightborne, @Male,    5, 1, 0, 6, 0, 0), -- big and long
(@Nightborne, @Male,    6, 2, 0, 2, 0, 0), -- favourite, left earring
(@Nightborne, @Male,    7, 2, 0, 3, 0, 0), -- short and cute, left earring
(@Nightborne, @Male,    8, 2, 0, 4, 0, 0), -- long and pointy, left earring
(@Nightborne, @Male,    9, 2, 0, 5, 0, 0), -- horn-like pointy, left earring
(@Nightborne, @Male,   10, 2, 0, 6, 0, 0), -- big and long, left earring
(@Nightborne, @Male,   11, 3, 0, 2, 0, 0), -- favourite, two right earrings
(@Nightborne, @Male,   12, 3, 0, 3, 0, 0), -- short and cute, two right earrings (fit)
(@Nightborne, @Male,   13, 3, 0, 4, 0, 0), -- long and pointy, two right earrings (barely touch)
(@Nightborne, @Male,   14, 3, 0, 5, 0, 0), -- horn-like pointy, two right earrings (barely fit)
(@Nightborne, @Male,   15, 3, 0, 6, 0, 0), -- big and long, two right earrings (fit)
(@Nightborne, @Male,   16, 4, 0, 2, 0, 0), -- favourite, one ring either side (barely fit)
(@Nightborne, @Male,   17, 4, 0, 3, 0, 0), -- short and cute, one ring either side (barely fit)
(@Nightborne, @Male,   18, 4, 0, 4, 0, 0), -- long and pointy, one ring either side (fit)
(@Nightborne, @Male,   19, 4, 0, 5, 0, 0), -- horn-like pointy, one ring either side (barely fit)
(@Nightborne, @Male,   20, 4, 0, 6, 0, 0), -- big and long, one ring either side (fit)
(@Nightborne, @Male,   21, 5, 0, 2, 0, 0), -- favourite, right earring (fit)
(@Nightborne, @Male,   22, 5, 0, 3, 0, 0), -- short and cute, right earring (fit)
(@Nightborne, @Male,   23, 5, 0, 4, 0, 0), -- long and pointy, right earring (barely touches)
(@Nightborne, @Male,   24, 5, 0, 5, 0, 0), -- horn-like pointy, right earring (fit)
(@Nightborne, @Male,   25, 5, 0, 6, 0, 0), -- big and long, right earring (fit)
(@Nightborne, @Male,   26, 6, 0, 6, 0, 0), -- big and long, three left earrings (fit)
(@Nightborne, @Female,  1, 1, 0, 2, 0, 0), -- big and long
(@Nightborne, @Female,  2, 1, 0, 3, 0, 0), -- short and pointy
(@Nightborne, @Female,  3, 1, 0, 4, 0, 0), -- big and round
(@Nightborne, @Female,  4, 1, 0, 5, 0, 0), -- bent forward
(@Nightborne, @Female,  5, 1, 0, 6, 0, 0), -- tube-curled
(@Nightborne, @Female,  6, 1, 0, 7, 0, 0), -- sharp and curled
(@Nightborne, @Female,  7, 1, 0, 8, 0, 0), -- one tip missing
(@Nightborne, @Female,  8, 2, 0, 2, 0, 0), -- big and long, three rings (2–1, fit)
(@Nightborne, @Female,  9, 2, 0, 4, 0, 0), -- long and round, three rings (2–1, fit)
(@Nightborne, @Female, 10, 2, 0, 6, 0, 0), -- tube-curled, three rings (2–1, barely touching)
(@Nightborne, @Female, 11, 2, 0, 7, 0, 0), -- sharp and curled, three rings (2–1, barely touching)
(@Nightborne, @Female, 12, 3, 0, 3, 0, 0), -- short and pointy, three rings bent up (2–1, fit)
(@Nightborne, @Female, 13, 3, 0, 8, 0, 0), -- one tip missing, three rings bent up (2–1, barely fit)
(@Nightborne, @Female, 14, 4, 0, 2, 0, 0), -- big and long, four rings (2–2, fit)
(@Nightborne, @Female, 15, 4, 0, 3, 0, 0), -- short and pointy, four rings (2–2, fit)
(@Nightborne, @Female, 16, 4, 0, 4, 0, 0), -- big and round, four rings (2–2, fit)
(@Nightborne, @Female, 17, 4, 0, 5, 0, 0), -- bent forward, four rings (2–2, barely touch)
(@Nightborne, @Female, 18, 4, 0, 6, 0, 0), -- tube-curled, four rings (2–2, barely touch)
(@Nightborne, @Female, 19, 4, 0, 7, 0, 0), -- sharp and curled, four rings (2–2, barely fit)
(@Nightborne, @Female, 20, 4, 0, 8, 0, 0), -- one tip missing, four rings (2–2, barely fit)
(@Nightborne, @Female, 21, 5, 0, 3, 0, 0), -- short and pointy, two rings (1–1, fit)
(@Nightborne, @Female, 22, 5, 0, 4, 0, 0), -- big and round, two rings (1–1, fit)
(@Nightborne, @Female, 23, 5, 0, 5, 0, 0), -- bent forward, two rings (1–1, fit)
(@Nightborne, @Female, 24, 5, 0, 6, 0, 0), -- tube-curled, two rings (1–1, fit)
(@Nightborne, @Female, 25, 5, 0, 7, 0, 0), -- sharp and curled, two rings (1–1, barely fit)
(@Nightborne, @Female, 26, 5, 0, 8, 0, 0), -- one tip missing, two rings (1–1, fit)
(@Nightborne, @Female, 27, 6, 0, 6, 0, 0); -- tube-curled, three rings left (fit)
