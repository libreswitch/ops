add_custom_target(ovsschema ALL)

# Vendors might provide a customized schema processing process ...
include("vendor-extensions/build.cmake" OPTIONAL
	RESULT_VARIABLE has_vendor_extensions)

# ... and if they don't, fall back to the common one.
if(has_vendor_extensions STREQUAL "NOTFOUND")
	include("build.cmake")
endif()

# Process extschema files

file(GLOB extschema
	RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}"
	"${CMAKE_CURRENT_SOURCE_DIR}/*.extschema"
)

foreach(fn ${extschema})
	message(STATUS "Process file: ${fn}")
	generate_ovsschema(${fn})
endforeach(fn)

# Process ovsschema files

file(GLOB ovsschema
	RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}"
	"${CMAKE_CURRENT_SOURCE_DIR}/*.ovsschema"
)

# If we are building in-source, the .ovsschema file might be a leftover
# from a previous run. Remove generated files from ovsschema list.
foreach(fn ${extschema})
	string(REGEX REPLACE "\\.extschema$" ".ovsschema" fn ${fn})
	list(REMOVE_ITEM ovsschema ${fn})
endforeach(fn)

# Install all the ovsschema files and their documentation if it exists
foreach(fn ${ovsschema})
	message(STATUS "Existing file: ${fn}")
	process_ovsschema(${fn})
endforeach(fn)

# Process header files

file(GLOB idl_headers
	RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}"
	"${CMAKE_CURRENT_SOURCE_DIR}/*.h"
)

install(FILES ${idl_headers} DESTINATION include)
