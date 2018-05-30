#!/usr/bin/env python
"""
.. See the NOTICE file distributed with this work for additional information
   regarding copyright ownership.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

"""
This is the logging facility of the mg-tool-api. It is meant to provide
a unified way for Tools to log information that needs to be read by the
VRE (e.g. information about progress, errors, exceptions, etc.).

It provides the following commonly used logging levels:

DEBUG:		Detailed information, typically of interest only when
		diagnosing problems.
INFO:		Confirmation that Tool execution is working as expected.
WARNING:	An indication that something unexpected happened, but that the
		Tool can continue working successfully.
ERROR:		A more serious problem has occurred, and the Tool will not be
		able to perform some function.
FATAL:		A serious error, indicating that the Tool may be unable to
		continue running.

As well as the following non-standard levels:

PROGRESS:	Provide the VRE with information about Tool execution progress,
		in the form of a percentage (0-100)
"""

import sys

CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
PROGRESS = 21
INFO = 20
DEBUG = 10

STDOUT_LEVELS = [DEBUG, INFO, PROGRESS]
STDERR_LEVELS = [WARNING, ERROR, FATAL, CRITICAL]

_levelNames = {
    FATAL: 'FATAL',
    ERROR: 'ERROR',
    WARNING: 'WARNING',
    PROGRESS: 'PROGRESS',
    INFO: 'INFO',
    DEBUG: 'DEBUG',
    WARN: 'WARNING',
    CRITICAL: 'FATAL'
}


def __log(level, message, *args, **kwargs):
    if level not in _levelNames:
        level = INFO
    outstream = sys.stdout
    if level in STDERR_LEVELS:
        outstream = sys.stderr
    outstream.write("{}: {}\n".format(
        _levelNames[level], message.format(*args, **kwargs)))
    return True

def debug(message, *args, **kwargs):
    """
    Logs a message with level DEBUG.

    'message' is the message format string, and the args are the arguments
    which are merged into msg using the string formatting operator. (Note that
    this means that you can use keywords in the format string, together with a
    single dictionary argument.)
    """
    return __log(DEBUG, message, *args, **kwargs)

def info(message, *args, **kwargs):
    """
    Logs a message with level INFO. The arguments are interpreted as for
    debug().
    """
    return __log(INFO, message, *args, **kwargs)

def warn(message, *args, **kwargs):
    """
    Logs a message with level WARNING. The arguments are interpreted as for
    debug().
    """
    return __log(WARNING, message, *args, **kwargs)

warning = warn

def error(message, *args, **kwargs):
    """
    Logs a message with level ERROR. The arguments are interpreted as for
    debug().
    """
    return __log(ERROR, message, *args, **kwargs)

def fatal(message, *args, **kwargs):
    """
    Logs a message with level FATAL. The arguments are interpreted as for
    debug().
    """
    return __log(FATAL, message, *args, **kwargs)
critical=fatal

## Special loggers
def progress(message, *args, **kwargs):
    """
    Provides information about progress.

    In fact it logs a message containing the percentage with level PERCENTAGE.
    """
    if "status" in kwargs:
        __log(PROGRESS, "{} - {}", message, kwargs["status"])
    elif "task_id" in kwargs:
        __log(PROGRESS, "{} ({}/{})", message, kwargs["task_id"], kwargs["total"])
    else:
        __log(PROGRESS, message, *args, **kwargs)
    return True

