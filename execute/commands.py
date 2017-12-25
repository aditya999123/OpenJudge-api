SCRIPTS = {
	'COMPILE' : """
				#!/bin/sh
				%s
				ES=$?
				ERR_CODE=%s
				ERR_CODE_FILE=%s
				RCODE=$ES
				if [ $ES != 0 ]
				then
					RCODE=$ERR_CODE
				fi

				echo "\treturn_code:$RCODE" > $ERR_CODE_FILE
				# echo "\tNumber of characters: $(wc -m < %s)" >> %s
			""",

	'RUN' : """
				#!/bin/sh
				%s
				ES=$?
				ERR_CODE=%s
				ERR_CODE_FILE=%s
				RCODE=$ES
				if [ $ES != 0 ] && [ $ES != 124 ]
				then
					RCODE=$ERR_CODE
				fi

				echo "\treturn_code:$RCODE" > $ERR_CODE_FILE
				echo "\tNumber of characters: $(wc -m < %s)" >> %s
			""",

	'COMPARE' : """
				#!/bin/sh
				FILE1=%s
				FILE2=%s
				#ERR_CODE=
				ERR_CODE_FILE=%s
				sed -i '/^$/d' $FILE1
				sed -i '/^$/d' $FILE2
				diff $FILE1 $FILE2
				ES=$?
				#RCODE = $ES
				#if [ $ES != 0 ]
				#then
				#	RCODE=$ERR_CODE
				#fi
				echo "\treturn_code:$ES" > $ERR_CODE_FILE
				"""
}

ERROR_CODE = {
	406 : 'CE',
	506 : 'RTE',
	0 : 'AC',
	1 : 'WA',
	124 : 'TLE'
}

LANG_COMMAND = {
	'C' : {
			'ext' : 'c',
			'time_limit': 5,
			'commands' : [
				{
					'command' : "\'gcc %s %s\'%(code_filename, ERR)",
					'error_code' : 406,
					'script' : 'COMPILE'
				},
				{
					'command' : "\'%s %s ./a.out %s %s\'%(TIME_COMMAND, time_limit, IO, ERR)",
					'error_code' : 506,
					'script' : 'RUN'
				}]
			},
	'C++' : {
			'ext' : 'cpp',
			'time_limit': 5,
			'commands' : [
				{
					'command' : "\'g++ %s %s\'%(code_filename, ERR)",
					'error_code' : 406,
					'script' : 'COMPILE'

				},
				{
					'command' : "\'%s %s ./a.out %s %s\'%(TIME_COMMAND, time_limit, IO, ERR)",
					'error_code' : 506,
					'script' : 'RUN'
				}],
			},
	'PYTHON2' : {
			'ext' : 'py',
			'time_limit': 5,
			'commands' : [
				{
					'command' : "\'python2 -m py_compile %s %s\'%(code_filename, ERR)",
					'error_code' : 406,
					'script' : 'COMPILE'
				},
				{
					'command' : "\'%s %s python2 %s %s %s\'%(TIME_COMMAND, time_limit, code_filename, IO, ERR)",
					'error_code' : 506,
					'script' : 'RUN'
				}],
			},
	'PYTHON3' : {
			'ext' : 'py',
			'time_limit': 5,
			'commands' : [
				{
					'command' : "\'python3 -m py_compile %s %s\'%(code_filename, ERR)",
					'error_code' : 406,
					'script' : 'COMPILE'
				},
				{
					'command' : "\'%s %s python3 %s %s %s\'%(TIME_COMMAND, time_limit, code_filename, IO, ERR)",
					'error_code' : 506,
					'script' : 'RUN'
				}],
			},
}