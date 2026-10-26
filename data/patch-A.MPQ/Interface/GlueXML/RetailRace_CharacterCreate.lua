--[[
    Retail race customization for Character Creation.

    Races mapped to a Retail model by the client's retailRaces setting (e.g. SET retailRaces "52=52,70=70" for
    Dracthyr) carry Retail's full option list instead of the five stock rows: horns, scales, tattoos and so on. While
    such a race is selected, this replaces the stock rows with a scrolling panel of every option that has more than
    one choice, named from the Retail tables. Two Forms races (Dracthyr Dragon/Visage) also get form tabs and a
    "Show both forms" checkbox; Randomize picks among the Retail choices.

    Camera, for every race: mouse wheel zooms towards the face, right-drag pans, a right-click without dragging
    recentres.

    When customizing an existing character (barber-type paid service), the panel starts from the look the server
    saved for it.

    Client functions used (custom client): CycleCharCustomization("EA_<command>", ...) and RetailLoadExisting().
    Without them nothing changes.
--]]

local NUM_ROWS = 10;
local ROW_HEIGHT = 30;
local PANEL_WIDTH = 250;
local PADDING = 10;

-- CycleCharCustomization with a string command. The stock client raises a usage error for it, hence the pcall.
local function Command(...)
    local ok, a, b, c = pcall(CycleCharCustomization, ...);
    if ( ok ) then
        return a, b, c;
    end
end

local function IsRetail()
    return Command("EA_RETAIL") == 1;
end

-- For other GlueXML add-ons (the altered form selector steps aside for the Retail form tabs)
function RetailCharacterCreate_Active()
    return CharacterCreate:IsShown() and IsRetail();
end

local panel = CreateFrame("Frame", "CharacterCreateRetailFrame", CharacterCreateFrame);
panel:SetWidth(PANEL_WIDTH);
panel:SetPoint("BOTTOMLEFT", CharacterCreateConfigurationFrame, "BOTTOMRIGHT", 0, 10);
panel:SetBackdrop({
    bgFile = "Interface\\Tooltips\\UI-Tooltip-Background",
    edgeFile = "Interface\\Tooltips\\UI-Tooltip-Border",
    tile = true, tileSize = 16, edgeSize = 16,
    insets = { left = 4, right = 4, top = 4, bottom = 4 },
});
panel:SetBackdropColor(0.05, 0.05, 0.08, 0.85);
panel:SetBackdropBorderColor(0.75, 0.75, 0.75, 1);
panel:EnableMouseWheel(true);
panel:EnableMouse(true);
panel:Hide();

local title = panel:CreateFontString(nil, "ARTWORK", "GlueFontNormal");
title:SetPoint("TOP", panel, "TOP", 0, -PADDING);
title:SetText("Appearance");

-- Two Forms tabs ("Dragon" / "Visage") and the side-by-side checkbox
local formTabs = {};

for index = 1, 2 do
    local tab = CreateFrame("Button", "CharacterCreateRetailFormTab"..index, panel, "GlueButtonSmallTemplate");
    tab:SetWidth((PANEL_WIDTH - 2 * PADDING) / 2 - 2);
    tab:SetHeight(26);
    tab:SetPoint("TOPLEFT", panel, "TOPLEFT", PADDING + (index - 1) * ((PANEL_WIDTH - 2 * PADDING) / 2 + 2), -PADDING - 20);
    tab:SetScript("OnClick", function(self)
        PlaySound("gsCharacterCreationClass");
        Command("EA_FORM_SET", index - 1);
    end);
    formTabs[index] = tab;
end

local dual = CreateFrame("CheckButton", "CharacterCreateRetailFormDual", panel);
dual:SetWidth(24);
dual:SetHeight(24);
dual:SetPoint("TOPLEFT", formTabs[1], "BOTTOMLEFT", 0, -2);
dual:SetNormalTexture("Interface\\Buttons\\UI-CheckBox-Up");
dual:SetPushedTexture("Interface\\Buttons\\UI-CheckBox-Down");
dual:SetHighlightTexture("Interface\\Buttons\\UI-CheckBox-Highlight", "ADD");
dual:SetCheckedTexture("Interface\\Buttons\\UI-CheckBox-Check");
dual:SetScript("OnClick", function(self)
    PlaySound("gsCharacterCreationClass");
    Command("EA_FORM_DUAL", self:GetChecked() and 1 or 0);
end);

local dualText = dual:CreateFontString(nil, "ARTWORK", "GlueFontNormalSmall");
dualText:SetPoint("LEFT", dual, "RIGHT", 2, 1);
dualText:SetText("Show both forms");

-- Option rows (the stock row template, with our own arrow handlers)
local rows = {};
local rowsTop = CreateFrame("Frame", nil, panel);
rowsTop:SetWidth(1);
rowsTop:SetHeight(1);

