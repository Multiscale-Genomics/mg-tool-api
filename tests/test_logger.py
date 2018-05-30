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

import pytest

from utils import logger


@pytest.mark.progress
def test_progress_00(capsys):
    """
    Test the basic use of the PROGRESS function
    """
    logger.progress("test")
    captured = capsys.readouterr()
    assert captured[0] == "PROGRESS: test\n"


@pytest.mark.progress
def test_progress_01(capsys):
    """
    Test the PROGRESS function for reporting task completion
    """
    logger.progress("test", status="RUNNING")
    captured = capsys.readouterr()
    assert captured[0] == "PROGRESS: test - RUNNING\n"

    logger.progress("test", status="DONE")
    captured = capsys.readouterr()
    assert captured[0] == "PROGRESS: test - DONE\n"


@pytest.mark.progress
def test_progress_02(capsys):
    """
    Test the PROGRESS function for reporting tool progress
    """
    logger.progress("test", task_id=2, total=5)
    captured = capsys.readouterr()
    assert captured[0] == "PROGRESS: test (2/5)\n"
