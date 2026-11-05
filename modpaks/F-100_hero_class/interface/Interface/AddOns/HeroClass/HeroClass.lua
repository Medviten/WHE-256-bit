--[[
    UI for the Hero class (F-100). The stock frames do the work; the patched client's API decides what they see:

    SetHeroTalentClass(classID), GetHeroTalentClass()   which class's three talent trees the talent frame shows
    SetHeroSpellTabPage(page), GetHeroSpellTabPage()    which seven skill lines the spellbook shows, besides General

    Nothing here writes to a stock frame's fields or calls SpellBookFrame_Update, whose tainted writes would block casting
    from the book. SetHeroSpellTabPage makes the client fire SPELLS_CHANGED, so the book refreshes itself.
--]]

-- Stock tables are keyed by class token and have no entry for this one. Other players can be Heroes, so always add it.
RAID_CLASS_COLORS["HERO"] = { r = 0.90, g = 0.80, b = 0.50 };
CLASS_ICON_TCOORDS["HERO"] = { 0.75, 1, 0.75, 1 }; -- an empty cell of UI-Classes-Circles

local _, playerClass = UnitClass("player");
if ( playerClass ~= "HERO" ) then
    return;
end

local CLASSES = {
    { id = 1,  token = "WARRIOR" },
    { id = 2,  token = "PALADIN" },
    { id = 3,  token = "HUNTER" },
    { id = 4,  token = "ROGUE" },
    { id = 5,  token = "PRIEST" },
    { id = 6,  token = "DEATHKNIGHT" },
    { id = 7,  token = "SHAMAN" },
    { id = 8,  token = "MAGE" },
    { id = 9,  token = "WARLOCK" },
    { id = 11, token = "DRUID" },
};

-------------------------------------------------------------------------------
-- Talent frame: a class picker down its left side
-------------------------------------------------------------------------------
local talentButtons;

local function UpdateTalentButtons()
    local selected = GetHeroTalentClass();
    for _, button in ipairs(talentButtons) do
        if ( PlayerTalentFrame.pet ) then
            button:Hide();
        else
            button:Show();
            if ( button.classID == selected ) then
                button:LockHighlight();
            else
                button:UnlockHighlight();
            end
        end
    end
end

local function CreateTalentButtons()
    talentButtons = {};
    for i, class in ipairs(CLASSES) do
        local button = CreateFrame("Button", "HeroClassTalentButton"..i, PlayerTalentFrame);
        button:SetWidth(30);
        button:SetHeight(30);
        button:SetPoint("TOPRIGHT", PlayerTalentFrame, "TOPLEFT", 12, -40 - (i - 1) * 32);
        button.classID = class.id;

        local icon = button:CreateTexture(nil, "ARTWORK");
        icon:SetAllPoints();
        icon:SetTexture("Interface\\TargetingFrame\\UI-Classes-Circles");
        local coords = CLASS_ICON_TCOORDS[class.token];
        icon:SetTexCoord(coords[1], coords[2], coords[3], coords[4]);

        button:SetHighlightTexture("Interface\\Buttons\\ButtonHilight-Square", "ADD");
        button:SetScript("OnClick", function(self)
            SetHeroTalentClass(self.classID);
            PlayerTalentFrame_Refresh();
        end);
        button:SetScript("OnEnter", function(self)
            GameTooltip:SetOwner(self, "ANCHOR_LEFT");
            GameTooltip:SetText(LOCALIZED_CLASS_NAMES_MALE[class.token]);
        end);
        button:SetScript("OnLeave", function() GameTooltip:Hide(); end);

        talentButtons[i] = button;
    end

    hooksecurefunc("PlayerTalentFrame_Refresh", UpdateTalentButtons);
    UpdateTalentButtons();
end

-------------------------------------------------------------------------------
-- Spellbook: page arrows below the tabs. Only shown once there are too many lines for one page.
-------------------------------------------------------------------------------
local prevPage, nextPage, pageText;

local function UpdateSpellPages()
    local page, pages = GetHeroSpellTabPage();
    if ( pages < 2 or SpellBookFrame.bookType ~= BOOKTYPE_SPELL ) then
        prevPage:Hide();
        nextPage:Hide();
        pageText:Hide();
        return;
    end

    prevPage:Show();
    nextPage:Show();
    pageText:Show();
    pageText:SetText(page.."/"..pages);
    if ( page > 1 ) then prevPage:Enable(); else prevPage:Disable(); end
    if ( page < pages ) then nextPage:Enable(); else nextPage:Disable(); end
end

local function CreatePageButton(name, texture)
    local button = CreateFrame("Button", name, SpellBookFrame);
    button:SetWidth(24);
    button:SetHeight(24);
    button:SetNormalTexture("Interface\\Buttons\\UI-SpellbookIcon-"..texture.."-Up");
    button:SetPushedTexture("Interface\\Buttons\\UI-SpellbookIcon-"..texture.."-Down");
    button:SetDisabledTexture("Interface\\Buttons\\UI-SpellbookIcon-"..texture.."-Disabled");
    button:SetHighlightTexture("Interface\\Buttons\\UI-Common-MouseHilight", "ADD");
    return button;
