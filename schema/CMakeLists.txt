add_custom_target(ovsschema ALL)

# Rules for database schemas using the old format
include("dbschemas.cmake")

# Rules for OpenSwitch database format
include("opsschemas.cmake")

# Process the legacy header files
add_subdirectory(legacy)

# Process the Openswitch database schema
add_subdirectory(openswitch)

# Process the DHCP Leases database schema
add_subdirectory(dhcp_leases)
