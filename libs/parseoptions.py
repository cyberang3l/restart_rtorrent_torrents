#coding:utf-8
# Author:  Vangelis Tasoulas --<cyberang3l@gmail.com>

import os
import sys
import logging
import ConfigParser
import argparse
import traceback
from libs import globalvars

LOGGER = logging.getLogger('default.' + __name__)

_quiet = False

def parse_all_conf():

    # Parse the command line options
    options = _command_Line_Options()

    # Configure logging
    _set_logging(options)

    # Read configuration from file
    _read_config_file(options)

    # Validate user input and perform any necessary actions
    # to the given command line options
    # Command line options may override certain configuration read from the conf file
    _validate_command_Line_Options(options)



def _command_Line_Options():
    """
    Define the accepted command line arguments in this function

    Read the documentation of argparse for more advanced command line
    argument parsing examples
    http://docs.python.org/2/library/argparse.html
    """

    ########################################
    ########################################
    ########################################
    ########################################
    #### Add user defined options here #####
    ########################################
    ########################################
    ########################################
    ########################################
    parser = argparse.ArgumentParser(version=globalvars.VERSION,
                                     description="Script to restart inactive torrents in rtorrent")

    ########################################
    ########################################
    ########################################
    ########################################
    #### End user defined options here #####
    ########################################
    ########################################
    ########################################
    ########################################


    parser.add_argument("-d", "--daemon",
                        action="store_true",
                        default=globalvars.daemonMode,
                        dest="isDaemon",
                        help="run in daemon mode")
    parser.add_argument("-c", "--conffile",
                        action="store",
                        default=globalvars.conf_file,
                        dest="conffile",
                        metavar="conf_file",
                        help="conf_file where the configuration will be read from (Default: will search for file '" +
                        globalvars.DEFAULT_CONFIG_FILENAME +
                        "' in the known predefined locations")

    ### Add logging options in a different options group
    loggingGroupOpts = parser.add_argument_group('Logging Options', 'List of optional logging options')
    loggingGroupOpts.add_argument("-q", "--quiet",
                                  action="store_true",
                                  default=_quiet,
                                  dest="isQuiet",
                                  help="Disable logging in the console but still keep logs in a file. This options is forced when run in daemon mode.")
    loggingGroupOpts.add_argument("-l", "--loglevel",
                                  action="store",
                                  default="NOTSET",
                                  dest="loglevel",
                                  metavar="log_level",
                                  help="log_level might be set to: CRITICAL, ERROR, WARNING, INFO, DEBUG. (Default: INFO)")
    loggingGroupOpts.add_argument("-f", "--logfile",
                                  action="store",
                                  default=globalvars.log_file,
                                  dest="logfile",
                                  metavar="log_file",
                                  help="log_file where the logs will be stored. If the file exists, text will be appended," +
                                  " otherwise the file will be created (Default: " + globalvars.log_file + ")")

    return parser.parse_args();



def _validate_command_Line_Options(opts):
    """
    Validate the passed arguments if needed
    """

    ##############################################################
    ##############################################################
    ##############################################################
    ##############################################################
    #### Add validation code for you options after this point ####
    ##############################################################
    ##############################################################
    ##############################################################
    ##############################################################

    ##############################################################
    ##############################################################
    ##############################################################
    ##############################################################
    #### Add validation code for you options until this point ####
    ##############################################################
    ##############################################################
    ##############################################################
    ##############################################################


def _set_logging(opts):
    global _quiet

    globalvars.daemonMode = opts.isDaemon
    _quiet = True if globalvars.daemonMode else opts.isQuiet
    _set_log_file(opts.logfile)
    _set_log_level(opts.loglevel)

def _set_log_level(loglevel):
    # Get the numeric loglevel provided by user (if provided)
    numeric_log_level = getattr(logging, loglevel.upper(), None)

    # Validate if the loglevel provided is correct (accepted)
    try:
        if not isinstance(numeric_log_level, int):
            raise ValueError()
    except ValueError:
        LOGGER.error('Invalid log level: %s' % loglevel)
        LOGGER.info('\tLog level must be set to one of the following:')
        LOGGER.info('\t   CRITICAL <- Least verbose')
        LOGGER.info('\t   ERROR')
        LOGGER.info('\t   WARNING')
        LOGGER.info('\t   INFO')
        LOGGER.info('\t   DEBUG    <- Most verbose')
        exit(globalvars.exitCode.INCORRECT_USAGE)

    if(numeric_log_level != logging.NOTSET):
        # If logging is set from the command line
        # define the logging policy
        globalvars.FileLogLevel = numeric_log_level
        _configureLogging()

    if(globalvars.FileLogLevel == logging.CRITICAL):
        LOGGER.info("Critical level logging is enabled")
    elif(globalvars.FileLogLevel == logging.ERROR):
        LOGGER.info("Error level logging is enabled")
    elif(globalvars.FileLogLevel == logging.WARNING):
        LOGGER.info("Warning level logging is enabled")
    elif(globalvars.FileLogLevel == logging.INFO):
        #LOGGER.info("Info level logging is enabled: Verbose")
        pass
    elif(globalvars.FileLogLevel == logging.DEBUG):
        LOGGER.info("Debug level logging is enabled: Very Verbose")

