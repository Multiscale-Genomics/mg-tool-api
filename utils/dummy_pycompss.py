"""
.. Copyright 2002-2015 Barcelona Supercomputing Center (www.bsc.es)

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

   This code is based on the dummy functions from the pyCOMPSS module so that the
   functions can be run outside of the COMPS environment for testing purposes.
"""

from __future__ import print_function
from functools import wraps


def compss_wait_on(job):
    """
    Dummy wait on function
    """
    return job


def compss_open(job, *args, **kwargs):  # pylint: disable=unused-argument
    """
    Dummy open function required when copying from out of the COMPSs system
    """
    return job


def compss_delete_file(job, *args, **kwargs):  # pylint: disable=unused-argument
    """
    Dummy delete file function required when deleting files in the COMPSs system
    """
    pass


def compss_delete_object(job, *args, **kwargs):  # pylint: disable=unused-argument
    """
    Dummy delete file function required when deleting objects in the COMPSs system
    """
    pass


def compss_delete(*args, **kwargs):  # pylint: disable=unused-argument
    """
    Dummy delete file function required when deleting from the COMPSs system
    """
    pass


def barrier():
    """
    Dummy function to trigger the pipeline to wait till all jobs have completed
    """
    pass


def local(job):
    """
    Dummy local function for triggering the job to be run locally on the head
    node
    """
    return job


class constraint(object):  # pylint: disable=invalid-name,too-few-public-methods
    """
    Dummy function for handling the contraint decorators
    """
    @wraps(object)
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, function):
        @wraps(function)
        def wrapped_f(*args, **kwargs):
            """
            Function wrapper for the decorator
            """
            return function(*args, **kwargs)
        return wrapped_f


class task(object):  # pylint: disable=invalid-name,too-few-public-methods
    """
    Dummy function for handling the task decorators
    """

    @wraps(object)
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, function):
        @wraps(function)
        def wrapped_f(*args, **kwargs):
            """
            Function wrapper for the decorator
            """
            return function(*args, **kwargs)
        return wrapped_f


# Numbers match both C and Java enums
class Direction(object):  # pylint: disable=too-few-public-methods
    """
    Dummy function for handling the direction for the movement of files
    """
    IN = 0  # pylint: disable=invalid-name
    OUT = 1
    INOUT = 2


# Numbers match both C and Java enums
class Type(object):  # pylint: disable=too-few-public-methods
    """
    Dummy function to determine the object types that are being handled
    """
    FILE = 0
    BOOLEAN = 1
    STRING = 3
    INT = 6
    LONG = 7
    FLOAT = 9    # C double
    OBJECT = 10
    # COMPLEX = 8


class Parameter(object):  # pylint: disable=too-few-public-methods
    """
    Dummy function for the collective handling of parameters
    """
    @wraps(object)
    def __init__(self, p_type=None, p_direction=Direction.IN):
        self.type = p_type
        self.direction = p_direction
        self.value = None    # placeholder for parameter value


# Aliases for parameters
IN = Parameter()
OUT = Parameter(p_direction=Direction.OUT)
INOUT = Parameter(p_direction=Direction.INOUT)

FILE = Parameter(p_type=Type.FILE)
FILE_IN = Parameter(p_type=Type.FILE)
FILE_OUT = Parameter(p_type=Type.FILE, p_direction=Direction.OUT)
FILE_INOUT = Parameter(p_type=Type.FILE, p_direction=Direction.INOUT)

# Java max and min integer and long values
JAVA_MAX_INT = 2147483647
JAVA_MIN_INT = -2147483648
JAVA_MAX_LONG = PYTHON_MAX_INT = 9223372036854775807
JAVA_MIN_LONG = PYTHON_MIN_INT = -9223372036854775808