local options = {};   -- EA option ids (1-based) of the options with more than one choice
local offset = 0;     -- first visible entry of `options`, 0-based

local function ShowTooltip(row)
    if ( not row.label ) then
        return;
    end
    GlueTooltip_SetOwner(row, CharacterCreateTooltip, -3, -5);
    GlueTooltip_SetText(row.label.."\n"..row.choice.."  ("..row.position..")", CharacterCreateTooltip);
end

local UpdatePanel;

local function Cycle(row, delta)
    if ( row.option ) then
        PlaySound("gsCharacterCreationLook");
        Command("EA_CYCLE", row.option, delta);
        UpdatePanel();
        if ( GetMouseFocus and GetMouseFocus() and GetMouseFocus():GetParent() == row ) then
            ShowTooltip(row);
        end
    end
end

for i = 1, NUM_ROWS do
    local row = CreateFrame("Frame", "CharacterCreateRetailRow"..i, panel, "CharacterCustomizationFrameTemplate");
    row:SetPoint("TOPLEFT", rowsTop, "BOTTOMLEFT", 0, -(i - 1) * ROW_HEIGHT);
    row:EnableMouse(true);

    local text = _G[row:GetName().."Text"];
    text:SetWidth(150);
    text:SetHeight(ROW_HEIGHT);
    row.text = text;

    _G[row:GetName().."LeftButton"]:SetScript("OnClick", function() Cycle(row, -1); end);
    _G[row:GetName().."RightButton"]:SetScript("OnClick", function() Cycle(row, 1); end);

    row:SetScript("OnEnter", ShowTooltip);
    row:SetScript("OnLeave", function() CharacterCreateTooltip:Hide(); end);
    rows[i] = row;
end

-- Scrolling: mouse wheel over the panel, or the arrows beside "1-10 of 45"
local scrollText = panel:CreateFontString(nil, "ARTWORK", "GlueFontNormalSmall");
scrollText:SetPoint("BOTTOM", panel, "BOTTOM", 0, PADDING + 4);

local function CreateScrollButton(name, direction)
    local button = CreateFrame("Button", name, panel);
    button:SetWidth(24);
    button:SetHeight(24);
    local texture = "Interface\\Buttons\\UI-ScrollBar-Scroll"..direction.."Button-";
    button:SetNormalTexture(texture.."Up");
    button:SetPushedTexture(texture.."Down");
    button:SetDisabledTexture(texture.."Disabled");
    button:SetHighlightTexture(texture.."Highlight", "ADD");
    return button;
end

local scrollUp = CreateScrollButton("CharacterCreateRetailScrollUp", "Up");
scrollUp:SetPoint("RIGHT", scrollText, "LEFT", -6, 0);
local scrollDown = CreateScrollButton("CharacterCreateRetailScrollDown", "Down");
scrollDown:SetPoint("LEFT", scrollText, "RIGHT", 6, 0);