def _set_log_file(logfile):
    # Get the absolute path
    globalvars.log_file = os.path.abspath(logfile)
    # If the path exists and it is NOT a file, exit with an error message
    if(os.path.exists(globalvars.log_file) and not os.path.isfile(globalvars.log_file)):
        # Using print here because the LOGGER will try to
        # write to a file which is not yet writable
        print("ERROR: " + globalvars.log_file + " exists but it is not a file.")
        exit(globalvars.exitCode.INCORRECT_USAGE)
    _configureLogging()

def strip_string_list(string_list):
    """
    This function will parse all the elements from a list of strings (string_list),
    and trim leading or trailing white spaces and/or new line characters
    """
    return [s.strip() for s in string_list]

def split_strip(string, separator=","):
    """
    splits the given string in 'sep' and trims the whitespaces or new lines

    returns a list of the splitted stripped strings

    If the 'string' is not a string, -1 will be returned
    """
    if(isinstance(string, str)):
        return strip_string_list(string.split(separator))
    else:
        return -1

def _read_config_file(opts):
    """
    This function contains code to read from a configuration file
    """

    conffile = opts.conffile

    if(conffile !=  ""):
        # Get the absolute path
        globalvars.conf_file = os.path.abspath(conffile)
        # If the path exists and it is NOT a file, exit with an error message
        if(os.path.exists(globalvars.conf_file) and not os.path.isfile(globalvars.conf_file)):
            LOGGER.error(globalvars.conf_file + " exists but it is not a file.")
            exit(globalvars.exitCode.INCORRECT_USAGE)
    else:
        for confpath in globalvars.CONFIG_FILE_LOCATIONS:
            globalvars.conf_file = "{0}/{1}".format(confpath,globalvars.DEFAULT_CONFIG_FILENAME)
            if(os.path.isfile(globalvars.conf_file)):
                break
            else:
                globalvars.conf_file = ""
                LOGGER.debug("No configuration file found in: " + globalvars.conf_file)

    # If globalvars.conf_file var is still "" in this point, no configuration file is defined
    if(globalvars.conf_file ==  ""):
        LOGGER.debug("No configuration files found in the known paths")
        return


    try:
        with open(globalvars.conf_file):
            LOGGER.debug("Reading configuration from file " + globalvars.conf_file)
            config = ConfigParser.ConfigParser()
            config.read(globalvars.conf_file)
            ##################################################################################
            ##################################################################################
            ##################################################################################
            ##################################################################################
            ############### Add your code to read the configuration file here ################
            ##################################################################################
            ##################################################################################
            ##################################################################################
            ##################################################################################

            CurrentSection = "rtorrent"
            if(config.has_section(CurrentSection)):
                if(config.has_option(CurrentSection, "xmlrpc_bin")):
                    globalvars.xmlrpc_bin = config.get(CurrentSection, "xmlrpc_bin")
                    LOGGER.debug("xmlrpc_bin = " + globalvars.xmlrpc_bin)
                if(config.has_option(CurrentSection, "rtorrent_xmlrpc_url")):
                    globalvars.rtorrent_xmlrpc_url = config.get(CurrentSection, "rtorrent_xmlrpc_url")
                    LOGGER.debug("rtorrent_xmlrpc_url = " + globalvars.rtorrent_xmlrpc_url)
                if(config.has_option(CurrentSection, "username")):
                    globalvars.username = config.get(CurrentSection, "username")
                    LOGGER.debug("username = " + globalvars.username)
                if(config.has_option(CurrentSection, "password")):
                    globalvars.password = config.get(CurrentSection, "password")
                    LOGGER.debug("password = " + globalvars.password)
                if(config.has_option(CurrentSection, "trackers")):
                    globalvars.trackers = config.get(CurrentSection, "trackers")
                    globalvars.trackers = split_strip(globalvars.trackers)
                    LOGGER.debug("trackers = ")
                    LOGGER.debug(globalvars.trackers)

            ##################################################################################
            ##################################################################################
            ##################################################################################
            ##################################################################################
            ###############                    Until here                     ################
            ##################################################################################
            ##################################################################################
            ##################################################################################
            ##################################################################################

            LOGGER.debug("Finished reading configuration from file " + globalvars.conf_file)

            return
    except:
        LOGGER.error("\n" + traceback.format_exc())
        exit(globalvars.exitCode.FAILURE)

