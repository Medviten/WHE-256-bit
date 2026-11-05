# mod-worgoblin-high-elf
## F-027_mod-gilnean

### Features
- Gilnean as the altered form of Worgen (requires F-024), not a playable race
    - Human with Gilnean voice (British accent)
    - Race ID 23, not playable (ChrRaces flag 1), so it takes no race mask bit, achievements, reputation, racials or starting data. Only its HelmetGeosetVisData bit remains, so helmets hide hair and ears as on a human
    - The client's `alteredFormRaces` default `22=23` selects it

### Known Issues
- Sound files may not be working while transformed
- For some reason, Gilnean doesn't show up