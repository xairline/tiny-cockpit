local POOR_MANS_COCKPIT_LOGGER = {}
function POOR_MANS_COCKPIT_LOGGER.write_log(message)
    logMsg(os.date('%H:%M:%S ') .. '[Poor Man\'s Cockpi]: ' .. message)
end

function POOR_MANS_COCKPIT_LOGGER.dumpTable(tbl, indent)
    if not indent then
        indent = 0
    end
    for k, v in pairs(tbl) do
        formatting = string.rep("  ", indent) .. k .. ": "
        if type(v) == "table" then
            POOR_MANS_COCKPIT_LOGGER.write_log(formatting)
            POOR_MANS_COCKPIT_LOGGER.dumpTable(v, indent + 1)
        else
            POOR_MANS_COCKPIT_LOGGER.write_log(formatting .. tostring(v))
        end
    end
end

return POOR_MANS_COCKPIT_LOGGER
