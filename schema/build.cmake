# The functions in this file are called from the CMakeLists.txt file and
# provide the regular workflow for the schema: sanitize the file to
# remove the extensions and install them in the expected directory.

function(install_ovsschema OVSSCHEMA_PATH)
	get_filename_component(ovsschema_name ${OVSSCHEMA_PATH} NAME_WE)
	set(docschema_path "${CMAKE_CURRENT_SOURCE_DIR}/${ovsschema_name}.xml")

	install(FILES ${OVSSCHEMA_PATH} DESTINATION share/openvswitch)

	if(EXISTS ${docschema_path})
		install(FILES ${docschema_path} DESTINATION share/openvswitch)
	endif()
endfunction(install_ovsschema)

# This function will process the given OVS schema file.
function(process_ovsschema OVSSCHEMA_FN)
	install_ovsschema(${OVSSCHEMA_FN})
endfunction(process_ovsschema)

# This function will process the given extended OVS schema file
# to generate the corresponding OVS schema file.
function(generate_ovsschema EXTSCHEMA_FN)
	set(sanitize ${CMAKE_SOURCE_DIR}/schema/sanitize.py)

	# OVS schema
	string(REGEX REPLACE "\\.extschema$" ".ovsschema" ovsschema_fn ${EXTSCHEMA_FN})
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
	install_ovsschema(${ovsschema_path})
endfunction(generate_ovsschema)
