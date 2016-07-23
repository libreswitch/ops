# FIXME(jar): Remove openswitch-idl.h and openswitch-dflt.h once
# the code is automatically generated
# Process the header file openswitch.h (automatically generated)
file(GLOB legacy_c_headers
	RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}"
	"${CMAKE_CURRENT_SOURCE_DIR}/*.h"
)

install(FILES ${legacy_c_headers} DESTINATION include)
