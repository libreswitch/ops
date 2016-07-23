# This function will process the given extended OVS schema file
# to generate the corresponding OVS schema file.
function(generate_ovsschema EXTSCHEMA_FN)
	set(sanitize ${CMAKE_SOURCE_DIR}/schema/bin/sanitize)

	# OVS schema
	get_filename_component(ovsschema_fn ${EXTSCHEMA_FN} NAME)
	string(REGEX REPLACE "\\.extschema$" ".ovsschema" ovsschema_fn ${ovsschema_fn})
	set(extschema_path ${CMAKE_CURRENT_SOURCE_DIR}/${EXTSCHEMA_FN})
	set(ovsschema_path ${CMAKE_CURRENT_BINARY_DIR}/${ovsschema_fn})
	string(REGEX REPLACE "/" "__" target ${ovsschema_path})

	add_custom_command(
		OUTPUT ${ovsschema_path}
		COMMAND ${sanitize} ${extschema_path} ${ovsschema_path}
		MAIN_DEPENDENCY ${extschema_path}
		DEPENDS ${sanitize}
	)
	add_custom_target(generate-${target} DEPENDS ${ovsschema_path})
	add_dependencies(ovsschema generate-${target})

	# Install
	install(FILES ${extschema_path} DESTINATION share/openvswitch)
	install(FILES ${ovsschema_path} DESTINATION share/openvswitch)
endfunction(generate_ovsschema)

file(GLOB_RECURSE extschema
	RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}"
	"${CMAKE_CURRENT_SOURCE_DIR}/*.extschema"
)

file(GLOB_RECURSE ovsschema
	RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}"
	"${CMAKE_CURRENT_SOURCE_DIR}/*.ovsschema"
)

file(GLOB_RECURSE xml
	RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}"
	"${CMAKE_CURRENT_SOURCE_DIR}/*.xml"
)

foreach(fn ${extschema})
	message(STATUS "Process file: ${fn}")
	generate_ovsschema(${fn})
endforeach(fn)

foreach(fn ${ovsschema})
	message(STATUS "Process file: ${fn}")
	install(FILES ${fn} DESTINATION share/openvswitch)
endforeach(fn)

foreach(fn ${xml})
	message(STATUS "Process file: ${fn}")
	install(FILES ${fn} DESTINATION share/openvswitch)
endforeach(fn)
