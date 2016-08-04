add_custom_target(database-schema ALL)
add_custom_target(doc)

# Rules for OpenSwitch database format
include("opsschemas.cmake")

# Rules for generating the OpenSwitch documentation
include("documentation.cmake")

# Rules for database schemas using the old format
include("dbschemas.cmake")

# Process the legacy header files
add_subdirectory(legacy)

# Process the Openswitch database schema
add_subdirectory(openswitch)

# Process the DHCP Leases database schema
add_subdirectory(dhcp_leases)
