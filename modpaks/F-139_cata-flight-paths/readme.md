# mod-worgoblin-high-elf
## F-139_cata-flight-paths

### Features
- Cataclysm's flight paths in Eastern Kingdoms and Kalimdor, on Open Azeroth's world (whose terrain there is
  Cataclysm's): 118 new taxi nodes, 627 paths to and from them and 122 flight masters standing at them, from the 4.0.6a
  client DBCs and [Project Neltharion](https://github.com/ProjectNeltharion)'s 4.3.4 world database. Among them: Hyjal,
  Uldum, Twilight Highlands, Cataclysm's Silverpine, Westfall, Wetlands, Stranglethorn, Badlands, Desolace, Stonetalon,
  Southern Barrens, Feralas and Azshara, and towns such as Goldshire, Kharanos, Brill, Sen'jin and Razor Hill
- The stock network stays as it is. Nodes stock or Open Azeroth already has (Open Azeroth ported Vashj'ir's and Surwich
  under other ids) are those nodes; a stock node Cataclysm moved a little (Sentinel Hill, Orgrimmar, Gadgetzan, ...)
  keeps its stock spot, and Cataclysm's paths to it start or end there
- Flight masters keep Cataclysm's looks: their displays, NPC bakes and outfit pieces (4.0.6a rows; the bakes and
  shoulder models in WHE-common's `patch-A.MPQ`, from the 4.3.4 client's `art.MPQ`)
- Spawn guids 13950001+, gossip menus and texts 1390000+

### Requirements
- F-010_patch-open-azeroth (the terrain the nodes stand on)
- `patches/core/taxi-mask-size.patch` and a recompile. AzerothCore's taxi masks hold nodes 1-448; Cataclysm's ids go up
  to 683. The patch widens them to 2048 nodes and sends the client as many mask words as its TaxiNodes.dbc needs.
  Without it the new nodes can't be learned, and the client, which sizes the mask by the highest node id, reads past the
  end of the server's. The patch also fixes this for Open Azeroth's own nodes 449-458 (Vashj'ir, Surwich, Keel Harbor,
  Havenswood), which stock AzerothCore writes past the end of its masks for. The 256-bit core has it
- The realm's client DBCs (the taxi rows are DBC rows) and WHE-common's assets

### Known Issues
- Untested in game
- Levels above 80 go down by 10 (Cataclysm's 85 flight masters are 75)
- Cataclysm's quest hubs around the new nodes aren't there, only the flight masters
- Display 33849 is also F-133's (from MoP's data); whichever modpak comes later wins
- 33 icons of the outfit pieces are missing (NPC-only displays, nothing shows them)
- 256-bit only so far (no 32-bit copy, and the 32-bit core lacks the patch)

### Updating
The SQL is generated; change `tools/races/cata_taxi_port.py`, not `dbc/` or `sql/`.
1. `python -I -X utf8 tools/races/cata_taxi_port.py extract <Neltharion world.sql> <extract>` (~3 minutes): the
   flight masters of the new nodes, their templates, equipment, gossip and model info
2. `python -I -X utf8 tools/races/cata_taxi_port.py port <extract> modpaks/F-139_cata-flight-paths`. Both steps take
   `--base-dbc`, a built client DBC folder with every other modpak, whose ids count as taken (default: the test client's
   256-bit realm patch). The port writes the extract's `bakes.txt`, the NPC bakes to copy from the 4.3.4 `art.MPQ` into WHE-common
3. Outfit pieces: `tools/checks/f013_item_assets.py --modpak modpaks/F-139_cata-flight-paths --art <art.MPQ> --copy`,
   then the staged models through wotlkconv and `tools/models/m2_unshare_tracks.py` into WHE-common (as for F-130)
