# mod-worgoblin-high-elf
## F-138_gnomey-helper

### Features
- From [Project Neltharion](https://github.com/ProjectNeltharion)'s world database: Gnomey <Radioactive's Helper>, a level 85
  gnome vendor at the Merchant Square in Gilneas City who sells convenience items for free: Foror's Crate of Endless Resist
  Gear Storage (a 36-slot bag), food, drink, potions and more
- Not part of Cataclysm: Neltharion added him to their server. F-130 used to carry him; its port
  (`tools/races/cata_gilneas_port.py`, `NELTHARION_NPCS`) now leaves him out, and this modpak holds what it dropped, so
  he is there only if you want him

### Requirements
- None. He stands in Gilneas City (map 0), where F-130's start puts new Worgen, but works without it

### Known Issues
- The items and their displays are F-130's port of the 4.0.6a data, copied as they were (spawn guid 13900001)
- Neltharion's other server NPC, XP Rates, is left out entirely: it needs their `npc_xp_rates` script
