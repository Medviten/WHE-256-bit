#include "ScriptMgr.h"
#include "Player.h"
#include "SpellAuras.h"
#include "SpellAuraEffects.h"
#include "SpellScript.h"

#include <cstdint>
#include <map>

namespace
{
    struct GenderedDisplay
    {
        uint32 maleDisplayId;
        uint32 femaleDisplayId;
    };

    // To add a new costume: add a line below and recompile. Key is the
    // trigger spell ID cast by whatever item/NPC/command grants the
    // transform aura. No database table involved.
    std::map<uint32, GenderedDisplay> const CostumeSpells =
    {
        // spellId, { maleDisplayId, femaleDisplayId }
        { 68994,    { 94135,          94136          } }, // Gilnean disguise
        { 110020,   { 20585,          20584          } }, // Tauren disguise
    };

    uint32 GetCostumeDisplayId(uint32 spellId, uint8 gender)
    {
        auto itr = CostumeSpells.find(spellId);
        if (itr == CostumeSpells.end())
            return 0;

        return (gender == GENDER_FEMALE) ? itr->second.femaleDisplayId : itr->second.maleDisplayId;
    }
}

// ============================================================
// Aura script - applies the correct gendered model on the transform
// aura's initial apply AND every later reapply (recast/refresh/
// stack). AfterEffectApply runs once the built-in SPELL_AURA_TRANSFORM
// handling for this effect has already completed, so our override
// reliably lands last instead of risking being overwritten by it -
// which is what OnEffectApply (used in an earlier version of this
// file) was vulnerable to.
// ============================================================

class spell_costume_override : public AuraScript
{
    PrepareAuraScript(spell_costume_override);

    void HandleApply(AuraEffect const* /*aurEff*/, AuraEffectHandleModes /*mode*/)
    {
        Unit* target = GetTarget();
        if (!target)
            return;

        Player* player = target->ToPlayer();
        if (!player)
            return;

        uint32 displayId = GetCostumeDisplayId(GetId(), player->getGender());
        if (!displayId)
            return;

        player->SetDisplayId(displayId);

        LOG_DEBUG(
            "scripts",
            "Custom costume applied: spell={}, gender={}, display={}",
            GetId(),
            (uint32)player->getGender(),
            displayId
        );
    }

    void Register() override
    {
        AfterEffectApply += AuraEffectApplyFn(
            spell_costume_override::HandleApply,
            EFFECT_ALL,
            SPELL_AURA_TRANSFORM,
            AURA_EFFECT_HANDLE_REAL_OR_REAPPLY_MASK
        );
    }
};

// ============================================================
// Script registration
// ============================================================

void AddSC_mod_race_costumes()
{
    RegisterSpellScript(spell_costume_override);
}