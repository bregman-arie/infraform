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


def list_scenarios():
    scenarios = []
    headers = ["Scenario Name", "Path", "Description"]
    for (dirpath, dirnames, filenames) in os.walk(SCENARIOS_PATH):
        for f in filenames:
            name = get_match_until_first_dot(f)
            scenario_path = dirpath + '/' + f
            with open(scenario_path, 'r') as f:
                description = get_description(f)
            scenarios.append([name, scenario_path, description])
    LOG.info(tabulate(scenarios, headers=headers))
