# Workflow
1. Set up the [DBCTools](https://github.com/Medviten/DBCTool-256-bit) config file and import clean DBCs (change the database name each time if you want to import different DBCs to compare them with DBC_diff)
2. Make a dump (export) of your squeaky clean DBCs, or make support tables you'll need first
3. Set up the build-dbc config file and point it at the directories containing your SQL files and/or your testworld server
4. Wait for the tool to finish, then copy the exported DBC files to your client patch

# Tools
- `checks/check_customization.py`: checks the customization data of race modpaks (CharSections, CharHairGeosets,
  CharacterFacialHairStyles, CharHairTextures, BarberShopStyle) for missing textures, textures from another race's
  folder, duplicate rows, colour/type gaps and geosets the model lacks. No database needed, but it reads the client
  assets from a [WHE-common](https://github.com/Medviten/WHE-common) checkout (next to this repo by default, or
  `--common PATH` / `$WHE_COMMON`):
  `python3 tools/checks/check_customization.py --stock-dbc /path/to/original/dbc [MODPAK ...]`

- `checks/check_f013_assets.py <paths file> <patch-A.MPQ> <archive.mpq> ...`: lists the client files from a list of paths
  that neither the unpacked patch-A nor the archives have. No MPQ library needed.
- `races/zep_goblin_port.py <zep-goblin-start> <F-013 folder>`: ports Zeppelin-Craft's Goblin starting zone to F-013.

- `races/alpha_race_modpaks.py <package> <stock DBFilesClient> <WHE-common patch-A.MPQ>`: makes F-094..F-097 from the Alpha-Worgen
  package (alpha Worgen and Goblin looks, Cultist and Man'ari races), with its files moved out of the paths they would overwrite.

- `models/m2_alpha_fixes.py <patch-A.MPQ>/Character`: fixes the alpha Worgen models for Two Forms (including copying arm meshes to the female) and removes the alpha Goblin blink, once, after MountSelf (F-094, F-095). `alpha_race_modpaks.py` runs it too.
- `models/m2_retarget_mountself.py <source.m2> <target.m2> [check]`: adds the MountSelf animations of one Worgen model to another with
  a different rig (F-094). `alpha_race_modpaks.py` runs it after copying the models.

- `racemask/word2vars.py`, `racemask/word2.py`: add second race-mask word handling (races 65-128) to config.sql,
  variables.sql and the modpak SQL. Run both with `report`, then `apply`, after adding a race above 64 (see word2.py).
- `racemask/port_32bit.py <modpaks> <WHE-32-bit modpaks> [MODPAK ...]` (then again with `--config`): ports modpaks
  to the [32-bit version](https://github.com/Medviten/WHE-32-bit): drops the second race-mask word, turns the fixed
  race IDs into its auto-incremented ones and keeps what the 32-bit files do differently on purpose (their race ID
  lines, the KEEP_FILES/KEEP_VARS lists, lines only they have). Reports what 32-bit masks cannot hold. Files a modpak
  no longer has are not deleted there
- `racemask/patch_edit.py`: helpers for editing hand-maintained patch files. Inserts or replaces
  `+` lines at exact anchors and recomputes every hunk header, so the patches stay valid (`check_headers()` verifies).

- `models/slimegiant_prep.py`: turns the converted retail SlimeSkeleton model (F-046) into a player model: texture
  types for the character code, the drip as geoset 102, the skeleton's shader. See the F-046 readme for the steps.

- CoA Custom 1.9 races (Ilusixn's "all race files" package; CoA draws them with EsteriaAppearance.dll, WHE keeps the
  stock customization only, see `races/coa_races.py`):
    - `models/coa_race_prep.py <CoA client\Work> <CoA client_root> <WHE-common>/patch-A.MPQ`: copies the race models from the
      extracted CoA MPQs and makes them player models (skin colour texture as the CharSections skin, the DLL's other
      options fixed at their first choice, unused geosets hidden; models over 50 MB get .anim files)
    - `races/coa_race_modpaks.py <built DBFilesClient> <CoA DBFilesClient> <CoA client_root>`: generates F-064..F-071
      and F-057's retail centaur with `new_race_modpaks.py`'s templates
    - `races/coa_racials.py <CoA server sql> <CoA Spell.dbc> <Ascension SpellIcon.dbc> <stock DBFilesClient> [icon folder ...]`:
      adds CoA's racial spells to the race modpaks (commented out where a race already has racials) and their ids to config.sql
    - Kyrian and Venthyr (F-068/F-069) come from Aetheria's newer Kyrian/Venthyr package
      ([aetheria-client](https://github.com/Shotboom12/aetheria-client), [aetheria-server](https://github.com/Shotboom12/aetheria-server)):
      unpack its assets with its `tools/unpack-assets.py --output <folder>`, then pass `--aetheria <aetheria-client> <folder>`
      to `coa_race_prep.py` and `--aetheria <aetheria-client>` to `coa_race_modpaks.py`. Only the files the prepared models
      use are copied (the package also has palettes for the options fixed here)
    - `races/aetheria_racials.py <aetheria-client> <aetheria-server>`: adds Aetheria's Kyrian and Venthyr racials to
      F-068/F-069 at Aetheria's spell ids (their C++ scripts are in `src/`, two core hunks in each modpak's `patches/core/`)
- `races/kalibro_races.py <Kalibros_Races folder> [modpaks] [WHE-common patch-A.MPQ] [more modpaks dirs]`: takes Lightforged
  Draenei, Nightborne and Void Elf (F-033..F-035) from Kalibro's races package: rewrites their customization SQL from its
  DBCs and replaces their WHE-common folders with the model and texture files used
- `models/m2_anim_split.py <model.m2> [output folder]`: moves a 3.3.5 model's animations into per-sequence .anim files,
  as Blizzard's character models keep them (a sequence loads the first time it plays); checks the result against the original
    - `races/dracthyr_modpaks.py <built DBFilesClient>`: generates F-073/F-074 (Dracthyr, races 52/70) with the same templates;
      the wowdecomp-256-bit client shows them with their Retail model. Rerun `coa_racials.py` afterwards for their racials
    - `races/haranir_modpaks.py <built DBFilesClient>`: generates F-098/F-099 (Haranir, races 86/91) the same way; no racials to add. It ends with `races/haranir_native.py <modpaks>`, which points them at the native look baked by `models/haranir_native_prep.py` (needs a `WOWDECOMP_RETAIL_ASSETS` build's probes and the Retail files)
    - `races/skyborne_modpaks.py <built DBFilesClient>`: generates F-103/F-104 (Skyborne, Forever races 95/96) the same way; no racials. It ends with `races/skyborne_native.py`, which writes the native look's rows from Kalibro's races package and copies its files to WHE-common's `custom/skyborne`, then runs `models/skyborne_native_prep.py` (geosets the stock client can select). The wowdecomp-256-bit client shows the Forever look with `retailRaces` `race=forever:<id>` and `Data/Retail/ForeverCasc.ini`
    - `races/retail_voices.py download`, then `races/retail_voices.py write <modpaks>`: retail voices (emotes, error lines, combat sounds) for the races added after Cataclysm (Pandaren, the allied races, Dracthyr, Earthen, Haranir; Skyborne from the Forever build). Reads wago.tools DB2 CSVs and the community listfile from `--data` (default `D:\wow-scratch\retail-vo`), downloads the sound files by FileDataID (paced, resumable), writes each modpak's `soundentries`, `emotestextsound`, `vocaluisounds` and `creaturesounddata` files (the Kin's rows where retail has none), the CreatureSoundData ids in config.sql and the files to WHE-common's `Sound/character`
