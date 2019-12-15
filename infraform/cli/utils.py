# Copyright 2019 Arie Bregman
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import os

from infraform.platforms.platform import Platform
from infraform.exceptions.utils import success_or_exit

SCENARIOS_PATH = os.path.dirname(__file__) + '/../scenarios'


def guess_platform(scenario):
    """Try to figure out which platform the user should use or fail."""
    scenario_path, scenario_file = Platform.verify_scenario_exists(
        SCENARIOS_PATH, scenario)
    if scenario_file.endswith(".tf"):
        return "terraform"
    if scenario_file.endswith(".py"):
        return "python"
    if scenario_file.endswith(".sh"):
        return "shell"
    if os.path.dirname(scenario_path).split('/')[-1] == "podman":
        return "podman"
    success_or_exit(
        1,
        "Couldn't figure out which platform to use. Please specify --platform")
