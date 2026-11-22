# mod-worgoblin-high-elf
## F-141_cata-glue-scenes

### Features
- Cataclysm's character creation and select scenes for Gnomes (`UI_Gnome`, Dun Morogh's snow) and Trolls (`UI_Troll`,
  the Echo Isles). Until then they show the Dwarf and Orc scenes, as in 3.3.5a
- Client files only: WHE-common's `modpaks/F-141_cata-glue-scenes/Interface/Glues/Models`, which `deploy-dbc.sh` copies
  into the realm's client patch (`patch-WHE.<realm>.MPQ`) when this modpak is in the manifest. No SQL

### Requirements
- The wowdecomp client from 2026-11-21 on: it shows a Gnome or Troll its own scene only when `UI_<race>.m2` is
  installed (`CCharacterSelection::GetBackgroundRace`); older clients always show the Dwarf and Orc scenes
- The GlueXML in patch-WHE.MPQ has their music and lights (Dwarf's and Orc's)

### Known Issues
- Downloaded from wago.tools (retail's copies of the 4.0 files, FileDataIDs 430171 and 429097) and converted with
  Kalibro's wotlkconv: retail-only shadow batches are dropped
- UI_Gnome's two point lights (diffuse 2.7 and 2.9) lit the character far too brightly in 3.3.5a: scaled by 0.4 with
  `tools/models/m2_scale_lights.py`. Reconvert, and that has to be done again
