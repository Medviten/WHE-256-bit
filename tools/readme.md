# Workflow
1. Set up the DBCTools config file and import clean DBCs (change the database name each time if you want to import different DBCs to compare them with DBC_diff)
2. Make a dump (export) of your squeaky clean DBCs, or make support tables you'll need first
3. Set up the build-dbc config file and point it at the directories containing your SQL files and/or your testworld server
4. Wait for the tool to finish, then copy the exported DBC files to your client patch

# Tools
- `checks/check_customization.py`: checks the customization data of race modpaks (CharSections, CharHairGeosets,
  CharacterFacialHairStyles, CharHairTextures, BarberShopStyle) for missing textures, textures from another race's
  folder, duplicate rows, colour/type gaps and geosets the model lacks. No database needed:
  `python3 tools/checks/check_customization.py --stock-dbc /path/to/original/dbc [MODPAK ...]`

- `racemask/word2vars.py`, `racemask/word2.py`: add second race-mask word handling (races 65-128) to config.sql,
  variables.sql and the modpak SQL. Run both with `report`, then `apply`, after adding a race above 64 (see word2.py).
- `racemask/patch_edit.py`: helpers for editing the hand-maintained integration/*.patch files. Inserts or replaces
  `+` lines at exact anchors and recomputes every hunk header, so the patches stay valid (`check_headers()` verifies).

- `models/slimegiant_prep.py`: turns the converted retail SlimeSkeleton model (F-046) into a player model: texture
  types for the character code, the drip as geoset 102, the skeleton's shader. See the F-046 readme for the steps.
