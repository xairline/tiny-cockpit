local bitwise = require "bit"

POOR_MANS_COCKPIT_LOGGER = dofile(SCRIPT_DIRECTORY .. "/poor-mans-cockpit/logger.lua")
POOR_MANS_COCKPIT_LOGGER.write_log("Loading ... ")


COCKPIT = hid_open(0x1d6b, 0x0104)
if COCKPIT == nil then
    POOR_MANS_COCKPIT_LOGGER.write_log("Failed to open device")
    return
end

-- POOR_MANS_COCKPIT_LOGGER.dumpTable(COCKPIT)

success = hid_set_nonblocking(COCKPIT, 1)
if success < 0 then
    POOR_MANS_COCKPIT_LOGGER.write_log("Failed to set non-blocking mode")
    return
end
local s = "SPD,your_string_here\n"
local spd = dataref_table("toliss_airbus/pfdoutputs/general/ap_speed_value")
local hdg = dataref_table("AirbusFBW/APHDG_Capt")
local alt = dataref_table("toliss_airbus/pfdoutputs/general/ap_alt_target_value")
local vs = dataref_table("sim/cockpit/autopilot/vertical_velocity")

function send_hid()
    jit.off()
    s = "SPD," .. spd[0] .. ",HDG," .. hdg[0] .. ",ALT," .. alt[0] .. ",V/S," .. vs[0] .. "\n"
    hid_write(COCKPIT, 0, string.byte(s, 1, #s))
end

-- local s = "SPD," .. spd[0] .. ",HDG," .. hdg[0] .. ",ALT," .. alt[0] .. ",V/S," .. vs[0] .. "\n"

-- POOR_MANS_COCKPIT_LOGGER.dumpTable(buffer)
-- do_often('send_hid()')
hid_close(COCKPIT)
