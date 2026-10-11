-- [F-033] mod-lightforged-draenei: creaturedisplayinfoextra

-- Unspecified versions of each
DELETE FROM `creaturedisplayinfoextra` WHERE `id` IN (@LightforgedDraeneiMaleDisplayExtra, @LightforgedDraeneiFemaleDisplayExtra);
INSERT INTO `creaturedisplayinfoextra` (`id`, `race`, `gender`, `skin_color`, `face_type`, `hair_style`, `hair_color`, `facial_hair`, `helm_id`, `shoulders_id`, `shirt_id`, `chest_id`, `belt_id`, `legs_id`, `boots_id`, `wrists_id`, `gloves_id`, `tabard_id`, `cape_id`, `can_equip`, `texture`) VALUES
(@LightforgedDraeneiMaleDisplayExtra,   @LightforgedDraenei, @Male,   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, ''),
(@LightforgedDraeneiFemaleDisplayExtra, @LightforgedDraenei, @Female, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, '');
