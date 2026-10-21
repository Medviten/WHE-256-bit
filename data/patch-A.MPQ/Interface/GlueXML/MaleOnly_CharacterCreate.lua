--[[
    Male-only races (Taunka, Tuskarr, Thin Human, ...) in Character Creation.

    A race is male-only when its ChrRaces female display uses the male display's model, i.e. it has no female model.
    The server (WHE core patch) creates characters of such races male whatever gender is sent; this hides the female
    button for them and switches to male when one is selected while female (also when the screen opens on a random
    female of such a race).

    Client function used: IsMaleOnlyRace() for the selected race (custom client). Without it nothing changes.
--]]

local MALE_BUTTON_X = -20; -- CharacterCreate.xml anchors the male button 20 left of centre, the female 20 right

local function UpdateMaleOnly()
    if ( not IsMaleOnlyRace ) then
        return;
    end

    if ( IsMaleOnlyRace() ) then
        CharacterCreateGenderButtonFemale:Hide();
        CharacterCreateGenderButtonMale:SetPoint("TOP", 0, -445);
        if ( GetSelectedSex() == SEX_FEMALE ) then
            -- calls SetCharacterRace again, which finds male selected and stops here
            SetCharacterGender(SEX_MALE);
        end
    else
        CharacterCreateGenderButtonFemale:Show();
        CharacterCreateGenderButtonMale:SetPoint("TOP", MALE_BUTTON_X, -445);
    end
end

-- Race clicks, gender changes and showing the screen all end up in SetCharacterRace
local originalSetCharacterRace = SetCharacterRace;
function SetCharacterRace(id)
    originalSetCharacterRace(id);
    UpdateMaleOnly();
end
