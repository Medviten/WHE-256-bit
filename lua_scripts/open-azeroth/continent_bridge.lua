--[[============================================================================
  Cross-Continent Flight Bridge — Kalimdor <-> Eastern Kingdoms <-> Northrend
  For AzerothCore / Eluna (ALE)

  Assumes:
    - The ocean around Kalimdor, Eastern Kingdoms and Northrend has been
      extended out to (at least) the trigger lines defined below, and flight
      is enabled on all three maps.
    - Kalimdor and Eastern Kingdoms use "equivalent" coordinates: the same
      X (north/south) lines up between the two maps, so crossing between
      them only needs the depth axis (Y) reset to the opposite shore. This
      applies on both sides of the world: Kalimdor's east edge <-> EK's
      west edge (near Northrend), and EK's east edge <-> Kalimdor's west
      edge (the "far side", no Northrend involved).
    - Kalimdor/EK and Northrend overlap on the world map. Every map uses
      the same yard scale, so the overlap is a straight translation
      (offset only, no scaling), derived from the known equivalent points
      at Northrend's SW/SE corners. Because Northrend's west/east edges
      run further north than Kalimdor's/EK's terrain does, that
      translation is clamped to the real northern edge of the target
      continent when necessary. This means a player far enough north on
      Northrend's edge will arrive further south than a pure translation
      would put them, and going back to Northrend from that clamped spot
      won't return them all the way to where they started — a deliberate,
      accepted trade-off rather than leaving a hole with no crossing at
      the northern part of the border.

  Tuning knobs you may want to adjust after testing in-game:
    - CHECK_INTERVAL: how often (ms) players are scanned for a crossing.
    - BUFFER: how far inside the new map a player lands on the direct
      Kalimdor<->EK crossing, so they don't instantly re-trigger the
      reverse check.
    - Z (altitude) is currently carried over unchanged on every jump. If
      the three continents' sea levels don't line up in your setup, add
      a per-border Z offset the same way the X/Y offsets are handled.

  Pandaria (F-133, map 870) and the Wandering Isle (F-134, map 860):
    - Pandaria lies south of the gap between Kalimdor and the Eastern
      Kingdoms. Its northern edge leads to Kalimdor's southern edge (west
      of PAN_SPLIT_Y) or EK's (east of it). The split line stands for the
      Kalimdor-east/EK-west crossing, so Y is a straight translation that
      lines PAN_SPLIT_Y up with KAL_EAST_Y and EK_WEST_Y, clamped to the
      maps the same way the Northrend crossing is.
    - The Wandering Isle swims around Pandaria. Its pose (centre on
      Pandaria's map plus heading) is a pure function of os.time(): one
      lap of an ellipse every WI_PERIOD seconds, heading along the path.
      Nothing is stored, so every scan and every restart agrees on it.
      Coming within WI_ENTER_R of that centre on Pandaria lands the player
      on map 860; leaving WI_EXIT_R of the island's own centre on map 860
      lands them back in Pandaria's ocean. Both ways go through the same
      rotation (isle front = its heading), so position and facing turn
      with the isle and turning around takes you back where you came from.
      WI_EXIT_R > WI_ENTER_R keeps arrivals from bouncing straight back.
    - Sea level is 0 on both maps, so Z carries over here too.
    - Like the other continents, this assumes open sea out to the trigger
      lines and the orbit. Pandaria's own tiles only reach ~500-2000 yards
      past its coast, so without ocean filler tiles on map 870 the outer
      orbit and the northern edge are flown over empty space.
============================================================================]]

local MAP_EK        = 0
local MAP_KALIMDOR  = 1
local MAP_NORTHREND = 571
local MAP_PANDARIA  = 870
local MAP_WI        = 860

local CHECK_INTERVAL = 500  -- ms between scans
local BUFFER         = 75   -- yards of slack given on arrival so the player
                             -- doesn't instantly re-trigger the reverse check

-- ---------------------------------------------------------------------------
-- Trigger lines ("threshold points" from the map planning)
-- ---------------------------------------------------------------------------

