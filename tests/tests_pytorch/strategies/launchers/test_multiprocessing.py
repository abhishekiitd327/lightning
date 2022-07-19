# Copyright The PyTorch Lightning team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from unittest import mock
from unittest.mock import ANY, Mock

import pytest

from pytorch_lightning.strategies.launchers.multiprocessing import _MultiProcessingLauncher


@mock.patch("pytorch_lightning.strategies.launchers.multiprocessing.mp.get_all_start_methods", return_value=[])
def test_spawn_launcher_forking_on_unsupported_platform(_):
    launcher = _MultiProcessingLauncher(strategy=Mock(), start_method="fork")
    with pytest.raises(ValueError, match="The start method 'fork' is not available on this platform"):
        launcher.launch(function=Mock())


@pytest.mark.parametrize("start_method", ["spawn", "fork"])
@mock.patch("pytorch_lightning.strategies.launchers.multiprocessing.mp")
def test_spawn_launcher_start_method(mp_mock, start_method):
    mp_mock.get_all_start_methods.return_value = [start_method]
    launcher = _MultiProcessingLauncher(strategy=Mock(), start_method=start_method)
    launcher.launch(function=Mock())
    mp_mock.get_context.assert_called_with(start_method)
    mp_mock.start_processes.assert_called_with(
        ANY,
        args=ANY,
        nprocs=ANY,
        start_method=start_method,
    )
