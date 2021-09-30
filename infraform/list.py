# Copyright 2021 Arie Bregman
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
import logging
import os
import re
from tabulate import tabulate

from infraform.utils.file import get_match_until_first_dot

LOG = logging.getLogger(__name__)

SCENARIOS_PATH = os.path.dirname(__file__) + '/../infraform/scenarios'


def list_scenarios(show_path=False):
    scenarios = []
    # The headers of the table that will be displayed to the user
    headers = ["Scenario Name", "Description", "Platform"]
    # Showing the path is optional and based on user choice
    if show_path:
        headers.append("Path")

    # Walk through the tree of scenarios to find
    # scenario files (ending with .ifr)
    for (dirpath, dirnames, filenames) in os.walk(SCENARIOS_PATH):
        for f in filenames:
            if "." in f:
                suffix = f.split('.')[1]
                if suffix == "ifr":
                    # Get scenario name and path
                    name = get_match_until_first_dot(f)
                    scenario_path = dirpath + '/' + f

                    # Read scenario content
                    platform = description = '-'
                    with open(scenario_path, 'r') as f:
                        for line in f.readlines():
                            if re.findall("description:(.*)", line):
                                description = re.findall("description:(.*)",
                                                         line)[0]
                            if re.findall("platform:(.*)",
                                          line):
                                platform = re.findall("platform:(.*)", line)[0]
                    scenario = [name, description, platform]
                    if show_path:
                        scenario.append(scenario_path)
                    scenarios.append(scenario)
    LOG.info(tabulate(scenarios, headers=headers))
