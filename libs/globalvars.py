#coding:utf-8
# Author:  Vangelis Tasoulas --<cyberang3l@gmail.com>

#######################################################
#######################################################
#######################################################
#######################################################
### Define you constants with CAPITAL LETTERS here ####
#######################################################
#######################################################
#######################################################
#######################################################

PROGRAM_NAME = 'restart_rtorrent_torrents'
VERSION = '0.0.1'
AUTHOR = 'Vangelis Tasoulas'

#######################################################
#######################################################
#######################################################
#######################################################
############# End of constant definition ##############
#######################################################
#######################################################
#######################################################
#######################################################

##################################
##################################
##################################
##################################
### Define you variables here ####
##################################
##################################
##################################
##################################

xmlrpc_bin = '/usr/bin/xmlrpc'
rtorrent_xmlrpc_url = 'https://localhost/RPC2'
username = 'user'
password = 'pass'
trackers = 'kickass.com'

##################################
##################################
##################################
##################################
### End of variable definition ###
##################################
##################################
##################################
##################################

# Define default constants

# Default config file location where the program should
# look for a configuration file
CONFIG_FILE_LOCATIONS = [".", "/etc/template"]

# The default config filename which might exist
# in CONFIG_FILE_LOCATIONS
DEFAULT_CONFIG_FILENAME = PROGRAM_NAME + ".conf"

# Console logging level (If you change this to DEBUG)
# text sent to STDOUT will be too much
# CRITICAL = 50
#    ERROR = 40
#  WARNING = 30
#     INFO = 20
#    DEBUG = 10
CONSOLE_LOG_LEVEL = 20

class exitCode():
    """
    Define static exit Codes
    """
    SUCCESS = 0
    FAILURE = 1
    INCORRECT_USAGE = 2



# Define AND set default values for the global variables here

# Default file logging level
# CRITICAL = 50
#    ERROR = 40
#  WARNING = 30
#     INFO = 20
#    DEBUG = 10
FileLogLevel = 20

# Default absolute path for the log file
log_file = "{0}/{1}".format(".", PROGRAM_NAME + ".log")

# Conf will be found on runtime (if any)
conf_file = ""

# If your program can run in daemon mode,
# check this variable in runtime if it is true
daemonMode = False
