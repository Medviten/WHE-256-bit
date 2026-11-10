/* Ensures that race-restricted items include Mo'arg (as Orc) */
UPDATE `item_template` SET `allowablerace` = `allowablerace` | @MoargMask WHERE `allowablerace` & @OrcMask AND `allowablerace` != -1;
