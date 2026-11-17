--[[
    The Hero class (F-100) in Character Creation: an eleventh class button and the class's texts.
    The Hero's button goes right above the Warrior's, and the other classes keep the stock slots. Buttons follow
    ChrClasses.dbc's order, so the Hero (class 10) would otherwise take the tenth slot and push the Druid out.
    It has no slot in the class icon atlas, so its button and big icon use an ordinary icon instead.
--]]

local HERO_ICON = "Interface\\Icons\\INV_Misc_Book_09";

MAX_CLASSES_PER_RACE = 11;
CLASS_ICON_TCOORDS["HERO"] = {0, 1, 0, 1};

CLASS_HERO = "Heroes follow no single path. They can learn from any class trainer and spend their talents in any class's trees, so a Hero is whatever its abilities make it.";
CLASS_HERO_FEMALE = CLASS_HERO;
CLASS_INFO_HERO0 = "- Role: Tank, Healer, Damage";
CLASS_INFO_HERO1 = "- Learns from every class's trainers";
CLASS_INFO_HERO2 = "- Spends talent points in every class's trees";
CLASS_INFO_HERO3 = "- Has mana, rage, energy and runic power";
HERO_DISABLED = "Hero\nYou must choose a different race to be this class.";

local button = CreateFrame("CheckButton", "CharacterCreateClassButton11", CharacterCreateClassButton10:GetParent(), "CharacterCreateClassButtonTemplate");
button:SetID(11);
button:Hide();

-- The stock slots: where CharacterCreate.xml puts the ten class buttons. An anchor to another class button names
-- the slot that button stands in.
local slots = {};
local slotOf = {};
for i=1, 10 do
    slotOf[_G["CharacterCreateClassButton"..i]] = i;
end
for i=1, 10 do
    local point, relativeTo, relativePoint, x, y = _G["CharacterCreateClassButton"..i]:GetPoint(1);
    slots[i] = {point, slotOf[relativeTo] or relativeTo, relativePoint, x, y};
end

local normalTexture = CharacterCreateClassButton1NormalTexture:GetTexture();
local pushedTexture = CharacterCreateClassButton1PushedTexture:GetTexture();
local classIcon = CharacterCreateClassIcon:GetTexture();

local originalEnumerateClasses = CharacterCreateEnumerateClasses;
function CharacterCreateEnumerateClasses(...)
    originalEnumerateClasses(...);

    local index = 1;
    local heroButton;
    local slotButtons = {};
    for i=1, select("#", ...), 3 do
        local classButton = _G["CharacterCreateClassButton"..index];
        local hero = strupper(select(i+1, ...) or "") == "HERO";
        _G["CharacterCreateClassButton"..index.."NormalTexture"]:SetTexture(hero and HERO_ICON or normalTexture);
        _G["CharacterCreateClassButton"..index.."PushedTexture"]:SetTexture(hero and HERO_ICON or pushedTexture);
        if ( hero ) then
            heroButton = classButton;
        elseif ( #slotButtons < #slots ) then
            table.insert(slotButtons, classButton);
        end
        index = index + 1;
    end

    -- Clear every anchor first, so no button is left anchored to one that is about to be anchored to it.
    for i=1, MAX_CLASSES_PER_RACE do
        _G["CharacterCreateClassButton"..i]:ClearAllPoints();
    end
    for slot, slotButton in ipairs(slotButtons) do
        local anchor = slots[slot];
        local relativeTo = anchor[2];
        if ( type(relativeTo) == "number" ) then
            relativeTo = slotButtons[relativeTo];
        end
        slotButton:SetPoint(anchor[1], relativeTo, anchor[3], anchor[4], anchor[5]);
    end
    if ( heroButton ) then
        heroButton:SetPoint("BOTTOM", slotButtons[1] or CharacterCreateClassButton1:GetParent(), slotButtons[1] and "TOP" or "BOTTOM", 0, 6);
    end
end

local originalSetCharacterClass = SetCharacterClass;
function SetCharacterClass(id)
    originalSetCharacterClass(id);

    local _, classFileName = GetSelectedClass();
    CharacterCreateClassIcon:SetTexture(classFileName == "HERO" and HERO_ICON or classIcon);
end
