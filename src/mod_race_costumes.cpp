#include "ScriptMgr.h"
#include "Player.h"
#include "Chat.h"
#include "DatabaseEnv.h"
#include "SpellAuras.h"
#include "SpellMgr.h"

// Structure to hold data map keys
struct CostumeKey {
    uint32 spellId;
    uint8 race;
    uint8 gender;

    bool operator<(const CostumeKey& other) const {
        return std::tie(spellId, race, gender) < std::tie(other.spellId, other.race, other.gender);
    }
};

// Global memory cache for fast lookup without querying the DB during gameplay
std::map<CostumeKey, uint32> CostumeDatabaseMap;

// 1. WorldScript to load database rows on startup or reload
class CustomCostumeWorldScript : public WorldScript
{
public:
    CustomCostumeWorldScript() : WorldScript("CustomCostumeWorldScript") { }

    void OnStartup() override
    {
        LoadCostumeDatabase();
    }

    static void LoadCostumeDatabase()
    {
        CostumeDatabaseMap.clear();
        LOG_INFO("server.loading", "Loading Custom Race Costumes Table...");

        QueryResult result = WorldDatabase.Query("SELECT trigger_spell_id, race, gender, display_id FROM custom_race_costumes");
        if (!result)
        {
            LOG_INFO("server.loading", ">> Loaded 0 custom race costumes. Table is empty.");
            return;
        }

        uint32 count = 0;
        do
        {
            Field* fields = result->Fetch();
            CostumeKey key;
            key.spellId = fields[0].Get<uint32>();
            key.race    = fields[1].Get<uint8>();
            key.gender  = fields[2].Get<uint8>();
            uint32 displayId = fields[3].Get<uint32>();

            CostumeDatabaseMap[key] = displayId;
            count++;
        } while (result->NextRow());

        LOG_INFO("server.loading", ">> Loaded {} custom race costumes.", count);
    }
};

// 2. PlayerScript to intercept the spell cast and apply the dynamic transformation
class CustomCostumePlayerScript : public PlayerScript
{
public:
    CustomCostumePlayerScript() : PlayerScript("CustomCostumePlayerScript") { }

    void OnSpellCast(Player* player, Spell* spell, bool /*skipCheck*/) override
    {
        if (!player || !spell)
            return;

        uint32 castSpellId = spell->GetSpellInfo()->Id;

        // Construct keys to check explicit gender vs global gender (2)
        CostumeKey specificKey = { castSpellId, player->getRace(), player->getGender() };
        CostumeKey genericGenderKey = { castSpellId, player->getRace(), 2 };

        uint32 targetDisplayId = 0;

        if (CostumeDatabaseMap.find(specificKey) != CostumeDatabaseMap.end())
        {
            targetDisplayId = CostumeDatabaseMap[specificKey];
        }
        else if (CostumeDatabaseMap.find(genericGenderKey) != CostumeDatabaseMap.end())
        {
            targetDisplayId = CostumeDatabaseMap[genericGenderKey];
        }

        // If a matching database setup is found, generate the custom transformation aura
        if (targetDisplayId > 0)
        {
            // AuraType 6 = SPELL_AURA_TRANSFORMS
            // We initialize a custom aura logic directly matching how custom Druid forms compute
            // We pass the displayId via the BP0 (BasePoints) parameter
            int32 basePoints = static_cast<int32>(targetDisplayId);
            
            // Cast the spell as a custom aura, embedding our custom display ID into it
            player->CastCustomSpell(player, castSpellId, &basePoints, nullptr, nullptr, true);
        }
    }
};

// Register scripts to AzerothCore loader
void AddSC_mod_race_costumes()
{
    new CustomCostumeWorldScript();
    new CustomCostumePlayerScript();
}