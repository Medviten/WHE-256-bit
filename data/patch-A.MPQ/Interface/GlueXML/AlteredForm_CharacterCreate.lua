--[[
    Altered form (Worgen/Human style) selector for Character Creation, like Cataclysm's.

    Needs the custom client and the alteredFormRaces setting (e.g. SET alteredFormRaces "22=1" in Config.wtf).
    For a race with an altered form, the client shows a second model of that race's altered form with the same
    customization choices, standing behind the character (background model attachment 1). The selector shows both
    forms' portraits in Cataclysm's double frame (Interface\Glues\CharacterCreate\AlternateForm); the form at the
    front has the gold ring, and clicking the other portrait brings it to the front.

    Client functions used: HasAlteredForm(), IsViewingAlteredForm(), SetViewingAlteredForm(bool),
    GetAlteredFormRace() (name, fileString of the altered race).
--]]

local FORM_TEXTURE = "Interface\\Glues\\CharacterCreate\\AlternateForm";
local PORTRAIT_TEXTURE = "Interface\\Glues\\CharacterCreate\\UI-CharacterCreate-RacesRound";

-- Layout in AlternateForm.blp pixels (128x256): the double frame is 80x160 at the top left, the gold ring 62x62 at
-- (0,160), the blue ring 62x62 at (64,160). The selector is drawn 1:1, so these are also frame units.
local FRAME_WIDTH, FRAME_HEIGHT = 80, 160;
local CIRCLE_CENTERS = { { 43, 41 }, { 43, 118 } }; -- top: the race itself, bottom: its altered form
local PORTRAIT_SIZE = 50;
local RING_SIZE = 62;

local selector = CreateFrame("Frame", "CharacterCreateAlteredFormSelector", CharacterCreateFrame);
selector:SetWidth(FRAME_WIDTH);
selector:SetHeight(FRAME_HEIGHT);
selector:SetPoint("BOTTOMLEFT", CharacterCreateConfigurationFrame, "BOTTOMRIGHT", -6, 60);
selector:Hide();

local frameTexture = selector:CreateTexture(nil, "ARTWORK");
frameTexture:SetTexture(FORM_TEXTURE);
frameTexture:SetTexCoord(0, FRAME_WIDTH / 128, 0, FRAME_HEIGHT / 256);
frameTexture:SetAllPoints(selector);

local buttons = {};

for index, center in ipairs(CIRCLE_CENTERS) do
    local altered = (index == 2);
    local button = CreateFrame("Button", "CharacterCreateAlteredFormButton"..index, selector);
    button:SetWidth(RING_SIZE);
    button:SetHeight(RING_SIZE);
    button:SetPoint("CENTER", selector, "TOPLEFT", center[1], -center[2]);
    button:SetFrameLevel(selector:GetFrameLevel() + 1);

    -- Portrait behind the frame's glass
    local portrait = selector:CreateTexture(nil, "BACKGROUND");
    portrait:SetTexture(PORTRAIT_TEXTURE);
    portrait:SetWidth(PORTRAIT_SIZE);
    portrait:SetHeight(PORTRAIT_SIZE);
    portrait:SetPoint("CENTER", button, "CENTER", 0, 0);
    button.portrait = portrait;

    -- Gold ring: this form stands at the front
    local selected = button:CreateTexture(nil, "OVERLAY");
    selected:SetTexture(FORM_TEXTURE);
    selected:SetTexCoord(0, 62 / 128, 160 / 256, 222 / 256);
    selected:SetBlendMode("ADD");
    selected:SetAllPoints(button);
    selected:Hide();
    button.selected = selected;

    -- Blue ring on hover
    local highlight = button:CreateTexture(nil, "HIGHLIGHT");
    highlight:SetTexture(FORM_TEXTURE);
    highlight:SetTexCoord(64 / 128, 126 / 128, 160 / 256, 222 / 256);
    highlight:SetBlendMode("ADD");
    highlight:SetAllPoints(button);

    button:SetScript("OnClick", function(self)
        if ( (IsViewingAlteredForm() and true or false) ~= altered ) then
            PlaySound("gsCharacterCreationClass");
            SetViewingAlteredForm(altered);
        end
    end);

    button:SetScript("OnEnter", function(self)
        if ( self.raceName ) then
            GlueTooltip_SetOwner(self, CharacterCreateTooltip, -3, -5);
            GlueTooltip_SetText(self.raceName, CharacterCreateTooltip);
        end
    end);

    button:SetScript("OnLeave", function(self)
        CharacterCreateTooltip:Hide();
    end);

    buttons[index] = button;
end

local function SetPortrait(button, raceName, fileString)
    local gender = (GetSelectedSex() == SEX_MALE) and "MALE" or "FEMALE";
    local coords = GetSafeRaceIconCoords(fileString, gender);
    button.portrait:SetTexCoord(coords[1], coords[2], coords[3], coords[4]);
    button.raceName = raceName;
end

-- Show the selector only for a race with an altered form; keep portraits and the gold ring current
local driver = CreateFrame("Frame", nil, CharacterCreateFrame);
driver:SetScript("OnUpdate", function(self)
    if ( not HasAlteredForm or not HasAlteredForm() ) then
        selector:Hide();
        return;
    end

    SetPortrait(buttons[1], GetNameForRace());
    SetPortrait(buttons[2], GetAlteredFormRace());

    if ( IsViewingAlteredForm() ) then
        buttons[1].selected:Hide();
        buttons[2].selected:Show();
    else
        buttons[1].selected:Show();
        buttons[2].selected:Hide();
    end

    selector:Show();
end);
