import subprocess, os, re, uuid
from datetime import datetime
from commands import *
TIME_OUTPUT = "time_out"
IN = "in.txt"
EXPECTED = 'output.txt'
OUT = "out.txt"
IO = "< %s > %s"%(IN, OUT)
CHAR_LIMIT = 65600
ERROR = "err.txt"
ERR = "2> %s"%(ERROR)
ERR_CODE_FILE = "err_code.txt"
ERR_COMPARE_FILE = "err_compare.txt"
SCRIPT_FILE = 'run.sh'

TIME_COMMAND = "/usr/bin/time -o %s -v timeout"%(TIME_OUTPUT)
SAND = "firejail --private=%s /bin/bash run.sh"

STATS_KEYS = [
    "Maximum resident set size (kbytes)",#: "2248",
    "Elapsed (wall clock) time (h:mm:ss or m:ss)",#: "0:00.34",
    "User time (seconds)",#: "0.34",
    "System time (seconds)",#: "0.00",
    "Exit status",#: "0"
    "Number of characters",
]

def execute(command):
	print "start : ", datetime.now()
	print command
	sp = subprocess.Popen(command, shell=True, close_fds=True, stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
	sp.wait()
	print "end : ", datetime.now()

def execute_with_cwd(command, cwd_dir):
	print "start : ", datetime.now()
	print command
	sp = subprocess.Popen(command, shell=True, close_fds=True, stderr=subprocess.STDOUT, cwd=cwd_dir)
	sp.wait()
	print "returncode : ", sp
	print "end : ", datetime.now()
	return sp

def read_file(path, chars_count = 0):
	file = open(path, "r")
	if chars_count > CHAR_LIMIT:
		output = file.read(CHAR_LIMIT) + '\n.\n.\n.\noutput trimmed'
	else :
		output = file.read()
	file.close()
	return output

def get_err_code(path):
	data = read_file(path)
	print ",,,,,,,,,,,,,,,,,,,,,,,,,,,,",data
	return int(data.split(':')[1])

def write_file(path, content):
	with open(path, "a") as file:
		file.write(content)

def create_folder(path):
	command = "mkdir %s"%(path)
	execute(command)

def get_path(path = None):
	if path is None:
		path = uuid.uuid4()
	else:
		path = "%s_%s"%(path, uuid.uuid4())

	return "/tmp/%s"%(path)

def copy_folder_file(path1, path2):
	command = "cp %s %s"%(path1, path2)
	execute(command)

def delete_folder_files(path):
	command = "rm -r %s"%(path)
	execute(command)

def read_stats(content):
	stats_list = content.split('\n')	
	response={}
	for stat in stats_list:
		key = stat.split(': ')[0]
		key = key.replace('\t','')
		val = stat.split(': ')[-1]
		try:
			try:
				val = int(val)
			except ValueError:
				val = float(val)
		except:
			pass
		if key is not '' and key in STATS_KEYS:
			key = key.replace(' ','_')
			response[key] = val
	return response