-- Kalimdor's eastern ocean edge (Y decreases going east)
local KAL_EAST_Y       = -9773
local KAL_EAST_SPLIT_X = 11037   -- south of this -> EK, north of this -> Northrend

-- Eastern Kingdoms' western ocean edge (Y increases going west)
local EK_WEST_Y        = 12615
local EK_WEST_SPLIT_X  = 5661    -- south of this -> Kalimdor, north of this -> Northrend

-- Northrend's western edge (borders Kalimdor only, Y increases going west)
local NR_WEST_Y = 10546

-- Northrend's eastern edge (borders EK only, Y decreases going east)
local NR_EAST_Y = -8036

-- The "far side" crossing: EK's eastern edge <-> Kalimdor's western edge.
-- No Northrend overlap here, so this is a straight X/Z/O-preserving jump
-- with Y reset, same as the direct Kalimdor<->EK crossing above. The
-- trigger line sits slightly closer to the true edge than the arrival
-- point on the other side, so a player can't ping-pong back and forth.
local EK_EAST_Y  = -16994   -- crossing further east (lower Y) than this -> Kalimdor
local KAL_WEST_Y = 16994    -- crossing further west (higher Y) than this -> EK

-- Southern edges of Kalimdor / EK -> Pandaria, and Pandaria's northern edge
-- back. All three maps are taken to run to the full tile grid (+-17066).
local KAL_SOUTH_X = -16994
local EK_SOUTH_X  = -16994
local PAN_NORTH_X = 16994
local PAN_SPLIT_Y = 0       -- Pandaria west of this -> Kalimdor, east -> EK
local PAN_MIN_Y   = -16944  -- clamp for arrivals on Pandaria's northern edge
local PAN_MAX_Y   = 16944

-- ---------------------------------------------------------------------------
-- Wandering Isle orbit (from the server .map tiles: Pandaria's land spans
-- X -3200..6933, Y -6400..6933; the isle's land X 0..1600, Y 2667..4800 on a
-- map whose sea reaches X -2133..3200, Y 1067..6400)
-- ---------------------------------------------------------------------------

local PAN_CX, PAN_CY = 1867, 267    -- centre of Pandaria's land
local WI_ORBIT_A     = 9500         -- ellipse half-axis along X (north/south)
local WI_ORBIT_B     = 11000        -- ellipse half-axis along Y (west/east)
local WI_PERIOD      = 24 * 3600    -- seconds per lap
local WI_CX, WI_CY   = 800, 3733    -- centre of the isle on map 860
local WI_FRONT       = 0            -- map-860 orientation of the isle's front (its +X)
local WI_ENTER_R     = 2100         -- on Pandaria: this close to the isle -> map 860
local WI_EXIT_R      = 2200         -- on map 860: this far from its centre -> Pandaria

-- ---------------------------------------------------------------------------
-- Northrend <-> Kalimdor / EK translation (offset only, same yard scale)
-- Derived from the known equivalent corners:
--   Northrend SW (-2932, 10932)  ==  Kalimdor (7596, -8980)
--   Northrend SE (-2932, -9332)  ==  EK       (4188, 11111)
-- ---------------------------------------------------------------------------

local NR_KAL_DX = 7596  - (-2932)   --  10528
local NR_KAL_DY = -8980 - 10932     -- -19912

local NR_EK_DX  = 4188  - (-2932)   --   7120
local NR_EK_DY  = 11111 - (-9332)   --  20443

-- Northrend reaches further north than Kalimdor/EK do. A straight
-- translation can therefore overshoot the destination continent's real
-- northern edge - when that happens we pull the arrival point back down
-- to just south of the edge instead of dropping the player into the void.
local SAFETY_MARGIN = 50            -- stay this far shy of the mapped terrain edge
local KAL_MAX_X = 16994 - SAFETY_MARGIN   -- Kalimdor's NE (ocean) corner
local EK_MAX_X  = 16985 - SAFETY_MARGIN   -- EK's NW (ocean) corner

