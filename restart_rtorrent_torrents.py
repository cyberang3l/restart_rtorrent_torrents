#!/usr/bin/env python
#coding:utf-8
# Author:  Vangelis Tasoulas --<cyberang3l@gmail.com>

import os
import sys
import re
from libs import globalvars
from libs import parseoptions
from libs.parseoptions import LOGGER
import datetime
import subprocess
import time

#----------------------------------------------------------------------
class executeCommand(object):
    """
    Custom class to execute a shell command and
    provide to the user, access to the returned
    values
    """

    def __init__(self, args=None, isUtc=True):
        self._stdout = None
        self._stderr = None
        self._returncode = None
        self._timeStartedExecution = None
        self._timeFinishedExecution = None
        self._args = args
        self.isUtc = isUtc
        if(self._args != None):
            self.execute()

    def execute(self, args=None):
        if(args != None):
            self._args = args

        if(self._args != None):
            if(self.isUtc):
                self._timeStartedExecution = datetime.datetime.utcnow()
            else:
                self._timeStartedExecution = datetime.datetime.now()
            p = subprocess.Popen(self._args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if(self.isUtc):
                self._timeFinishedExecution = datetime.datetime.utcnow()
            else:
                self._timeFinishedExecution = datetime.datetime.now()
            self._stdout, self._stderr = p.communicate()
            self._returncode = p.returncode
            return 1
        else:
            self._stdout = None
            self._stderr = None
            self._returncode = None
            return 0

    def getStdout(self, getList=True):
        """
        Get the standard output of the executed command

        getList: If True, return a list of lines.
                 Otherwise, return the result as one string
        """

        if getList:
            return self._stdout.split('\n')

        return self._stdout

    def getStderr(self, getList=True):
        """
        Get the error output of the executed command

        getList: If True, return a list of lines.
                 Otherwise, return the result as one string
        """

        if getList:
            return self._stderr.split('\n')

        return self._stderr

    def getReturnCode(self):
        """
        Get the exit/return status of the command
        """
        return self._returncode

    def getTimeStartedExecution(self, inMicroseconds=False):
        """
        Get the time when the execution started
        """
        if(isinstance(self._timeStartedExecution, datetime.datetime)):
            if(inMicroseconds):
                return int(str(calendar.timegm(self._timeStartedExecution.timetuple())) + str(self._timeStartedExecution.strftime("%f")))
                #return self.__timeStartedExecution.strftime("%s%f")
        return self._timeStartedExecution

    def getTimeFinishedExecution(self, inMicroseconds=False):
        """
        Get the time when the execution finished
        """
        if(isinstance(self._timeFinishedExecution, datetime.datetime)):
            if(inMicroseconds):
                return int(str(calendar.timegm(self._timeFinishedExecution.timetuple())) + str(self._timeFinishedExecution.strftime("%f")))
                #return self.__timeStartedExecution.strftime("%s%f")
        return self._timeFinishedExecution

#----------------------------------------------------------------------
class execute_xmlrpc_command(executeCommand):
    def __init__(self, args=None, isUtc=True):
        super(execute_xmlrpc_command, self).__init__(args, isUtc)

    def execute(self, args=None):
        if(args != None):
            self._args = args

        if(self._args != None):
            self._modified_args=self._args
            self._modified_args.insert(0, globalvars.rtorrent_xmlrpc_url)
            self._modified_args.insert(0, globalvars.xmlrpc_bin)
            self._modified_args.extend(['-username', globalvars.username, '-password', globalvars.password, '-curlnoverifypeer', 't', '-curlnoverifyhost', 't'])
            if(self.isUtc):
                self._timeStartedExecution = datetime.datetime.utcnow()
            else:
                self._timeStartedExecution = datetime.datetime.now()
            p = subprocess.Popen(self._modified_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if(self.isUtc):
                self._timeFinishedExecution = datetime.datetime.utcnow()
            else:
                self._timeFinishedExecution = datetime.datetime.now()
            self._stdout, self._stderr = p.communicate()
            self._returncode = p.returncode
            return 1
        else:
            self._stdout = None
            self._stderr = None
            self._returncode = None
            return 0

#----------------------------------------------------------------------
def print_(value_to_be_printed, print_indent=0, spaces_per_indent=4, endl="\n"):
    """
    This function, among anything else, it will print dictionaries (even nested ones) in a good looking way

    # value_to_be_printed: The only needed argument and it is the
                           text/number/dictionary to be printed
    # print_indent: indentation for the printed text (it is used for
                    nice looking dictionary prints) (default is 0)
    # spaces_per_indent: Defines the number of spaces per indent (default is 4)
    # endl: Defines the end of line character (default is \n)

    More info here:
    http://stackoverflow.com/questions/19473085/create-a-nested-dictionary-for-a-word-python?answertab=active#tab-top
    """

    if(isinstance(value_to_be_printed, dict)):
        for key, value in value_to_be_printed.iteritems():
            if(isinstance(value, dict)):
                print_('{0}{1!r}:'.format(print_indent * spaces_per_indent * ' ', key))
                print_(value, print_indent + 1)
            else:
                print_('{0}{1!r}: {2}'.format(print_indent * spaces_per_indent * ' ', key, value))
    else:
        string = ('{0}{1}{2}'.format(print_indent * spaces_per_indent * ' ', value_to_be_printed, endl))
        sys.stdout.write(string)

#----------------------------------------------------------------------
class quick_regexp(object):
    """
    Quick regular expression class, which can be used directly in if() statements in a perl-like fashion.

    #### Sample code ####
    r = quick_regexp()
    if(r.search('pattern (test) (123)', string)):
        print(r.groups[0]) # Prints 'test'
        print(r.groups[1]) # Prints '123'
    """
    def __init__(self):
        self.groups = None
        self.matched = False

    def search(self, pattern, string, flags=0):
        match = re.search(pattern, string, flags)
        if match:
            self.matched = True
            if(match.groups()):
                self.groups = re.search(pattern, string, flags).groups()
            else:
                self.groups = True
        else:
            self.matched = False
            self.groups = None

        return self.matched

######################################
######################################
######################################
######################################
## Write your main application code ##
######################################
######################################
######################################
######################################

# https://code.google.com/p/gi-torrent/wiki/rTorrent_XMLRPC_reference

# WORKING COMMANDS!

# xmlrpc localhost download_list
# xmlrpc localhost download_list "" "incomplete"
# xmlrpc localhost download_list "" "complete"
# xmlrpc localhost download_list "" "seeding"
# xmlrpc localhost download_list "" "stopped"
# xmlrpc localhost download_list "" "started"
# xmlrpc localhost download_list "" "hashing"
# xmlrpc localhost download_list "" "active"

# xmlrpc https://localhost/RPC2 d.multicall "" "d.get_hash=" "d.get_name=" "d.get_state=" "d.get_complete=" "d.is_active=" "d.is_hash_checking=" "d.get_down_rate=" -username user -password 'p@ss' -curlnoverifypeer t -curlnoverifyhost t


# xmlrpc localhost d.get_base_filename 179A53187190FF9C3EBABE8D8D63AF70FED9C47A
# xmlrpc localhost d.multicall "main" "d.get_hash=" "d.get_name=" "d.get_base_filename=" "d.get_down_rate=" "to_kb=\$d.get_bytes_done=" "to_kb=\$d.get_left_bytes=" "to_kb=\$d.get_size_bytes="

# xmlrpc localhost t.get_url 179A53187190FF9C3EBABE8D8D63AF70FED9C47A:t0

# d.get_state=
#     0 = stopped
#     1 = started
# d.get_complete=
#     0 = Not completed
#     1 = Completed downloading
# d.is_active=
#     0 = inactive
#     1 = active
# d.is_hash_checking=
#     0 = not hash checking
#     1 = hash checking


class Main(object):
    def __init__(self):
        # Parse configuration files and command line options
        parseoptions.parse_all_conf()

    def exec_(self):
        # Print the program name and version if the logging level is set to info
        #LOGGER.info(globalvars.PROGRAM_NAME + " " + globalvars.VERSION + " started...")

        command = execute_xmlrpc_command()
        r = quick_regexp()
        torrent_hashes = {}

        command.execute(['d.multicall', "", "d.get_hash=", "d.get_name=", "d.get_state=", "d.get_complete=", "d.is_active=", "d.is_hash_checking=", "d.get_down_rate="])
        command_output = command.getStdout(getList=True)
        i = 0

        LOGGER.debug("All available torrents:")
        while i < len(command_output):
            line = command_output[i]
            if r.search('^\s*Index\s+\d+\s+Array\s+of\s+\d+\s+items:', line):
                hash_string = None
                #print i, line
                for j in range(1, 8):
                    i += 1
                    line = command_output[i]
                    if j == 1:
                        # Hash
                        if r.search('^\s*Index\s+\d+\s+String:\s+\'(.*)\'', line):
                            hash_string = r.groups[0]
                            torrent_hashes[hash_string] = {}
                            LOGGER.debug(hash_string + ":")
                    elif j == 2:
                        # Name
                        if r.search('^\s*Index\s+\d+\s+String:\s+\'(.*)\'', line):
                            torrent_hashes[hash_string]['name'] = r.groups[0]
                            LOGGER.debug("name: " + torrent_hashes[hash_string]['name'])
                    elif j == 3:
                        # State
                        if r.search('^\s*Index\s+\d+\s+64-bit\s+integer:\s*(.*)', line):
                            torrent_hashes[hash_string]['state'] = int(r.groups[0])
                            LOGGER.debug("state: " + str(torrent_hashes[hash_string]['state']))
                    elif j == 4:
                        # Complete
                        if r.search('^\s*Index\s+\d+\s+64-bit\s+integer:\s*(.*)', line):
                            torrent_hashes[hash_string]['complete'] = int(r.groups[0])
                            LOGGER.debug("complete: " + str(torrent_hashes[hash_string]['complete']))
                    elif j == 5:
                        # Active
                        if r.search('^\s*Index\s+\d+\s+64-bit\s+integer:\s*(.*)', line):
                            torrent_hashes[hash_string]['active'] = int(r.groups[0])
                            LOGGER.debug("active: " + str(torrent_hashes[hash_string]['active']))
                    elif j == 6:
                        # Is hash checking
                        if r.search('^\s*Index\s+\d+\s+64-bit\s+integer:\s*(.*)', line):
                            torrent_hashes[hash_string]['is_hash_checking'] = int(r.groups[0])
                            LOGGER.debug("is_hash_checking: " + str(torrent_hashes[hash_string]['is_hash_checking']))
                    elif j == 7:
                        # Is hash checking
                        if r.search('^\s*Index\s+\d+\s+64-bit\s+integer:\s*(.*)', line):
                            torrent_hashes[hash_string]['download_rate'] = int(r.groups[0])
                            LOGGER.debug("download_rate: " + str(torrent_hashes[hash_string]['download_rate']))

                    #print i, j, line
            i += 1

        #print_(torrent_hashes)

        for hash_string, values in torrent_hashes.items():
            # If the hash is checked, remove it from the list since
            # we are not allowed to stop/start the torrent
            if torrent_hashes[hash_string]['is_hash_checking']:
                del torrent_hashes[hash_string]
                continue

            # If the torrent is stopped or paused, remove it from the list
            if not torrent_hashes[hash_string]['state']:
                del torrent_hashes[hash_string]
                continue

            # If the torrent is completly downloaded, remove it from the list
            if torrent_hashes[hash_string]['complete']:
                del torrent_hashes[hash_string]
                continue

            # A torrent which is not stopped or paused (if it was stopped or paused we would
            # have already removed it from the list until this point) and it is not active either,
            # it is usually in the Queued state.
            # So if a torrent is in a Queued state, then do not stop/start it (so remove it from the list)
            if not torrent_hashes[hash_string]['active']:
                del torrent_hashes[hash_string]
                continue

            # If the torrent download speed is not zero, remove it from the list as it is not
            # need to be restarted
            if torrent_hashes[hash_string]['download_rate']:
                del torrent_hashes[hash_string]
                continue

            # If the torrent is not from a tracker listed in the "globalvars.trackers", remove it from the list.
            # We only want to restart torrents that are listed in one of the given trackers.
            command.execute(['t.get_url', hash_string + ":t0"])
            for line in command.getStdout(getList=True):
                if r.search('^\s*String:\s+\'(.*)\'', line):
                    LOGGER.debug("Tracker of torrent '" + torrent_hashes[hash_string]['name'] + "' is: " + r.groups[0])
                    tracker_found = False
                    for tracker in globalvars.trackers:
                        if(r.groups[0].find(tracker) != -1):
                            tracker_found = True
                            break

                    if not tracker_found:
                        LOGGER.debug("Tracker of torrent '" + torrent_hashes[hash_string]['name'] + "' is not in the list. Torrent will not be restarted.")
                        del torrent_hashes[hash_string]


        #print_(torrent_hashes)

        LOGGER.debug("Torrents to be restarted:")
        # At this point of code execution, we have only torrents that they should be stopped/started if their download rate is 0
        for hash_string in torrent_hashes.keys():
            LOGGER.info("Restarting torrent '" + torrent_hashes[hash_string]['name'] + "'")
            command.execute(['d.stop', hash_string])
            time.sleep(2)
            command.execute(['d.start', hash_string])




######################################
######################################
######################################
######################################
### End your main application code ###
######################################
######################################
######################################
######################################

if __name__ == '__main__':
    # Load the main class
    main = Main()

    # Execute
    main.exec_()
