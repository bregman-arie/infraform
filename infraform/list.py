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
import logging
import os
from tabulate import tabulate

from infraform.utils import get_match_until_first_dot
from infraform.utils import get_description

LOG = logging.getLogger(__name__)

SCENARIOS_PATH = os.path.dirname(__file__) + '/../infraform/scenarios'


def list_scenarios(show_path=False):
    scenarios = []
    # The headers of the table that will be displayed to the user
    headers = ["Scenario Name", "Description"]
    if show_path:
        headers.append("Path")
    # Iterate over the scenarios
    for scenario_f in os.listdir(SCENARIOS_PATH):
        scenario_path = os.path.join(SCENARIOS_PATH, scenario_f)
        if os.path.isfile(os.path.join(SCENARIOS_PATH, scenario_f)):
            if "ifr" in scenario_f and "." in scenario_f:
                scenario_info = [scenario_f.split('.')[0]]
                suffix = scenario_f.split('.')[1]
                if suffix == "ifr":
                    with open(scenario_path, 'r') as f:
                        description = get_description(f)
                    scenario_info.append(description)
                if show_path:
                    scenario_info.append(scenario_path)
                scenarios.append(scenario_info)
            
    LOG.info(tabulate(scenarios, headers=headers))