end

local function CreateSpellPages()
    prevPage = CreatePageButton("HeroClassSpellPrevPage", "PrevPage");
    prevPage:SetPoint("TOPLEFT", SpellBookFrame, "TOPRIGHT", -32, -36);
    prevPage:SetScript("OnClick", function()
        SetHeroSpellTabPage(GetHeroSpellTabPage() - 1);
    end);

    nextPage = CreatePageButton("HeroClassSpellNextPage", "NextPage");
    nextPage:SetPoint("LEFT", prevPage, "RIGHT", 18, 0);
    nextPage:SetScript("OnClick", function()
        SetHeroSpellTabPage(GetHeroSpellTabPage() + 1);
    end);

    pageText = SpellBookFrame:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall");
    pageText:SetPoint("LEFT", prevPage, "RIGHT", -2, 0);
    pageText:SetWidth(22);

    hooksecurefunc("SpellBookFrame_Update", UpdateSpellPages);
    UpdateSpellPages();
end

-------------------------------------------------------------------------------
-- Resource bars for the pools the player frame doesn't show, below it
-------------------------------------------------------------------------------
local BARS = {
    { power = 0, color = PowerBarColor["MANA"] },
    { power = 1, color = PowerBarColor["RAGE"] },
    { power = 3, color = PowerBarColor["ENERGY"] },
    { power = 6, color = PowerBarColor["RUNIC_POWER"] },
};

local function CreateBars()
    for _, bar in ipairs(BARS) do
        local frame = CreateFrame("StatusBar", nil, PlayerFrame);
        frame:SetWidth(119);
        frame:SetHeight(9);
        frame:SetStatusBarTexture("Interface\\TargetingFrame\\UI-StatusBar");
        frame:SetStatusBarColor(bar.color.r, bar.color.g, bar.color.b);

        local background = frame:CreateTexture(nil, "BACKGROUND");
        background:SetAllPoints();
        background:SetTexture(0, 0, 0, 0.5);

        bar.frame = frame;
    end
end

local function UpdateBars()
    local shown = 0;
    local displayed = UnitPowerType("player");
    local inCombat = UnitAffectingCombat("player");

    for _, bar in ipairs(BARS) do
        local current, maximum = UnitPower("player", bar.power), UnitPowerMax("player", bar.power);
        local show = bar.power ~= displayed and maximum > 0;
        if ( show ) then
            if ( bar.power == 1 or bar.power == 6 ) then
                -- rage and runic power start empty and decay: only worth a bar while there's some
                show = current > 0;
            elseif ( bar.power == 3 ) then
                -- energy starts full and refills
                show = inCombat or current < maximum;
            end
        end

        if ( show ) then
            bar.frame:ClearAllPoints();
            bar.frame:SetPoint("TOPLEFT", PlayerFrame, "TOPLEFT", 106, -68 - shown * 10);
            bar.frame:SetMinMaxValues(0, maximum);
            bar.frame:SetValue(current);
            bar.frame:Show();
            shown = shown + 1;
        else
            bar.frame:Hide();
        end
    end
end

-------------------------------------------------------------------------------
-- Runes: stock hides them for anyone else, so show them once a Death Knight spell is known
-------------------------------------------------------------------------------
local DEATH_KNIGHT_SPELLS = { 45462, 45477, 45902, 47541 }; -- first ranks of Plague Strike, Icy Touch, Blood Strike, Death Coil

local function UpdateRunes()
    for _, spell in ipairs(DEATH_KNIGHT_SPELLS) do
        if ( IsSpellKnown(spell) ) then
            RuneFrame:Show();
            return;
        end
    end
    RuneFrame:Hide();
end

-------------------------------------------------------------------------------
local elapsed = 0;
local driver = CreateFrame("Frame");
driver:RegisterEvent("PLAYER_LOGIN");
driver:RegisterEvent("ADDON_LOADED");
driver:RegisterEvent("SPELLS_CHANGED");
driver:SetScript("OnEvent", function(self, event, arg1)
    if ( event == "PLAYER_LOGIN" ) then
        CreateSpellPages();
        CreateBars();
        UpdateRunes();
        if ( IsAddOnLoaded("Blizzard_TalentUI") ) then
            CreateTalentButtons();
        end
    elseif ( event == "ADDON_LOADED" and arg1 == "Blizzard_TalentUI" and not talentButtons ) then
        CreateTalentButtons();
    elseif ( event == "SPELLS_CHANGED" ) then
        UpdateRunes();
    end
end);
driver:SetScript("OnUpdate", function(self, delta)
    elapsed = elapsed + delta;
    if ( elapsed >= 0.1 and BARS[1].frame ) then
        elapsed = 0;
        UpdateBars();
    end
end);