local function Scroll(delta)
    local last = math.max(0, #options - NUM_ROWS);
    local wanted = math.min(last, math.max(0, offset + delta));
    if ( wanted ~= offset ) then
        offset = wanted;
        UpdatePanel();
    end
end

scrollUp:SetScript("OnClick", function() Scroll(-NUM_ROWS); end);
scrollDown:SetScript("OnClick", function() Scroll(NUM_ROWS); end);
panel:SetScript("OnMouseWheel", function(self, delta) Scroll(-delta); end);

-- The stock rows this panel stands in for
local stockRowsHidden = false;

local function SetStockRowsShown(shown)
    if ( shown == not stockRowsHidden ) then
        return;
    end
    stockRowsHidden = not shown;
    for i = 1, NUM_CHAR_CUSTOMIZATIONS do
        local row = _G["CharacterCustomizationButtonFrame"..i];
        if ( shown ) then
            row:Show();
        else
            row:Hide();
        end
    end
end

local signature;

function UpdatePanel()
    -- Options worth a row
    options = {};
    local count = Command("EA_COUNT") or 0;
    for option = 1, count do
        local _, choices = Command("EA_GET", option);
        if ( choices and choices > 1 ) then
            options[#options + 1] = option;
        end
    end
    offset = math.min(offset, math.max(0, #options - NUM_ROWS));

    -- Form tabs
    local forms = (Command("EA_FORM_COUNT") or 0) == 2;
    local top = PADDING + 20;
    if ( forms ) then
        local current = Command("EA_FORM_GET") or 0;
        for index, tab in ipairs(formTabs) do
            tab:SetText(Command("EA_FORM_NAME", index - 1) or "");
            if ( current == index - 1 ) then
                tab:LockHighlight();
            else
                tab:UnlockHighlight();
            end
            tab:Show();
        end
        dual:SetChecked(Command("EA_FORM_DUAL", 2) == 1 and 1 or nil);
        dual:Show();
        top = top + 26 + 2 + 24 + 4;
    else
        formTabs[1]:Hide();
        formTabs[2]:Hide();
        dual:Hide();
    end

    rowsTop:SetPoint("TOPLEFT", panel, "TOPLEFT", PADDING, -top);
    local shown = math.min(NUM_ROWS, #options);

    for i, row in ipairs(rows) do
        local option = options[offset + i];
        if ( option ) then
            local value, choices, label = Command("EA_GET", option);
            local name = Command("EA_CHOICE_NAME", option, value);
            row.option = option;
            row.label = label or "";
            row.choice = (name and name ~= "") and name or tostring(value + 1);
            row.position = (value + 1).." / "..choices;
            row.text:SetText(row.label..": "..row.choice);
            row:Show();
        else
            row.option = nil;
            row.label = nil;
            row:Hide();
        end
    end

    -- Scroll footer, only when the options do not all fit
    local footer = 0;
    if ( #options > NUM_ROWS ) then
        scrollText:SetText((offset + 1).."-"..(offset + shown).." of "..#options);
        scrollText:Show();
        scrollUp:Show();
        scrollDown:Show();
        if ( offset > 0 ) then scrollUp:Enable(); else scrollUp:Disable(); end
        if ( offset + NUM_ROWS < #options ) then scrollDown:Enable(); else scrollDown:Disable(); end
        footer = 28;
    else
        scrollText:Hide();
        scrollUp:Hide();
        scrollDown:Hide();
    end

    panel:SetHeight(top + shown * ROW_HEIGHT + footer + PADDING);
end

-- What the panel shows, to rebuild it only when something changed (race, sex, class, form, a choice)
local function Signature()
    local parts = { GetSelectedRace() or 0, GetSelectedSex() or 0, Command("EA_FORM_GET") or 0, Command("EA_FORM_DUAL", 2) or 0 };
    local count = Command("EA_COUNT") or 0;
    for option = 1, count do
        parts[#parts + 1] = Command("EA_GET", option) or -1;
    end
    return table.concat(parts, ":");
end

-- Show the panel only while a Retail race is selected; follow changes made elsewhere (Randomize, race, sex)
local driver = CreateFrame("Frame", nil, CharacterCreateFrame);
driver:SetScript("OnUpdate", function(self, elapsed)
    self.sinceCheck = (self.sinceCheck or 0) + elapsed;
    if ( self.sinceCheck < 0.15 ) then
        return;
    end
    self.sinceCheck = 0;

    if ( IsRetail() ) then
        SetStockRowsShown(false);
        local current = Signature();
        if ( current ~= signature or not panel:IsShown() ) then
            if ( not panel:IsShown() ) then
                offset = 0;
            end
            signature = current;
            UpdatePanel();
        end
        panel:Show();
    else
        signature = nil;
        panel:Hide();
        SetStockRowsShown(true);
    end
end);

-- Randomize among the Retail choices
local originalRandomize = CharacterCreate_Randomize;
function CharacterCreate_Randomize()
    if ( IsRetail() ) then
        PlaySound("gsCharacterCreationLook");
        Command("EA_RANDOM");
    else
        originalRandomize();
    end
end

-- An existing character starts from the look the server saved for it
local originalOnShow = CharacterCreate_OnShow;
function CharacterCreate_OnShow()
    originalOnShow();
    if ( PAID_SERVICE_TYPE and RetailLoadExisting ) then
        RetailLoadExisting();
    end
end

-- Camera: wheel zoom, right-drag pan, right-click recentre
CharacterCreateFrame:EnableMouseWheel(true);
CharacterCreateFrame:SetScript("OnMouseWheel", function(self, delta)
    Command("EA_ZOOM", delta);
end);

local panX, panY, panMoved;

local originalMouseDown = CharacterCreateFrame_OnMouseDown;
function CharacterCreateFrame_OnMouseDown(button)
    if ( button == "RightButton" ) then
        panX, panY = GetCursorPosition();
        panMoved = false;
    end
    originalMouseDown(button);
end

local originalMouseUp = CharacterCreateFrame_OnMouseUp;
function CharacterCreateFrame_OnMouseUp(button)
    if ( button == "RightButton" and panX ) then
        if ( not panMoved ) then
            Command("EA_PAN_RESET");
        end
        panX, panY = nil, nil;
    end
    originalMouseUp(button);
end

local originalFrameUpdate = CharacterCreateFrame_OnUpdate;
function CharacterCreateFrame_OnUpdate()
    if ( panX ) then
        -- Glue cursor positions and GetScreenHeight share units: the client takes screen-height fractions
        local x, y = GetCursorPosition();
        local dx, dy = x - panX, y - panY;
        if ( dx ~= 0 or dy ~= 0 ) then
            panMoved = true;
            Command("EA_PAN", dx / GetScreenHeight(), dy / GetScreenHeight());
            panX, panY = x, y;
        end
    end
    originalFrameUpdate();
end
