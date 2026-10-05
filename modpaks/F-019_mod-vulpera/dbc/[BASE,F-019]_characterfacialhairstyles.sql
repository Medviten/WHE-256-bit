-- characterfacialhairstyles: 16 inserts, 0 updates, 0 deletes

-- Insertions
DELETE FROM `characterfacialhairstyles` WHERE `race` = (@Vulpera);
INSERT INTO `characterfacialhairstyles` (`race`, `gender`, `variation_id`, `geoset_1`, `geoset_2`, `geoset_3`, `geoset_4`, `geoset_5`) VALUES
(@Vulpera, @Male,    0, 1, 0, 1, 0, 0), -- no ears
(@Vulpera, @Male,    1, 1, 1, 1, 0, 0), -- duplicate
(@Vulpera, @Male,    2, 1, 0, 2, 0, 0), -- favourite
(@Vulpera, @Male,    3, 1, 2, 2, 0, 0), -- duplicate
(@Vulpera, @Male,    4, 1, 0, 3, 0, 0), -- short and cute
(@Vulpera, @Male,    5, 1, 3, 3, 0, 0), -- duplicate
(@Vulpera, @Male,    6, 1, 0, 4, 0, 0), -- long and pointy
(@Vulpera, @Male,    7, 1, 4, 4, 0, 0), -- duplicate
(@Vulpera, @Male,    8, 1, 0, 5, 0, 0), -- horn-like pointy
(@Vulpera, @Male,    9, 1, 5, 5, 0, 0), -- duplicate
(@Vulpera, @Male,   10, 1, 0, 6, 0, 0), -- big and long
(@Vulpera, @Male,   11, 1, 6, 6, 0, 0), -- duplicate
(@Vulpera, @Male,   12, 2, 0, 1, 0, 0), -- no ears, left earring
(@Vulpera, @Male,   13, 2, 1, 1, 0, 0), -- duplicate
(@Vulpera, @Male,   14, 2, 0, 2, 0, 0), -- favourite, left earring
(@Vulpera, @Male,   15, 2, 2, 2, 0, 0), -- duplicate
(@Vulpera, @Male,   16, 2, 0, 3, 0, 0), -- short and cute, left earring
(@Vulpera, @Male,   17, 2, 3, 3, 0, 0), -- duplicate
(@Vulpera, @Male,   18, 2, 0, 4, 0, 0), -- long and pointy, left earring
(@Vulpera, @Male,   19, 2, 4, 4, 0, 0), -- duplicate
(@Vulpera, @Male,   20, 2, 0, 5, 0, 0), -- horn-like pointy, left earring
(@Vulpera, @Male,   21, 2, 5, 5, 0, 0), -- duplicate
(@Vulpera, @Male,   22, 2, 0, 6, 0, 0), -- big and long, left earring
(@Vulpera, @Male,   23, 2, 6, 6, 0, 0), -- duplicate
(@Vulpera, @Male,   24, 3, 0, 1, 0, 0), -- no ears, two right earrings
(@Vulpera, @Male,   25, 3, 1, 1, 0, 0), -- duplicate
(@Vulpera, @Male,   26, 3, 0, 2, 0, 0), -- favourite, two right earrings
(@Vulpera, @Male,   27, 3, 2, 2, 0, 0), -- duplicate
(@Vulpera, @Male,   28, 3, 0, 3, 0, 0), -- short and cute, two right earrings (fit)
(@Vulpera, @Male,   29, 3, 3, 3, 0, 0), -- duplicate
(@Vulpera, @Male,   30, 3, 0, 4, 0, 0), -- long and pointy, two right earrings (barely touch)
(@Vulpera, @Male,   31, 3, 4, 4, 0, 0), -- duplicate
(@Vulpera, @Male,   32, 3, 0, 5, 0, 0), -- horn-like pointy, two right earrings (barely fit)
(@Vulpera, @Male,   33, 3, 5, 5, 0, 0), -- duplicate
(@Vulpera, @Male,   34, 3, 0, 6, 0, 0), -- big and long, two right earrings (fit)
(@Vulpera, @Male,   35, 3, 6, 6, 0, 0), -- duplicate
(@Vulpera, @Male,   36, 4, 0, 1, 0, 0), -- no ears, one ring either side
(@Vulpera, @Male,   37, 4, 1, 1, 0, 0), -- duplicate
(@Vulpera, @Male,   38, 4, 0, 2, 0, 0), -- favourite, one ring either side (barely fit)
(@Vulpera, @Male,   39, 4, 2, 2, 0, 0), -- duplicate
(@Vulpera, @Male,   40, 4, 0, 3, 0, 0), -- short and cute, one ring either side (barely fit)
(@Vulpera, @Male,   41, 4, 3, 3, 0, 0), -- duplicate
(@Vulpera, @Male,   42, 4, 0, 4, 0, 0), -- long and pointy, one ring either side (fit)
(@Vulpera, @Male,   43, 4, 4, 4, 0, 0), -- duplicate
(@Vulpera, @Male,   44, 4, 0, 5, 0, 0), -- horn-like pointy, one ring either side (barely fit)
(@Vulpera, @Male,   45, 4, 5, 5, 0, 0), -- duplicate
(@Vulpera, @Male,   46, 4, 0, 6, 0, 0), -- big and long, one ring either side (fit)
(@Vulpera, @Male,   47, 4, 6, 6, 0, 0), -- duplicate
(@Vulpera, @Male,   48, 5, 0, 1, 0, 0), -- no ears, right earring
(@Vulpera, @Male,   49, 5, 1, 1, 0, 0), -- duplicate
(@Vulpera, @Male,   50, 5, 0, 2, 0, 0), -- favourite, right earring (fit)
(@Vulpera, @Male,   51, 5, 2, 2, 0, 0), -- duplicate
(@Vulpera, @Male,   52, 5, 0, 3, 0, 0), -- short and cute, right earring (fit)
(@Vulpera, @Male,   53, 5, 3, 3, 0, 0), -- duplicate
(@Vulpera, @Male,   54, 5, 0, 4, 0, 0), -- long and pointy, right earring (barely touches)
(@Vulpera, @Male,   55, 5, 4, 4, 0, 0), -- duplicate
(@Vulpera, @Male,   56, 5, 0, 5, 0, 0), -- horn-like pointy, right earring (fit)
(@Vulpera, @Male,   57, 5, 5, 5, 0, 0), -- duplicate
(@Vulpera, @Male,   58, 5, 0, 6, 0, 0), -- big and long, right earring (fit)
(@Vulpera, @Male,   59, 5, 6, 6, 0, 0), -- duplicate
(@Vulpera, @Male,   60, 6, 0, 1, 0, 0), -- no ears, three left earrings
(@Vulpera, @Male,   61, 6, 1, 1, 0, 0), -- duplicate
(@Vulpera, @Male,   62, 6, 0, 2, 0, 0), -- favourite, three left earrings (two float)
(@Vulpera, @Male,   63, 6, 2, 2, 0, 0), -- duplicate
(@Vulpera, @Male,   64, 6, 0, 3, 0, 0), -- short and cute, three left earrings (two float)
(@Vulpera, @Male,   65, 6, 3, 3, 0, 0), -- duplicate
(@Vulpera, @Male,   66, 6, 0, 4, 0, 0), -- long and pointy, three left earrings (two float)
(@Vulpera, @Male,   67, 6, 4, 4, 0, 0), -- duplicate
(@Vulpera, @Male,   68, 6, 0, 5, 0, 0), -- horn-like pointy, three left earrings (two float)
(@Vulpera, @Male,   69, 6, 5, 5, 0, 0), -- duplicate
(@Vulpera, @Male,   70, 6, 0, 6, 0, 0), -- big and long, three left earrings (fit)
(@Vulpera, @Male,   71, 6, 6, 6, 0, 0), -- duplicate
(@Vulpera, @Female,  0, 1, 0, 1, 0, 0), -- no ears
(@Vulpera, @Female,  1, 1, 1, 1, 0, 0), -- duplicate
(@Vulpera, @Female,  2, 1, 0, 2, 0, 0), -- big and long
(@Vulpera, @Female,  3, 1, 2, 2, 0, 0), -- duplicate
(@Vulpera, @Female,  4, 1, 0, 3, 0, 0), -- short and pointy
(@Vulpera, @Female,  5, 1, 3, 3, 0, 0), -- duplicate
(@Vulpera, @Female,  6, 1, 0, 4, 0, 0), -- big and round
(@Vulpera, @Female,  7, 1, 4, 4, 0, 0), -- duplicate
(@Vulpera, @Female,  8, 1, 0, 5, 0, 0), -- bent forward
(@Vulpera, @Female,  9, 1, 5, 5, 0, 0), -- duplicate
(@Vulpera, @Female, 10, 1, 0, 6, 0, 0), -- tube-curled
(@Vulpera, @Female, 11, 1, 6, 6, 0, 0), -- duplicate
(@Vulpera, @Female, 12, 1, 0, 7, 0, 0), -- sharp and curled
(@Vulpera, @Female, 13, 1, 7, 7, 0, 0), -- duplicate
(@Vulpera, @Female, 14, 1, 0, 8, 0, 0), -- one tip missing
(@Vulpera, @Female, 15, 1, 8, 8, 0, 0), -- duplicate
(@Vulpera, @Female, 16, 2, 0, 1, 0, 0), -- no ears, three rings (2–1)
(@Vulpera, @Female, 17, 2, 1, 1, 0, 0), -- duplicate
(@Vulpera, @Female, 18, 2, 0, 2, 0, 0), -- big and long, three rings (2–1, fit)
(@Vulpera, @Female, 19, 2, 2, 2, 0, 0), -- duplicate
(@Vulpera, @Female, 20, 2, 0, 3, 0, 0), -- short and sharp, three rings (2–1, one floats)
(@Vulpera, @Female, 21, 2, 3, 3, 0, 0), -- duplicate
(@Vulpera, @Female, 22, 2, 0, 4, 0, 0), -- long and round, three rings (2–1, fit)
(@Vulpera, @Female, 23, 2, 4, 4, 0, 0), -- duplicate
(@Vulpera, @Female, 24, 2, 0, 5, 0, 0), -- bent forward, three rings (2–1, floating)
(@Vulpera, @Female, 25, 2, 5, 5, 0, 0), -- duplicate
(@Vulpera, @Female, 26, 2, 0, 6, 0, 0), -- tube-curled, three rings (2–1, barely touching)
(@Vulpera, @Female, 27, 2, 6, 6, 0, 0), -- duplicate
(@Vulpera, @Female, 28, 2, 0, 7, 0, 0), -- sharp and curled, three rings (2–1, barely touching)
(@Vulpera, @Female, 29, 2, 7, 7, 0, 0), -- duplicate
(@Vulpera, @Female, 30, 2, 0, 8, 0, 0), -- one tip missing, three rings (2–1, floating)
(@Vulpera, @Female, 31, 2, 8, 8, 0, 0), -- duplicate
(@Vulpera, @Female, 32, 3, 0, 1, 0, 0), -- no ears, three rings bent up (2–1)
(@Vulpera, @Female, 33, 3, 1, 1, 0, 0), -- duplicate
(@Vulpera, @Female, 34, 3, 0, 2, 0, 0), -- big and long, three rings bent up (2–1, hidden behind)
(@Vulpera, @Female, 35, 3, 2, 2, 0, 0), -- duplicate
(@Vulpera, @Female, 36, 3, 0, 3, 0, 0), -- short and pointy, three rings bent up (2–1, fit)
(@Vulpera, @Female, 37, 3, 3, 3, 0, 0), -- duplicate
(@Vulpera, @Female, 38, 3, 0, 4, 0, 0), -- big and round, three rings bent up (2–1, hidden behind)
(@Vulpera, @Female, 39, 3, 4, 4, 0, 0), -- duplicate
(@Vulpera, @Female, 40, 3, 0, 5, 0, 0), -- bent forward, three rings bent up (2–1, floating)
(@Vulpera, @Female, 41, 3, 5, 5, 0, 0), -- duplicate
(@Vulpera, @Female, 42, 3, 0, 6, 0, 0), -- tube-curled, three rings bent up (2–1, hidden behind, clipping through)
(@Vulpera, @Female, 43, 3, 6, 6, 0, 0), -- duplicate
(@Vulpera, @Female, 44, 3, 0, 7, 0, 0), -- sharp and curled, three rings bent up (2–1, hidden behind, clipping through)
(@Vulpera, @Female, 45, 3, 7, 7, 0, 0), -- duplicate
(@Vulpera, @Female, 46, 3, 0, 8, 0, 0), -- one tip missing, three rings bent up (2–1, barely fit)
(@Vulpera, @Female, 47, 3, 8, 8, 0, 0), -- duplicate
(@Vulpera, @Female, 48, 4, 0, 1, 0, 0), -- no ears, four rings (2–2)
(@Vulpera, @Female, 49, 4, 1, 1, 0, 0), -- duplicate
(@Vulpera, @Female, 50, 4, 0, 2, 0, 0), -- big and long, four rings (2–2, fit)
(@Vulpera, @Female, 51, 4, 2, 2, 0, 0), -- duplicate
(@Vulpera, @Female, 52, 4, 0, 3, 0, 0), -- short and pointy, four rings (2–2, fit)
(@Vulpera, @Female, 53, 4, 3, 3, 0, 0), -- duplicate
(@Vulpera, @Female, 54, 4, 0, 4, 0, 0), -- big and round, four rings (2–2, fit)
(@Vulpera, @Female, 55, 4, 4, 4, 0, 0), -- duplicate
(@Vulpera, @Female, 56, 4, 0, 5, 0, 0), -- bent forward, four rings (2–2, barely touch)
(@Vulpera, @Female, 57, 4, 5, 5, 0, 0), -- duplicate
(@Vulpera, @Female, 58, 4, 0, 6, 0, 0), -- tube-curled, four rings (2–2, barely touch)
(@Vulpera, @Female, 59, 4, 6, 6, 0, 0), -- duplicate
(@Vulpera, @Female, 60, 4, 0, 7, 0, 0), -- sharp and curled, four rings (2–2, barely fit)
(@Vulpera, @Female, 61, 4, 7, 7, 0, 0), -- duplicate
(@Vulpera, @Female, 62, 4, 0, 8, 0, 0), -- one tip missing, four rings (2–2, barely fit)
(@Vulpera, @Female, 63, 4, 8, 8, 0, 0), -- duplicate
(@Vulpera, @Female, 64, 5, 0, 1, 0, 0), -- no ears, two rings (1–1)
(@Vulpera, @Female, 65, 5, 1, 1, 0, 0), -- duplicate
(@Vulpera, @Female, 66, 5, 0, 2, 0, 0), -- big and long, two rings (1–1, clipping through)
(@Vulpera, @Female, 67, 5, 2, 2, 0, 0), -- duplicate
(@Vulpera, @Female, 68, 5, 0, 3, 0, 0), -- short and pointy, two rings (1–1, fit)
(@Vulpera, @Female, 69, 5, 3, 3, 0, 0), -- duplicate
(@Vulpera, @Female, 70, 5, 0, 4, 0, 0), -- big and round, two rings (1–1, fit)
(@Vulpera, @Female, 71, 5, 4, 4, 0, 0), -- duplicate
(@Vulpera, @Female, 72, 5, 0, 5, 0, 0), -- bent forward, two rings (1–1, fit)
(@Vulpera, @Female, 73, 5, 5, 5, 0, 0), -- duplicate
(@Vulpera, @Female, 74, 5, 0, 6, 0, 0), -- tube-curled, two rings (1–1, fit)
(@Vulpera, @Female, 75, 5, 6, 6, 0, 0), -- duplicate
(@Vulpera, @Female, 76, 5, 0, 7, 0, 0), -- sharp and curled, two rings (1–1, barely fit)
(@Vulpera, @Female, 77, 5, 7, 7, 0, 0), -- duplicate
(@Vulpera, @Female, 78, 5, 0, 8, 0, 0), -- one tip missing, two rings (1–1, fit)
(@Vulpera, @Female, 79, 5, 8, 8, 0, 0), -- duplicate
(@Vulpera, @Female, 80, 6, 0, 1, 0, 0), -- no ears, three rings left (
(@Vulpera, @Female, 81, 6, 1, 1, 0, 0), -- duplicate
(@Vulpera, @Female, 82, 6, 0, 2, 0, 0), -- big and long, three rings left (clipping through)
(@Vulpera, @Female, 83, 6, 2, 2, 0, 0), -- duplicate
(@Vulpera, @Female, 84, 6, 0, 3, 0, 0), -- short and pointy, three rings left (float)
(@Vulpera, @Female, 85, 6, 3, 3, 0, 0), -- duplicate
(@Vulpera, @Female, 86, 6, 0, 4, 0, 0), -- big and round, three rings left (clipping through)
(@Vulpera, @Female, 87, 6, 4, 4, 0, 0), -- duplicate
(@Vulpera, @Female, 88, 6, 0, 5, 0, 0), -- bent forward, three rings left (floating)
(@Vulpera, @Female, 89, 6, 5, 5, 0, 0), -- duplicate
(@Vulpera, @Female, 90, 6, 0, 6, 0, 0), -- tube-curled, three rings left (fit)
(@Vulpera, @Female, 91, 6, 6, 6, 0, 0), -- duplicate
(@Vulpera, @Female, 92, 6, 0, 7, 0, 0), -- sharp and curled, three rings left (clipping through)
(@Vulpera, @Female, 93, 6, 7, 7, 0, 0), -- duplicate
(@Vulpera, @Female, 94, 6, 0, 8, 0, 0), -- one tip missing, three rings left (floating)
(@Vulpera, @Female, 95, 6, 8, 8, 0, 0); -- duplicate
