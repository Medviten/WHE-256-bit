#ifndef WHE_RACIAL_RACE_H
#define WHE_RACIAL_RACE_H

#include "DBCStructure.h"
#include "SpellMgr.h"

// The race whose racial skill line teaches `spell` (its SkillLineAbility row in the race's modpak), 0 if none. Scripts
// ported with fixed race ids use it so that the race id in config.sql stays the only one to set.
inline uint8 RaceTeaching(uint32 spell)
{
    SkillLineAbilityMapBounds bounds = sSpellMgr->GetSkillLineAbilityMapBounds(spell);
    for (SkillLineAbilityMap::const_iterator itr = bounds.first; itr != bounds.second; ++itr)
        for (uint32 race = 1; race <= 255; ++race)
            if (itr->second->RaceMask.HasRace(race))
                return uint8(race);
    return 0;
}

#endif
