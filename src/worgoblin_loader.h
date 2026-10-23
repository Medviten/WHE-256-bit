void Add_Worgoblin();
void AddSC_mod_race_costumes();

// AzerothCore calls Add<module folder name, '-' as '_'>Scripts(): the repository's own name (WHE-256-bit)...
void AddWHE_256_bitScripts()
{
    Add_Worgoblin();
    AddSC_mod_race_costumes();
}

// ...or the module's former name, for installs whose folder is still called mod-worgoblin-high-elf
void Addmod_worgoblin_high_elfScripts()
{
    AddWHE_256_bitScripts();
}
