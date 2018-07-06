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

import re
import pytest

from utils import logger


@pytest.mark.debug
def test_debug(capsys):
    """
    Test the basic use of the DEBUG function
    """
    logger.debug("test")
    captured = capsys.readouterr()
    assert re.search("DEBUG: test", captured[0])


@pytest.mark.info
def test_info(capsys):
    """
    Test the basic use of the INFO function
    """
    logger.info("test")
    captured = capsys.readouterr()
    assert re.search("INFO: test", captured[0])


@pytest.mark.warn
def test_warn(capsys):
    """
    Test the basic use of the WARN function
    """
    logger.warn("test")
    captured = capsys.readouterr()
    assert re.search("WARNING: test", captured[1])


@pytest.mark.error
def test_error(capsys):
    """
    Test the basic use of the ERROR function
    """
    logger.error("test")
    captured = capsys.readouterr()
    assert re.search("ERROR: test", captured[1])


@pytest.mark.fatal
def test_fatal(capsys):
    """
    Test the basic use of the FATAL function
    """
    logger.fatal("test")
    captured = capsys.readouterr()
    assert re.search("FATAL: test", captured[1])


@pytest.mark.progress
def test_progress_00(capsys):
    """
    Test the basic use of the PROGRESS function
    """
    logger.progress("test")
    captured = capsys.readouterr()
    assert re.search("PROGRESS: test", captured[0])


@pytest.mark.progress
def test_progress_01(capsys):
    """
    Test the PROGRESS function for reporting task completion
    """
    logger.progress("test", status="RUNNING")
    captured = capsys.readouterr()
    assert re.search("PROGRESS: test - RUNNING", captured[0])

    logger.progress("test", status="DONE")
    captured = capsys.readouterr()
    assert re.search("PROGRESS: test - DONE", captured[0])


@pytest.mark.progress
def test_progress_02(capsys):
    """
    Test the PROGRESS function for reporting tool progress
    """
    logger.progress("test", task_id=2, total=5)
    captured = capsys.readouterr()
    assert re.search("PROGRESS: test \(2\/5\)", captured[0])
