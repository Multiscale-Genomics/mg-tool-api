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

import sys
import datetime

"""
This is the logging facility of the mg-tool-api. It is meant to provide
a unified way for Tools to log information that needs to be read by the
VRE (e.g. information about progress, errors, exceptions, etc.).

It provides the following commonly used logging levels:

DEBUG:   Detailed information, typically of interest only when
         diagnosing problems.
INFO:    Confirmation that Tool execution is working as expected.
WARNING: An indication that something unexpected happened, but that the
         Tool can continue working successfully.
ERROR:   A more serious problem has occurred, and the Tool will not be
         able to perform some function.
FATAL:   A serious error, indicating that the Tool may be unable to
         continue running.

As well as the following non-standard levels:

PROGRESS: Provide the VRE with information about Tool execution progress.
"""  # pylint: disable=pointless-string-statement


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

_levelNames = {  # pylint: disable=invalid-name
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
    """
    Function to print out the logging input
    """
    log_time = datetime.datetime.now()
    log_ts = "{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
        log_time.year, log_time.month, log_time.day,
        log_time.hour, log_time.minute, log_time.second)
    if level not in _levelNames:
        level = INFO
    outstream = sys.stdout
    if level in STDERR_LEVELS:
        outstream = sys.stderr
    outstream.write("{} | {}: {}\n".format(
        log_ts, _levelNames[level], message.format(*args, **kwargs)))
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


# Required for compatibility legacy code
warning = warn  # pylint: disable=invalid-name


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

# Required for compatibility legacy code
critical = fatal  # pylint: disable=invalid-name


# Special loggers
def progress(message, *args, **kwargs):
    """
    Provides information about Tool progress.

    Logs a message containing information about Tool progress, with level
    ``PROGRESS``.

    The arguments are interpreted as for ``debug()`` (see below for exceptions).

    This function provides two pre-baked log message formats, that can be
    activated by specifying the following items in ``**kwargs``:

    Parameters
    ----------
    status : str
        Status of the Tool
        logs "MESSAGE - STATUS"

    task_id : int
        Current task; requires also the "total" item
        logs "MESSAGE (TASK_ID/TOTAL)

    total : int
        Total number of tasks, should be provided in conjunction with task_id
        logs "MESSAGE (TASK_ID/TOTAL)

    Example
    -------

    .. code-block:: python
       :linenos:

       class TestTool(Tool):
           def run(self, input_files, input_metadata, output_files):
               logger.progress("TestTool starting", status="RUNNING")
               total_tasks = 3

               self.task1()
               logger.progress("TestTool", task_id=1, total=total_tasks)

               self.task2()
               logger.progress("TestTool", task_id=2, total=total_tasks)

               self.task3()
               logger.progress("TestTool", task_id=3, total=total_tasks)

               logger.progress("TestTool", status="DONE")
               return True

    """

    if "status" in kwargs:
        return __log(PROGRESS, "{} - {}", message, kwargs["status"])

    if "task_id" in kwargs:
        return __log(PROGRESS, "{} ({}/{})", message, kwargs["task_id"], kwargs["total"])

    return __log(PROGRESS, message, *args, **kwargs)