-- ---------------------------------------------------------------------------
-- Coordinate conversions
-- ---------------------------------------------------------------------------

local function clampMaxX(x, maxX)
    if x > maxX then
        return maxX
    end
    return x
end

local function northrendXToKalimdor(x)
    return clampMaxX(x + NR_KAL_DX, KAL_MAX_X)
end

local function kalimdorXToNorthrend(x)
    return x - NR_KAL_DX
end

local function northrendXToEK(x)
    return clampMaxX(x + NR_EK_DX, EK_MAX_X)
end

local function ekXToNorthrend(x)
    return x - NR_EK_DX
end

local function clamp(v, lo, hi)
    if v < lo then
        return lo
    elseif v > hi then
        return hi
    end
    return v
end

local function jump(player, mapId, x, y, z, o)
    player:Teleport(mapId, x, y, z, o)
end

-- ---------------------------------------------------------------------------
-- Wandering Isle pose
-- ---------------------------------------------------------------------------

local atan2 = math.atan2 or math.atan  -- Lua 5.1/LuaJIT vs 5.3+
local TWO_PI = 2 * math.pi

-- Centre of the isle on Pandaria's map and the rotation from map-860 axes to
-- map-870 axes (its heading minus WI_FRONT).
local function wiPose()
    local phi = TWO_PI * (os.time() % WI_PERIOD) / WI_PERIOD
    local cx = PAN_CX + WI_ORBIT_A * math.cos(phi)
    local cy = PAN_CY + WI_ORBIT_B * math.sin(phi)
    local heading = atan2(WI_ORBIT_B * math.cos(phi), -WI_ORBIT_A * math.sin(phi))
    return cx, cy, heading - WI_FRONT
end

local function rotate(x, y, a)
    local c, s = math.cos(a), math.sin(a)
    return x * c - y * s, x * s + y * c
end

local function wrapO(o)
    return o % TWO_PI
end

-- ---------------------------------------------------------------------------
-- Border checks
-- ---------------------------------------------------------------------------

local function checkKalimdor(player, x, y, z, o)
    if y <= KAL_EAST_Y then
        -- Eastern edge.
        if x < KAL_EAST_SPLIT_X then
            -- Southern stretch of the edge -> Eastern Kingdoms.
            -- Latitude (X), altitude (Z) and orientation carry straight over.
            jump(player, MAP_EK, x, EK_WEST_Y - BUFFER, z, o)
        else
            -- Northern stretch of the edge -> Northrend.
            local nx = kalimdorXToNorthrend(x)
            local ny = y - NR_KAL_DY
            jump(player, MAP_NORTHREND, nx, ny, z, o)
        end
    elseif y >= KAL_WEST_Y then
        -- Western edge -> Eastern Kingdoms (the "far side" crossing).
        jump(player, MAP_EK, x, EK_EAST_Y + BUFFER, z, o)
    elseif x <= KAL_SOUTH_X then
        -- Southern edge -> Pandaria's northern edge, west of the split.
        local py = clamp(PAN_SPLIT_Y + (y - KAL_EAST_Y), PAN_SPLIT_Y, PAN_MAX_Y)
        jump(player, MAP_PANDARIA, PAN_NORTH_X - BUFFER, py, z, o)
    end
end

local function checkEasternKingdoms(player, x, y, z, o)
    if y >= EK_WEST_Y then
        -- Western edge.
        if x < EK_WEST_SPLIT_X then
            -- Southern stretch of the edge -> Kalimdor.
            jump(player, MAP_KALIMDOR, x, KAL_EAST_Y + BUFFER, z, o)
        else
            -- Northern stretch of the edge -> Northrend.
            local nx = ekXToNorthrend(x)
            local ny = y - NR_EK_DY
            jump(player, MAP_NORTHREND, nx, ny, z, o)
        end
    elseif y <= EK_EAST_Y then
        -- Eastern edge -> Kalimdor (the "far side" crossing).
        jump(player, MAP_KALIMDOR, x, KAL_WEST_Y - BUFFER, z, o)
    elseif x <= EK_SOUTH_X then
        -- Southern edge -> Pandaria's northern edge, east of the split.
        -- y < EK_WEST_Y here, so this always lands east of the split.
        local py = clamp(PAN_SPLIT_Y + (y - EK_WEST_Y), PAN_MIN_Y, PAN_SPLIT_Y)
        jump(player, MAP_PANDARIA, PAN_NORTH_X - BUFFER, py, z, o)
    end
