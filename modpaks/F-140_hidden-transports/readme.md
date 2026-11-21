# mod-worgoblin-high-elf
## F-140_hidden-transports

### Features
- Transports (zeppelins, ships) that a player sees only once they have done a given quest: a regular service can
  stay out of sight until a scripted first trip has been made. Players who haven't done the quest don't see the
  transport at all, so they can't board it either; it appears as soon as the quest is rewarded. Whoever is on board
  always sees it
- The world table `transport_visibility` (`entry`: the transport's gameobject_template, `quest`: the quest to have
  rewarded), created by `sql/db-world/base/[F-140]_transport_visibility_table.sql`
- No transports are hidden yet: rows come with the services they hide

### Requirements
- `patches/core/transport-visibility.patch` and a recompile. AzerothCore sends every transport on a map to every
  player there, outside the usual visibility and phase checks, so the patch checks the table where transports are
  sent: on entering a map, when a transport arrives from another map, in its updates, and when the quest is rewarded.
  The table empty, the core behaves as stock. The 256-bit core has it

### Considerations
- Keep it after the modpaks whose transports it hides
- Removing the quest (`.quest remove`) leaves the transport in sight until the player changes map