def _configureLogging():
    # Configure a defaultLogger
    defaultLogger = logging.getLogger('default')

    # Define the format of file log output
    logFileFormatter = DefaultLoggingFormatter("%(asctime)s, %(levelname)8s, %(module)15s:%(lineno)-7d %(message)s", "%Y-%m-%d %H:%M:%S.%f, %s%f")

    # Define the format of console log output
    logConsoleFormatter = VisualFormatter()

    # Set default logging level
    defaultLogger.setLevel(logging.DEBUG)

    # Enable logging in a file
    defaultFileHandler = logging.FileHandler(globalvars.log_file)
    defaultFileHandler.setLevel(globalvars.FileLogLevel)
    defaultFileHandler.setFormatter(logFileFormatter)

    # Enable logging to the console
    defaultConsoleHandler = logging.StreamHandler()
    defaultConsoleHandler.setLevel(globalvars.CONSOLE_LOG_LEVEL)
    defaultConsoleHandler.setFormatter(logConsoleFormatter)

    # Remove existing handlers if present
    defaultLogger.handlers = []

    # If quiet, set the level very high to suppress all
    # messages in the console handlers.
    if(_quiet):
        defaultConsoleHandler.setLevel(1000)

    # Add the handlers to the loggers
    defaultLogger.addHandler(defaultFileHandler)
    defaultLogger.addHandler(defaultConsoleHandler)

class DefaultLoggingFormatter(logging.Formatter):
    """
    The logging.Formatter does not accept %f argument
    which returns microseconds because it is using
    struct_time.

    This class, uses datetime instead, to provide microsecond
    precision in logging time.
    """
    import datetime

    converter=datetime.datetime.fromtimestamp
    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            t = ct.strftime("%Y-%m-%d %H:%M:%S")
            s = "%s,%03d" % (t, record.msecs)
        return s

class VisualFormatter(DefaultLoggingFormatter):
    """
    This visual formatter allows the user to
    Define different formats and date formats
    for different Log Levels

    fmt sets the global format

    datefmt sets the global date format

    xxx_fmt sets the format for each xxx level

    xxx_datefmt set the date format for each xxx level
    """
    def __init__(self, fmt=None, datefmt=None,
                 dbg_fmt=None, dbg_datefmt=None,
                 info_fmt=None, info_datefmt=None,
                 warn_fmt=None, warn_datefmt=None,
                 err_fmt=None, err_datefmt=None,
                 crit_fmt=None, crit_datefmt=None):

        # If fmt is set, instantiate the format
        # for each level to this of fmt
        # Otherwise set the default values
        if(fmt is not None):
            self._dbg_fmt = fmt
            self._info_fmt = fmt
            self._warn_fmt = fmt
            self._err_fmt = fmt
            self._crit_fmt = fmt
        else:
            self._dbg_fmt = "{0},{1}:{2}   {3}".format("%(levelname)8s", "%(module)15s", "%(lineno)d", "%(message)s")
            self._info_fmt = "%(message)s"
            self._warn_fmt = self._dbg_fmt
            self._err_fmt = self._dbg_fmt
            self._crit_fmt = self._dbg_fmt

        # If each individual format has been set
        # then choose this one for each specific level
        if(dbg_fmt):
            self._dbg_fmt = dbg_fmt
        if(info_fmt):
            self._info_fmt = info_fmt
        if(warn_fmt):
            self._warn_fmt = warn_fmt
        if(err_fmt):
            self._err_fmt = err_fmt
        if(crit_fmt):
            self._crit_fmt = crit_fmt

        # instantiate the date format for each level
        # to this of datefmt
        self._dbg_datefmt = datefmt
        self._info_datefmt = datefmt
        self._warn_datefmt = datefmt
        self._err_datefmt = datefmt
        self._crit_datefmt = datefmt

        # If each individual date format has been set
        # then choose this one for each specific level
        if(dbg_datefmt):
            self._dbg_datefmt = dbg_datefmt
        if(info_datefmt):
            self._info_datefmt = info_datefmt
        if(warn_datefmt):
            self._warn_datefmt = warn_datefmt
        if(err_datefmt):
            self._err_datefmt = err_datefmt
        if(crit_datefmt):
            self._crit_datefmt = crit_datefmt


    def format(self, record):

        # Replace the original format with one customized by logging level
        if record.levelno == logging.DEBUG:
            self.datefmt = self._dbg_datefmt
            self._fmt = self._dbg_fmt
        elif record.levelno == logging.INFO:
            self.datefmt = self._info_datefmt
            self._fmt = self._info_fmt
        elif record.levelno == logging.WARNING:
            self.datefmt = self._warn_datefmt
            self._fmt = self._warn_fmt
        elif record.levelno == logging.ERROR:
            self.datefmt = self._err_datefmt
            self._fmt = self._err_fmt
        elif record.levelno == logging.CRITICAL:
            self.datefmt = self._crit_datefmt
            self._fmt = self._crit_fmt

        # Call the original formatter class to do the grunt work
        result = logging.Formatter.format(self, record)

        return result
