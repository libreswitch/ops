# Common definitions
set(metaschema "${CMAKE_CURRENT_SOURCE_DIR}/ops.metaschema.json")

# Pytnon scripts
file(GLOB python_scripts
	${CMAKE_CURRENT_SOURCE_DIR}/bin/*.py
	${CMAKE_CURRENT_SOURCE_DIR}/lib/*.py
)

# Add the local python libraries to the path
set(PYTHONPATH "$ENV{PYTHONPATH}:${CMAKE_SOURCE_DIR}/schema/lib")


# This function will process the master schema file to generate
# the unified schema file, the extended schema file, and the IDL
# constants files for C
function(generate_database_schema)

	set(unified_generator "${CMAKE_SOURCE_DIR}/schema/bin/unified_generator")
	set(schemas_generator "${CMAKE_SOURCE_DIR}/schema/bin/schemas_generator")

	# Get the DB name from the current directory
	string(REGEX MATCH "[^/.]+$" dbname ${CMAKE_CURRENT_SOURCE_DIR})

	message(STATUS "Processing OPS database schemas for: ${dbname}")

	# Handle the special case:
	#   openswitch -> vswitch
	set(output_dbname ${dbname})
	if(dbname STREQUAL "openswitch")
		set(output_dbname "vswitch")
	endif()

	set(master_schema ${CMAKE_CURRENT_SOURCE_DIR}/master.opsschema.json)
	set(unified_schema "${CMAKE_CURRENT_BINARY_DIR}/${dbname}.opsschema")
	set(extschema "${CMAKE_CURRENT_BINARY_DIR}/${output_dbname}.extschema")
	set(ovsschema "${CMAKE_CURRENT_BINARY_DIR}/${output_dbname}.ovsschema")
	set(xml "${CMAKE_CURRENT_BINARY_DIR}/${output_dbname}.xml")
	set(empty_values_header "${CMAKE_CURRENT_BINARY_DIR}/${dbname}_empty_values.h")

	file(GLOB json_schemas
		${CMAKE_CURRENT_SOURCE_DIR}/common/*.json
	)

	add_custom_command(
		OUTPUT ${unified_schema}
		COMMAND PYTHONPATH=${PYTHONPATH} ${unified_generator}
			${master_schema}
			${unified_schema}
		MAIN_DEPENDENCY ${master_schema}
		DEPENDS ${unified_generator} ${json_schemas}
	)

	add_custom_target(generate-${dbname}-dbschema DEPENDS ${unified_schema})
	add_dependencies(ovsschema generate-${dbname}-dbschema)

	add_custom_command(
		OUTPUT ${ovsschema}
			${empty_values_header}
		COMMAND PYTHONPATH=${PYTHONPATH} ${schemas_generator}
			${unified_schema}
			--ovsschema ${ovsschema}
			--metaschema ${metaschema}
			--empty_values_header ${empty_values_header}
			MAIN_DEPENDENCY ${unified_schema}
			DEPENDS ${schemas_generator} ${python_scripts} ${metaschema}
	)

	add_custom_target(generate-${dbname}-extschema
		DEPENDS ${ovsschema}
			${empty_values_header}
	)
	add_dependencies(ovsschema generate-${dbname}-extschema)

	install(FILES ${empty_values_header} DESTINATION include)
	install(FILES ${unified_schema} DESTINATION share/openvswitch)
	install(FILES ${extschema} DESTINATION share/openvswitch OPTIONAL)
	install(FILES ${ovsschema} DESTINATION share/openvswitch)
	install(FILES ${xml} DESTINATION share/openvswitch OPTIONAL)

endfunction(generate_database_schema)

