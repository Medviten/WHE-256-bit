--[[
    Lets character names be up to 47 letters in Character Creation and in the rename box.

    47 matches the custom client and the server, which count UTF-8 bytes (so e.g. é counts as 2). The client checks the
    byte length itself, so this only lifts the edit boxes' letter limit.

    (Replaces TwoNames_CharacterCreate.lua, which also took over the random appearance button to make two-part names.)
--]]

local MAX_NAME_LETTERS = 47;

local frame = CreateFrame("Frame");
frame:SetScript("OnUpdate", function(self)
    if ( CharacterCreateNameEdit and CharacterCreateNameEdit:GetMaxLetters() ~= MAX_NAME_LETTERS ) then
        CharacterCreateNameEdit:SetMaxLetters(MAX_NAME_LETTERS);
    end

    if ( CharacterRenameEditBox and CharacterRenameEditBox:GetMaxLetters() ~= MAX_NAME_LETTERS ) then
        CharacterRenameEditBox:SetMaxLetters(MAX_NAME_LETTERS);
    end
end);
