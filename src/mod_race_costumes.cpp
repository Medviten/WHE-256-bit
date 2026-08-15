#include "ScriptMgr.h"
#include "Player.h"
#include "SpellAuras.h"
#include "DatabaseEnv.h"

#include <cstdint>
#include <map>
#include <tuple>

namespace
{
    // Gender values:
    // 0 = male
    // 1 = female
    //
    // 2 is our custom wildcard meaning "either gender".
    constexpr uint8 COSTUME_GENDER_ANY = 2;

    struct CostumeKey
    {
        uint32 spellId;
        uint8 race;
        uint8 gender;

        bool operator<(CostumeKey const& other) const
        {
            return std::tie(spellId, race, gender) <
                   std::tie(other.spellId, other.race, other.gender);
        }
    };

    // spellId + race + gender -> display ID
    std::map<CostumeKey, uint32> CostumeDatabaseMap;

    uint32 GetCostumeDisplayId(uint32 spellId, uint8 race, uint8 gender)
    {
        // First try exact race + gender.
        CostumeKey exactKey{ spellId, race, gender };

        auto itr = CostumeDatabaseMap.find(exactKey);
        if (itr != CostumeDatabaseMap.end())
            return itr->second;

        // Then try race + wildcard gender.
        CostumeKey anyGenderKey{ spellId, race, COSTUME_GENDER_ANY };

        itr = CostumeDatabaseMap.find(anyGenderKey);
        if (itr != CostumeDatabaseMap.end())
            return itr->second;

        return 0;
    }

    void LoadCostumeDatabase()
    {
        CostumeDatabaseMap.clear();

        LOG_INFO("server.loading", "Loading custom_race_costumes...");

        QueryResult result = WorldDatabase.Query(
            "SELECT trigger_spell_id, race, gender, display_id "
            "FROM custom_race_costumes"
        );

        if (!result)
        {
            LOG_INFO(
                "server.loading",
                ">> Loaded 0 custom race costumes. Table is empty."
            );
            return;
        }

        uint32 count = 0;

        do
        {
            Field* fields = result->Fetch();

            uint32 spellId   = fields[0].Get<uint32>();
            uint8 race       = fields[1].Get<uint8>();
            uint8 gender     = fields[2].Get<uint8>();
            uint32 displayId = fields[3].Get<uint32>();

            CostumeKey key{ spellId, race, gender };

            CostumeDatabaseMap[key] = displayId;
            ++count;

        } while (result->NextRow());

        LOG_INFO(
            "server.loading",
            ">> Loaded {} custom race costume entries.",
            count
        );
    }
}

// ============================================================
// World script
// ============================================================

class CustomCostumeWorldScript : public WorldScript
{
public:
    CustomCostumeWorldScript()
        : WorldScript("CustomCostumeWorldScript")
    {
    }

    void OnStartup() override
    {
        LoadCostumeDatabase();
    }
};

// ============================================================
// Global aura hook
// ============================================================

class CustomCostumeUnitScript : public UnitScript
{
public:
    CustomCostumeUnitScript()
        : UnitScript("CustomCostumeUnitScript")
    {
    }

    void OnAuraApply(Unit* unit, Aura* aura) override
    {
        if (!unit || !aura)
            return;

        // We only care about player characters.
        Player* player = unit->ToPlayer();
        if (!player)
            return;

        SpellInfo const* spellInfo = aura->GetSpellInfo();
        if (!spellInfo)
            return;

        uint32 spellId = spellInfo->Id;

        // Only bother with the lookup if this aura actually has a
        // transform effect - otherwise it's not one of ours.
        bool hasTransformEffect = false;
        for (uint8 i = 0; i < MAX_SPELL_EFFECTS; ++i)
        {
            AuraEffect* effect = aura->GetEffect(i);
            if (effect && effect->GetAuraType() == SPELL_AURA_TRANSFORM)
            {
                hasTransformEffect = true;
                break;
            }
        }

        if (!hasTransformEffect)
            return;

        uint32 displayId = GetCostumeDisplayId(
            spellId,
            player->getRace(),
            player->getGender()
        );

        if (!displayId)
            return;

        // Set the display ID directly. SPELL_AURA_TRANSFORM's own effect
        // "amount" is not what controls the model shown to the client
        // (for this aura type it's used internally as a CC-duration cap),
        // so we can't influence it by changing that value. This hook fires
        // after the aura's default effect handling has already run, so
        // this simply overrides whatever model the core just applied.
        // When the aura is removed, AzerothCore's own transform-removal
        // logic recomputes the player's native model from scratch, so no
        // explicit restore is needed here.
        player->SetDisplayId(displayId);

        LOG_DEBUG(
            "scripts",
            "Custom costume applied: spell={}, race={}, gender={}, display={}",
            spellId,
            (uint32)player->getRace(),
            (uint32)player->getGender(),
            displayId
        );
    }
};

// ============================================================
// Script registration
// ============================================================

void AddSC_mod_race_costumes()
{
    new CustomCostumeWorldScript();
    new CustomCostumeUnitScript();
}