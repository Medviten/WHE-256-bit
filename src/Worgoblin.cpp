#include "worgoblin_loader.h"
#include "Chat.h"
#include "Player.h"
#include "ScriptMgr.h"
#include "SpellAuraEffects.h"
#include "SpellScript.h"
#include "Config.h"

enum Spells
{
    BEST_DEALS_ANYWHERE = 69044,
};

enum WorgenRiding
{
    SPELL_APPRENTICE_RIDING  = 33388,
    SPELL_JOURNEYMAN_RIDING  = 33391,
    SPELL_RUNNING_WILD       = 87840,

    RUNNING_WILD_LEVEL       = 20,
    RIDING_SKILL_APPRENTICE  = 75,
    RIDING_SKILL_JOURNEYMAN  = 150,
};

class worgoblin : public PlayerScript {

public:
    worgoblin() : PlayerScript("worgoblin") { }

    void OnPlayerLogin(Player* player) override
    {
        if (sConfigMgr->GetOption<bool>("Announce.enable", true))
            ChatHandler(player->GetSession()).SendSysMessage("This server is running the Worgoblin and High Elf modules.");
    }

    void OnPlayerGetReputationPriceDiscount(Player const* player, FactionTemplateEntry const* factionTemplate, float& discount) override
    {
        if (!factionTemplate || !factionTemplate->faction)
            return;

        if (player->HasSpell(BEST_DEALS_ANYWHERE))
            discount *= 0.8;
    }
};

class spell_rocket_barrage : public SpellScript
{
    PrepareSpellScript(spell_rocket_barrage);

    void HandleDamage(SpellEffIndex /*effIndex*/)
    {
        Unit* caster = GetCaster();
        if (!caster)
            return;

        int32 basePoints = 0 + caster->GetLevel() * 2;
        basePoints += caster->SpellBaseDamageBonusDone(GetSpellInfo()->GetSchoolMask()) * 0.429; //BM=0.429 here, don't ask me how.
        basePoints += caster->GetTotalAttackPowerValue(caster->getClass() != CLASS_HUNTER ? BASE_ATTACK : RANGED_ATTACK) * 0.25; // 0.25=BonusCoefficient, hardcoding it here
        SetEffectValue(basePoints);
    }

    void Register() override
    {
        OnEffectLaunchTarget += SpellEffectFn(spell_rocket_barrage::HandleDamage, EFFECT_0, SPELL_EFFECT_SCHOOL_DAMAGE);
    }
};

// Running Wild, as in Cataclysm: a mount on which the Worgen is its own mount. The spell's mounted aura names no
// creature, so instead of mounting nothing (display 0), mount the player's own native display; the patched client
// draws a mount display equal to the native display as the player running on all fours. Running Wild is taken in the
// native form, so it drops the altered (human) form first. Speed follows riding skill, like Cataclysm's
// MountCapability: +60%, or +100% from Journeyman Riding (150 skill). Like any mount, it needs Apprentice Riding
// (75 skill) to cast, since Worgen learn it at level 20 whether or not riding is handed out for free.
class spell_worgen_running_wild : public SpellScript
{
    PrepareSpellScript(spell_worgen_running_wild);

    SpellCastResult CheckRiding()
    {
        Player* player = GetCaster() ? GetCaster()->ToPlayer() : nullptr;
        if (!player || player->GetSkillValue(SKILL_RIDING) >= RIDING_SKILL_APPRENTICE)
            return SPELL_CAST_OK;

        // SPELL_FAILED_MIN_SKILL would show the skill and amount, but the core sends both as 0
        ChatHandler(player->GetSession()).SendNotification("Requires Apprentice Riding");
        return SPELL_FAILED_DONT_REPORT;
    }

    void Register() override
    {
        OnCheckCast += SpellCheckCastFn(spell_worgen_running_wild::CheckRiding);
    }
};

class spell_worgen_running_wild_aura : public AuraScript
{
    PrepareAuraScript(spell_worgen_running_wild_aura);

    void HandleMount(AuraEffect const* /*aurEff*/, AuraEffectHandleModes /*mode*/)
    {
        PreventDefaultAction();

        Unit* target = GetTarget();
        target->RemoveAurasByType(SPELL_AURA_302);
        target->Mount(target->GetNativeDisplayId());
    }

    void CalculateSpeed(AuraEffect const* /*aurEff*/, int32& amount, bool& /*canBeRecalculated*/)
    {
        Player* player = GetUnitOwner() ? GetUnitOwner()->ToPlayer() : nullptr;
        if (!player)
            return;

        amount = player->GetSkillValue(SKILL_RIDING) >= RIDING_SKILL_JOURNEYMAN ? 100 : 60;
    }

    void Register() override
    {
        // Same modes as the default mounted aura handler, so it never runs for this spell
        OnEffectApply += AuraEffectApplyFn(spell_worgen_running_wild_aura::HandleMount, EFFECT_0, SPELL_AURA_MOUNTED, AURA_EFFECT_HANDLE_SEND_FOR_CLIENT_MASK);
        DoEffectCalcAmount += AuraEffectCalcAmountFn(spell_worgen_running_wild_aura::CalculateSpeed, EFFECT_1, SPELL_AURA_MOD_INCREASE_MOUNTED_SPEED);
    }
};

// Teaches every Worgen Running Wild at level 20, as in Cataclysm; its speed comes from riding skill when cast (see
// spell_worgen_running_wild), so there is nothing to sync afterwards. Optionally hands out Apprentice and Journeyman
// Riding for free. Death Knights are left out of that: they already start with 150 riding skill.
// The previous gendered, per-tier version is in legacy/legacy_worgen_running_wild.cpp.
class player_worgen_running_wild : public PlayerScript
{
public:
    player_worgen_running_wild() : PlayerScript("player_worgen_running_wild") { }

    void OnPlayerLogin(Player* player) override { HandleWorgen(player); }
    void OnPlayerLevelChanged(Player* player, uint8 /*oldLevel*/) override { HandleWorgen(player); }

private:
    void HandleWorgen(Player* player)
    {
        if (player->getRace() != RACE_WORGEN)
            return;

        uint8 level = player->GetLevel();

        if (level >= RUNNING_WILD_LEVEL && !player->HasSpell(SPELL_RUNNING_WILD))
            player->learnSpell(SPELL_RUNNING_WILD);

        if (player->getClass() == CLASS_DEATH_KNIGHT)
            return;

        if (sConfigMgr->GetOption<bool>("Worgoblin.RunningWild.FreeApprentice", true)
            && level >= 20 && !player->HasSpell(SPELL_APPRENTICE_RIDING))
            player->learnSpell(SPELL_APPRENTICE_RIDING);

        if (sConfigMgr->GetOption<bool>("Worgoblin.RunningWild.FreeJourneyman", true)
            && level >= 40 && !player->HasSpell(SPELL_JOURNEYMAN_RIDING))
            player->learnSpell(SPELL_JOURNEYMAN_RIDING);
    }
};

void Add_Worgoblin()
{
    new worgoblin();
    RegisterSpellScript(spell_rocket_barrage);
    RegisterSpellAndAuraScriptPair(spell_worgen_running_wild, spell_worgen_running_wild_aura);
    new player_worgen_running_wild();
}