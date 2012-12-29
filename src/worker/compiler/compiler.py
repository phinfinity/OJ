##########################################
#     Compiler Code                      #
# Assumption : All code will be          #
#     compilable. For scripts and other  #
#     non-compiled programs, the         #
#     compler will only be a stub.       #
##########################################

COMPILERS_SCRIPTS_BIN = "../bin/"
CONF_DIR = "../conf/"
LOGGING_DIR = "../../../log/"
COMPILED_EXE_DIR = "../compiled_executables/"


import sys
import json
import logging
import subprocess
import random


def get_compiler_script(language):
    # Open the config file (JSON)
    # Contains [Language] -> Compiler script mapping
    LANGUAGE_CONFIG_FILENAME = "language.json"
    conf_file_loc = CONF_DIR + LANGUAGE_CONFIG_FILENAME
    fin = open(conf_file_loc)

    language_conf_content = fin.read()
    try:
        language_conf_dict = json.loads(language_conf_content)
    except e:
	logging.warning("File open Error\n"+e)
	raise "File IO Error"
        

    try:
        language_script = language_conf_dict[language]['compiler']
	return language_script
    except e:
        logging.warning("Compiler not found \n"+e)
	raise "Compiler not found"

    return "NO-COMPILER"



    



def compiler():
    logging.basicConfig(filename=LOGGING_DIR+"compiler.log",level = logging.DEBUG)
    logging.info("Program started")
    # Program to be evaluated is the 1st argument
    input_program = sys.argv[1]

    # Language is the 2nd argument
    # All the compiling scripts are stored in COMPILERS_SCRIPTS_BIN
    language = sys.argv[2]
    language_compiler = get_compiler_script(language)
    logging.info("Compiling for %s with %s"%(language,language_compiler))
    
    compiled_executable = "exe"+str(random.randrange(1000000))+".out"


    # Execute compilation.
    compiler_path = COMPILERS_SCRIPTS_BIN+language_compiler
    print compiler_path
    ret_val = subprocess.call([compiler_path, input_program,compiled_executable])
    logging.info("Compilation of %s with %s returned %s"%(input_program,language_compiler,str(ret_val)))
    print COMPILED_EXE_DIR+compiled_executable
    return compiled_executable








# boilerplate.    
if __name__=="__main__":
    compiler()
