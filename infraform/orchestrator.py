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

from infraform.workspace import Workspace
from infraform.exceptions import usage as usage_exc
from infraform.utils import file as file_utils
from infraform.scenario import Scenario

LOG = logging.getLogger(__name__)


class Orchestrator(object):

    def __init__(self, platform_name=None, scenario=[],
                 commands=None, vars=None,
                 skip_check=False, hosts=[], scenarios_dir=None):
        self.platform_name = platform_name
        self.scenario = scenario[0]
        self.commands = commands
        self.scenarios_dir = scenarios_dir

    def prepare(self):
        self.validate_input()
        self.prepare_workspace()

    def run(self):
        scenario_executor = Scenario()
        scenario_executor.validate()
        scenario_executor.run()
        self.cleanup_workspace()

    def prepare_workspace(self):
        self.workspace = Workspace()
        self.workspace.create()

    def cleanup_workspace(self):
        pass

    def validate_input(self):
        # Check a scenario was provided
        if not self.scenario:
            raise usage_exc.RunUsageError
        # Validate it actually exists
        else:
            self.scenario_path = file_utils.get_file_path(
                self.scenarios_dir, self.scenario, exact_match=False)
            if not self.scenario_path:
                raise usage_exc.ScenarioNotFoundError(self.scenario)
        LOG.info(f"Found scenario: {self.scenario_path}")