end

local function checkNorthrend(player, x, y, z, o)
    if y > NR_WEST_Y then
        -- West edge -> Kalimdor only.
        local kx = northrendXToKalimdor(x)
        local ky = y + NR_KAL_DY
        jump(player, MAP_KALIMDOR, kx, ky, z, o)
    elseif y < NR_EAST_Y then
        -- East edge -> Eastern Kingdoms only.
        local ex = northrendXToEK(x)
        local ey = y + NR_EK_DY
        jump(player, MAP_EK, ex, ey, z, o)
    end
end

local function checkPandaria(player, x, y, z, o)
    if x >= PAN_NORTH_X then
        -- Northern edge -> Kalimdor's or EK's southern edge. The BUFFER clamps
        -- keep arrivals off Kalimdor's east / EK's west trigger lines.
        if y >= PAN_SPLIT_Y then
            local ky = math.max(KAL_EAST_Y + (y - PAN_SPLIT_Y), KAL_EAST_Y + BUFFER)
            jump(player, MAP_KALIMDOR, KAL_SOUTH_X + BUFFER, ky, z, o)
        else
            local ey = math.min(EK_WEST_Y + (y - PAN_SPLIT_Y), EK_WEST_Y - BUFFER)
            jump(player, MAP_EK, EK_SOUTH_X + BUFFER, ey, z, o)
        end
        return
    end

    local cx, cy, a = wiPose()
    local dx, dy = x - cx, y - cy
    if dx * dx + dy * dy <= WI_ENTER_R * WI_ENTER_R then
        -- Swam into the isle: same offset from its centre, in its own axes.
        local lx, ly = rotate(dx, dy, -a)
        jump(player, MAP_WI, WI_CX + lx, WI_CY + ly, z, wrapO(o - a))
    end
end

local function checkWanderingIsle(player, x, y, z, o)
    local lx, ly = x - WI_CX, y - WI_CY
    if lx * lx + ly * ly > WI_EXIT_R * WI_EXIT_R then
        -- Left the isle's waters -> Pandaria's ocean, wherever the isle is now.
        local cx, cy, a = wiPose()
        local dx, dy = rotate(lx, ly, a)
        jump(player, MAP_PANDARIA, cx + dx, cy + dy, z, wrapO(o + a))
    end
end

-- ---------------------------------------------------------------------------
-- Main scan loop
-- ---------------------------------------------------------------------------

local function ScanForBorderCrossings()
    local players = GetPlayersInWorld()

    for _, player in ipairs(players) do
        if player and player:IsInWorld() then
            local mapId = player:GetMapId()

            if mapId == MAP_KALIMDOR then
                checkKalimdor(player, player:GetX(), player:GetY(), player:GetZ(), player:GetO())
            elseif mapId == MAP_EK then
                checkEasternKingdoms(player, player:GetX(), player:GetY(), player:GetZ(), player:GetO())
            elseif mapId == MAP_NORTHREND then
                checkNorthrend(player, player:GetX(), player:GetY(), player:GetZ(), player:GetO())
            elseif mapId == MAP_PANDARIA then
                checkPandaria(player, player:GetX(), player:GetY(), player:GetZ(), player:GetO())
            elseif mapId == MAP_WI then
                checkWanderingIsle(player, player:GetX(), player:GetY(), player:GetZ(), player:GetO())
            end
        end
    end

    CreateLuaEvent(ScanForBorderCrossings, CHECK_INTERVAL, 1)
end

CreateLuaEvent(ScanForBorderCrossings, CHECK_INTERVAL, 1)